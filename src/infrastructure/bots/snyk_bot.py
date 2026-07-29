import re
from urllib.parse import quote
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from src.domain.models import (
    DependencyModel,
    SnykModel,
)
from src.share.exceptions import (
    SnykPackageNotFoundError,
    SnykScrapingError,
)

class SnykBot:

    def __init__(
        self,
        driver: WebDriver,
        package_url: str,
        timeout: int,
    ) -> None:

        self.driver = driver

        self.package_url = package_url

        self.timeout = timeout

    def get_package(
        self,
        dependency: DependencyModel,
    ) -> SnykModel:

        package_name = quote(
            dependency.name,
            safe="",
        )

        url = self.package_url.format(
            package=package_name
        )

        try:

            self.driver.get(url)

            wait = WebDriverWait(
                self.driver,
                self.timeout,
            )

            wait.until(self._page_is_loaded)

        except TimeoutException as error:
            raise SnykScrapingError(
                "O tempo limite foi excedido ao consultar "
                f"{dependency.name!r} no Snyk."
            ) from error

        except WebDriverException as error:
            raise SnykScrapingError(
                "O navegador apresentou uma falha ao consultar "
                f"{dependency.name!r} no Snyk."
            ) from error

        page_text = self._get_page_text()

        if self._package_not_found(page_text):
            raise SnykPackageNotFoundError(
                f"Pacote não encontrado no Snyk: "
                f"{dependency.name!r}."
            )

        score = self._extract_score(page_text)

        vulnerabilities = self._extract_vulnerabilities(
            page_text
        )

        return SnykModel(
            score=score,
            vulnerabilities=vulnerabilities,
        )

    @staticmethod
    def _page_is_loaded(
        driver: WebDriver,
    ) -> bool:

        body = driver.find_element(
            By.TAG_NAME,
            "body",
        )

        page_text = body.text

        return any(
            indicator in page_text
            for indicator in (
                "Package Health Score",
                "Direct Vulnerabilities",
                "Page not found",
                "404",
            )
        )

    def _get_page_text(self) -> str:

        body = self.driver.find_element(
            By.TAG_NAME,
            "body",
        )

        return body.text

    @staticmethod
    def _package_not_found(
        page_text: str,
    ) -> bool:

        normalized_text = page_text.lower()

        return any(
            indicator in normalized_text
            for indicator in (
                "page not found",
                "package not found",
                "404 not found",
            )
        )

    @staticmethod
    def _extract_score(
        page_text: str,
    ) -> int | None:

        match = re.search(
            r"Package Health Score\s+(\d{1,3})/100",
            page_text,
            flags=re.IGNORECASE,
        )

        if match is None:
            return None

        score = int(match.group(1))

        if not 0 <= score <= 100:
            return None

        return score

    def _extract_vulnerabilities(
        self,
        page_text: str,
    ) -> int | None:

        vulnerability_links = self.driver.find_elements(
            By.CSS_SELECTOR,
            'a[href*="/vuln/SNYK-"]',
        )

        unique_links: set[str] = set()

        for link in vulnerability_links:


            href = link.get_attribute("href")


            if href:
                unique_links.add(href)

        if unique_links:
            return len(unique_links)

        normalized_text = page_text.lower()

        if (
            "no known security issues" in normalized_text
            or "no known vulnerabilities" in normalized_text
        ):
            return 0


        match = re.search(
            r"(\d+)\s+(?:direct\s+)?"
            r"vulnerabilit(?:y|ies)",
            page_text,
            flags=re.IGNORECASE,
        )

        if match is not None:
            return int(match.group(1))

        return None