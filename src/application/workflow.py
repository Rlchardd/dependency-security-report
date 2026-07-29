from selenium.webdriver.remote.webdriver import WebDriver
from src.core import logger
from src.domain.models import (
    DependencyModel,
    PackageReportModel,
    PyPiModel,
    SnykModel,
)
from src.infrastructure.bots import SnykBot
from src.infrastructure.clients import PyPiClient
from src.infrastructure.readers import DependencyReader
from src.infrastructure.repositories import ExcelRepository
from src.share.exceptions import (
    PyPiApiError,
    SnykScrapingError,
)

class Workflow:

    def __init__(
        self,
        reader: DependencyReader,
        snyk_bot: SnykBot,
        pypi_client: PyPiClient,
        excel_repository: ExcelRepository,
        driver: WebDriver,
    ) -> None:
        self.reader = reader

        self.snyk_bot = snyk_bot

        self.pypi_client = pypi_client

        self.excel_repository = excel_repository

        self.driver = driver

    def run(self) -> None:

        logger.info("Iniciando análise das dependências.")

        try:

            dependencies = self.reader.read()

            logger.info(
                "%s dependências encontradas.",
                len(dependencies),
            )

            for position, dependency in enumerate(
                dependencies,
                start=1,
            ):
                logger.info(
                    "Processando %s/%s: %s.",
                    position,
                    len(dependencies),
                    dependency.name,
                )

                report = self._process_dependency(
                    dependency
                )

                self.excel_repository.add(report)

                logger.info(
                    "Dependência %s adicionada à planilha.",
                    dependency.name,
                )

            self.excel_repository.save()

            logger.info(
                "Planilha gerada com sucesso."
            )


        finally:

            self.driver.quit()

            logger.info(
                "Navegador encerrado."
            )


    def _process_dependency(
        self,
        dependency: DependencyModel,
    ) -> PackageReportModel:

        snyk_data = self._get_snyk_data(
            dependency
        )


        pypi_data = self._get_pypi_data(
            dependency
        )


        return PackageReportModel(

            name=dependency.name,


            project_version=dependency.version,


            description=pypi_data.description,


            score=snyk_data.score,


            license=pypi_data.license,


            latest_version=pypi_data.latest_version,


            vulnerabilities=(
                snyk_data.vulnerabilities
            ),


            last_publication=(
                pypi_data.last_publication
            ),
        )


    def _get_snyk_data(
        self,
        dependency: DependencyModel,
    ) -> SnykModel:
        try:

            return self.snyk_bot.get_package(
                dependency
            )


        except SnykScrapingError as error:
            logger.warning(
                "Não foi possível coletar dados do "
                "Snyk para %s: %s",
                dependency.name,
                error,
            )


            return SnykModel()


    def _get_pypi_data(
        self,
        dependency: DependencyModel,
    ) -> PyPiModel:
        try:

            return self.pypi_client.get_package(
                dependency
            )

        except PyPiApiError as error:
            logger.warning(
                "Não foi possível coletar dados do "
                "PyPI para %s: %s",
                dependency.name,
                error,
            )

            return PyPiModel(
                name=dependency.name
            )