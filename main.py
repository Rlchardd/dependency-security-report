# Importa a classe que coordena todo o processo.
from src.application import Workflow

# Importa configurações e logger.
from src.core import (
    constants,
    logger,
    settings,
)

# Importa o bot do Snyk.
from src.infrastructure.bots import SnykBot

# Importa o cliente do PyPI.
from src.infrastructure.clients import PyPiClient

# Importa a Factory dos leitores.
from src.infrastructure.readers import ReaderFactory

# Importa o repositório da planilha.
from src.infrastructure.repositories import (
    ExcelRepository,
)

# Importa a exceção-base da aplicação.
from src.share.exceptions import ApplicationError


# Função principal e ponto de composição da aplicação.
#
# Ela cria os objetos e estabelece
# como eles serão conectados.
def main() -> None:
    # Registra o início da aplicação.
    logger.info("Preparando a aplicação.")

    logger.info(
        "Ambiente selecionado: %s.",
        constants.name,
    )
    
    # Cria o navegador conforme o ambiente selecionado.
    # Homologação:
    # headless=False → Chrome aparece.
    # Produção:
    # headless=True → Chrome não aparece.
    driver = settings.create_driver(
        headless=constants.headless
    )

    # Solicita à Factory o leitor apropriado.
    reader = ReaderFactory.create(
        file_path=settings.input_file
    )

    # Cria o bot do Snyk e entrega o navegador.
    snyk_bot = SnykBot(
        driver=driver,
        package_url=settings.snyk_package_url,
        timeout=settings.webdriver_timeout,
    )

    # Cria o cliente da API do PyPI.
    pypi_client = PyPiClient(
        api_url=settings.pypi_api_url,
        timeout=settings.request_timeout,
    )

    # Mantém a pasta configurada em settings.output_file,
    # mas substitui o nome conforme o ambiente.
    # Exemplo:
    # output/dependency_report.xlsx
    # Em homologação torna-se:
    # output/dependency_report_hg.xlsx
    environment_output_file = (
        settings.output_file.with_name(
            constants.output_filename
        )
    )
    
    # Cria o repositório responsável pelo Excel.
    excel_repository = ExcelRepository(
    output_file=environment_output_file,
    score_alert_limit=settings.score_alert_limit,
     )

    # Cria o Workflow e conecta todos os componentes.
    workflow = Workflow(
        reader=reader,
        snyk_bot=snyk_bot,
        pypi_client=pypi_client,
        excel_repository=excel_repository,
        driver=driver,
    )

    try:
        # Inicia o processo completo.
        workflow.run()

    # Captura os erros controlados da aplicação.
    except ApplicationError as error:
        logger.error(
            "A aplicação foi encerrada com erro: %s",
            error,
        )

    # Captura erros inesperados.
    #
    # logger.exception também registra o traceback.
    except Exception:
        logger.exception(
            "Ocorreu um erro inesperado."
        )


# Executa o programa somente quando este arquivo
# for iniciado diretamente.
if __name__ == "__main__":
    main()