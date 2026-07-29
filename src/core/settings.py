# Importa Path para representar caminhos de arquivos e pastas.
from pathlib import Path

# Importa Literal para restringir o ambiente
# aos valores "hg" e "pd".
from typing import Literal

# Importa field_validator para validar e transformar
# configurações antes que sejam armazenadas pelo Pydantic.
from pydantic import field_validator

# Importa BaseSettings para criar configurações tipadas
# e SettingsConfigDict para definir o comportamento do Settings.
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

# Importa o módulo responsável por criar o Chrome.
from selenium import webdriver

# Importa a classe utilizada para configurar o Chrome.
from selenium.webdriver.chrome.options import Options

# Importa WebDriver para documentar o tipo
# retornado pelo método create_driver.
from selenium.webdriver.remote.webdriver import WebDriver


# __file__ representa o caminho deste arquivo.
#
# Este arquivo está em:
# src/core/settings.py
#
# parents[0] → core
# parents[1] → src
# parents[2] → raiz do projeto
BASE_DIR: Path = Path(__file__).resolve().parents[2]


# Classe responsável por centralizar e validar
# as configurações gerais da aplicação.
class Settings(BaseSettings):

    # Configura o comportamento do Pydantic Settings.
    model_config = SettingsConfigDict(
        # Permite carregar valores do arquivo .env.
        env_file=".env",

        # Define UTF-8 como codificação do .env.
        env_file_encoding="utf-8",

        # Ignora configurações adicionais presentes no .env
        # que não estejam declaradas nesta classe.
        extra="ignore",
    )

    # Define o ambiente atual da aplicação.
    #
    # Literal restringe o valor final a:
    # "hg" → homologação
    # "pd" → produção
    #
    # Se ENVIRONMENT não existir no .env,
    # homologação será utilizada como padrão.
    environment: Literal["hg", "pd"] = "hg"

    # Caminho padrão do arquivo de dependências.
    #
    # Esse valor pode ser substituído pelo INPUT_FILE
    # definido no arquivo .env.
    input_file: Path = (
        BASE_DIR / "input" / "requirements.txt"
    )

    # Caminho-base do relatório Excel.
    #
    # Mais tarde, o nome do arquivo será alterado
    # conforme o ambiente selecionado.
    output_file: Path = (
        BASE_DIR / "output" / "dependency_report.xlsx"
    )

    # Modelo da URL usada para consultar pacotes no Snyk.
    snyk_package_url: str = (
        "https://security.snyk.io/package/pip/{package}"
    )

    # Modelo da URL usada para consultar a API do PyPI.
    pypi_api_url: str = (
        "https://pypi.org/pypi/{package}/json"
    )

    # Tempo máximo de espera do Selenium.
    webdriver_timeout: int = 15

    # Tempo máximo das requisições HTTP.
    request_timeout: int = 15

    # Scores menores que este valor serão destacados.
    score_alert_limit: int = 65

    # Configuração antiga mantida como valor alternativo.
    #
    # O ambiente poderá enviar outro valor diretamente
    # ao método create_driver().
    headless: bool = False

    # Valida e normaliza o valor de ENVIRONMENT.
    #
    # mode="before" significa que o método recebe
    # o valor original antes da validação de Literal.
    @field_validator(
        "environment",
        mode="before",
    )
    @classmethod
    def normalize_environment(
        cls,
        value: object,
    ) -> str:
        # Converte o valor para texto.
        #
        # strip() remove espaços no início e no final.
        # lower() transforma as letras em minúsculas.
        normalized_value = str(value).strip().lower()

        # Define diferentes nomes aceitos
        # para o ambiente de homologação.
        homologation_names = {
            "hg",
            "hml",
            "homolog",
            "homologation",
        }

        # Define diferentes nomes aceitos
        # para o ambiente de produção.
        production_names = {
            "pd",
            "prd",
            "prod",
            "production",
        }

        # Todos os nomes de homologação
        # serão transformados no valor padrão "hg".
        if normalized_value in homologation_names:
            return "hg"

        # Todos os nomes de produção
        # serão transformados no valor padrão "pd".
        if normalized_value in production_names:
            return "pd"

        # Se o valor não pertencer a nenhum grupo,
        # interrompe a criação do Settings.
        raise ValueError(
            "Ambiente inválido. Utilize 'hg' para "
            "homologação ou 'pd' para produção."
        )

    # Aplica o mesmo tratamento aos caminhos
    # de entrada e saída.
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
        # Converte o valor recebido para Path.
        path = Path(value)

        # Se o caminho já for absoluto,
        # devolve sem modificações.
        if path.is_absolute():
            return path

        # Se for relativo, adiciona a raiz do projeto.
        #
        # input/pyproject.toml
        #
        # torna-se:
        #
        # C:\...\Desafio 1\input\pyproject.toml
        return BASE_DIR / path

    # Cria as configurações do Chrome.
    #
    # headless pode ser informado pelo ambiente.
    #
    # Se nenhuma configuração for enviada,
    # será utilizado o valor self.headless.
    def create_chrome_options(
        self,
        headless: bool | None = None,
    ) -> Options:
        # Cria o objeto que armazenará
        # as opções do navegador.
        options = Options()

        # Decide qual valor headless será utilizado.
        #
        # Se o argumento for None:
        # utiliza self.headless.
        #
        # Se o argumento for True ou False:
        # utiliza o valor recebido.
        use_headless = (
            self.headless
            if headless is None
            else headless
        )

        # Solicita que o Chrome abra maximizado
        # quando houver uma janela visível.
        options.add_argument("--start-maximized")

        # Desativa solicitações de notificações.
        options.add_argument("--disable-notifications")

        # Se o ambiente solicitar modo headless,
        # adiciona as opções correspondentes.
        if use_headless:
            # Executa o Chrome sem interface visual.
            options.add_argument("--headless=new")

            # Define o tamanho da tela virtual.
            options.add_argument(
                "--window-size=1920,1080"
            )

        # Devolve as opções configuradas.
        return options

    # Cria o WebDriver do Chrome.
    #
    # Também pode receber o valor headless
    # selecionado pelo ambiente.
    def create_driver(
        self,
        headless: bool | None = None,
    ) -> WebDriver:
        # Cria as opções usando o valor recebido.
        options = self.create_chrome_options(
            headless=headless
        )

        # Cria e devolve o navegador configurado.
        return webdriver.Chrome(
            options=options
        )


# Cria a instância central das configurações.
#
# Ao executar esta linha, o Pydantic:
# 1. procura o arquivo .env;
# 2. lê os valores;
# 3. executa os validadores;
# 4. valida os tipos;
# 5. cria o objeto settings.
settings = Settings()