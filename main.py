"""Ponto de entrada da aplicação."""

from src.application import Workflow
from src.core import constants, logger, settings
from src.infrastructure.bots import SnykBot
from src.infrastructure.clients import PyPiClient
from src.infrastructure.readers import ReaderFactory
from src.infrastructure.repositories import ExcelRepository
from src.share.exceptions import ApplicationError


def main() -> None:
    """Configura os componentes e executa o fluxo principal da aplicação."""

    logger.info("Preparando a aplicação.")
    logger.info(
        "Ambiente selecionado: %s.",
        constants.name,
    )

    driver = settings.create_driver(
        headless=constants.headless,
    )

    reader = ReaderFactory.create(
        file_path=settings.input_file,
    )

    snyk_bot = SnykBot(
        driver=driver,
        package_url=settings.snyk_package_url,
        timeout=settings.webdriver_timeout,
    )

    pypi_client = PyPiClient(
        api_url=settings.pypi_api_url,
        timeout=settings.request_timeout,
    )

    environment_output_file = settings.output_file.with_name(
        constants.output_filename,
    )

    excel_repository = ExcelRepository(
        output_file=environment_output_file,
        score_alert_limit=settings.score_alert_limit,
    )

    workflow = Workflow(
        reader=reader,
        snyk_bot=snyk_bot,
        pypi_client=pypi_client,
        excel_repository=excel_repository,
        driver=driver,
    )

    try:
        workflow.run()

    except ApplicationError as error:
        logger.error(
            "A aplicação foi encerrada com erro: %s",
            error,
        )

    except Exception:
        logger.exception("Ocorreu um erro inesperado.")


if __name__ == "__main__":
    main()