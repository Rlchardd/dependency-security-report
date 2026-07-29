# Importa o tipo WebDriver usado na tipagem
# e no fechamento do navegador.
from selenium.webdriver.remote.webdriver import WebDriver

# Importa o logger da aplicação.
from src.core import logger

# Importa os models usados durante o fluxo.
from src.domain.models import (
    DependencyModel,
    PackageReportModel,
    PyPiModel,
    SnykModel,
)

# Importa o bot responsável pelo portal Snyk.
from src.infrastructure.bots import SnykBot

# Importa o cliente responsável pela API do PyPI.
from src.infrastructure.clients import PyPiClient

# Importa a classe-base dos leitores.
from src.infrastructure.readers import DependencyReader

# Importa o repositório responsável pela planilha.
from src.infrastructure.repositories import ExcelRepository

# Importa as exceções específicas das integrações.
from src.share.exceptions import (
    PyPiApiError,
    SnykScrapingError,
)


# Classe responsável por coordenar o caso de uso completo.
class Workflow:

    # O construtor recebe todos os objetos necessários.
    #
    # Isso é chamado de injeção de dependências:
    # o Workflow recebe os componentes prontos,
    # em vez de criá-los internamente.
    def __init__(
        self,
        reader: DependencyReader,
        snyk_bot: SnykBot,
        pypi_client: PyPiClient,
        excel_repository: ExcelRepository,
        driver: WebDriver,
    ) -> None:
        # Guarda o leitor de dependências.
        self.reader = reader

        # Guarda o bot do Snyk.
        self.snyk_bot = snyk_bot

        # Guarda o cliente do PyPI.
        self.pypi_client = pypi_client

        # Guarda o repositório da planilha.
        self.excel_repository = excel_repository

        # Guarda o navegador para fechá-lo ao final.
        self.driver = driver

    # Executa todo o fluxo da aplicação.
    def run(self) -> None:
        # Registra o início do processo.
        logger.info("Iniciando análise das dependências.")

        try:
            # Solicita ao leitor que leia o arquivo.
            #
            # O resultado será uma lista de DependencyModel.
            dependencies = self.reader.read()

            # Registra a quantidade encontrada.
            logger.info(
                "%s dependências encontradas.",
                len(dependencies),
            )

            # Percorre cada dependência.
            for position, dependency in enumerate(
                dependencies,
                start=1,
            ):
                # Registra o progresso.
                logger.info(
                    "Processando %s/%s: %s.",
                    position,
                    len(dependencies),
                    dependency.name,
                )

                # Processa uma única dependência.
                report = self._process_dependency(
                    dependency
                )

                # Entrega o relatório completo ao Excel.
                self.excel_repository.add(report)

                logger.info(
                    "Dependência %s adicionada à planilha.",
                    dependency.name,
                )

            # Salva a planilha depois que todas
            # as dependências forem processadas.
            self.excel_repository.save()

            logger.info(
                "Planilha gerada com sucesso."
            )

        # O finally será executado mesmo que
        # uma exceção interrompa a execução.
        finally:
            # Encerra o navegador.
            self.driver.quit()

            logger.info(
                "Navegador encerrado."
            )

    # Processa uma única dependência.
    def _process_dependency(
        self,
        dependency: DependencyModel,
    ) -> PackageReportModel:
        # Consulta o Snyk.
        snyk_data = self._get_snyk_data(
            dependency
        )

        # Consulta o PyPI.
        pypi_data = self._get_pypi_data(
            dependency
        )

        # Consolida os dados em um único model.
        return PackageReportModel(
            # Nome declarado no arquivo do projeto.
            name=dependency.name,

            # Versão usada no projeto.
            project_version=dependency.version,

            # Descrição retornada pelo PyPI.
            description=pypi_data.description,

            # Score retornado pelo Snyk.
            score=snyk_data.score,

            # Licença retornada pelo PyPI.
            license=pypi_data.license,

            # Última versão retornada pelo PyPI.
            latest_version=pypi_data.latest_version,

            # Vulnerabilidades retornadas pelo Snyk.
            vulnerabilities=(
                snyk_data.vulnerabilities
            ),

            # Data retornada pelo PyPI.
            last_publication=(
                pypi_data.last_publication
            ),
        )

    # Consulta o portal Snyk.
    def _get_snyk_data(
        self,
        dependency: DependencyModel,
    ) -> SnykModel:
        try:
            # Envia o DependencyModel ao bot.
            return self.snyk_bot.get_package(
                dependency
            )

        # Um erro no Snyk não interromperá
        # a análise das outras dependências.
        except SnykScrapingError as error:
            logger.warning(
                "Não foi possível coletar dados do "
                "Snyk para %s: %s",
                dependency.name,
                error,
            )

            # Devolve um model vazio.
            #
            # Score e vulnerabilidades ficarão como None.
            return SnykModel()

    # Consulta a API pública do PyPI.
    def _get_pypi_data(
        self,
        dependency: DependencyModel,
    ) -> PyPiModel:
        try:
            # Envia o DependencyModel ao cliente.
            return self.pypi_client.get_package(
                dependency
            )

        # Um erro no PyPI também não interromperá
        # o processamento dos outros pacotes.
        except PyPiApiError as error:
            logger.warning(
                "Não foi possível coletar dados do "
                "PyPI para %s: %s",
                dependency.name,
                error,
            )

            # O nome é obrigatório no PyPiModel.
            #
            # Os outros campos assumirão None.
            return PyPiModel(
                name=dependency.name
            )