"""Configurações da aplicação e criação do WebDriver."""

from pathlib import Path
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver


BASE_DIR: Path = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Centraliza e valida as configurações da aplicação."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: Literal["hg", "pd"] = "hg"

    input_file: Path = BASE_DIR / "input" / "requirements.txt"
    output_file: Path = BASE_DIR / "output" / "dependency_report.xlsx"

    snyk_package_url: str = (
        "https://security.snyk.io/package/pip/{package}"
    )
    pypi_api_url: str = "https://pypi.org/pypi/{package}/json"

    webdriver_timeout: int = 15
    request_timeout: int = 15
    score_alert_limit: int = 65
    headless: bool = False

    @field_validator(
        "environment",
        mode="before",
    )
    @classmethod
    def normalize_environment(
        cls,
        value: object,
    ) -> str:
        """Normaliza o identificador do ambiente."""
        normalized_value = str(value).strip().lower()

        homologation_names = {
            "hg",
            "hml",
            "homolog",
            "homologation",
        }

        production_names = {
            "pd",
            "prd",
            "prod",
            "production",
        }

        if normalized_value in homologation_names:
            return "hg"

        if normalized_value in production_names:
            return "pd"

        raise ValueError(
            "Ambiente inválido. Utilize 'hg' para "
            "homologação ou 'pd' para produção."
        )

    @field_validator(
        "input_file",
        "output_file",
        mode="before",
    )
    @classmethod
    def resolve_project_path(
        cls,
        value: str | Path,
    ) -> Path:
        """Resolve caminhos relativos a partir da raiz do projeto."""
        path = Path(value)

        if path.is_absolute():
            return path

        return BASE_DIR / path

    def create_chrome_options(
        self,
        headless: bool | None = None,
    ) -> Options:
        """Cria as opções de execução do navegador Chrome."""
        options = Options()

        use_headless = (
            self.headless
            if headless is None
            else headless
        )

        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")

        if use_headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

        return options

    def create_driver(
        self,
        headless: bool | None = None,
    ) -> WebDriver:
        """Cria uma instância configurada do Chrome WebDriver."""
        options = self.create_chrome_options(
            headless=headless,
        )

        return webdriver.Chrome(
            options=options,
        )


settings = Settings()