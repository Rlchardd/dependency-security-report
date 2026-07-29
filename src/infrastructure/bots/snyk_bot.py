# Importa expressões regulares.
#
# Utilizaremos regex para encontrar o Score
# dentro do texto exibido na página.
import re

# Importa quote para preparar corretamente
# o nome do pacote antes de inseri-lo na URL.
from urllib.parse import quote

# Importa os componentes do Selenium.
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

# Importa os models usados como entrada e saída.
from src.domain.models import (
    DependencyModel,
    SnykModel,
)

# Importa as exceções específicas do bot.
from src.share.exceptions import (
    SnykPackageNotFoundError,
    SnykScrapingError,
)


# Classe responsável pela automação do portal Snyk.
class SnykBot:

    # Método construtor.
    #
    # driver:
    # Navegador já criado e controlado pelo Selenium.
    #
    # package_url:
    # Modelo de URL utilizado para acessar um pacote.
    #
    # timeout:
    # Tempo máximo de espera pelo carregamento da página.
    def __init__(
        self,
        driver: WebDriver,
        package_url: str,
        timeout: int,
    ) -> None:

        # Guarda o WebDriver dentro do objeto.
        self.driver = driver

        # Guarda o modelo de URL.
        self.package_url = package_url

        # Guarda o tempo máximo de espera.
        self.timeout = timeout

    # Consulta um pacote no portal Snyk.
    #
    # Recebe:
    # DependencyModel.
    #
    # Retorna:
    # SnykModel.
    def get_package(
        self,
        dependency: DependencyModel,
    ) -> SnykModel:

        # Prepara o nome para ser utilizado com segurança na URL.
        #
        # Por exemplo, espaços e caracteres especiais
        # seriam convertidos para o formato apropriado.
        package_name = quote(
            dependency.name,
            safe="",
        )

        # Substitui {package} pelo nome da dependência.
        url = self.package_url.format(
            package=package_name
        )

        try:
            # Solicita ao Chrome que acesse a página do pacote.
            self.driver.get(url)

            # Cria uma espera explícita.
            wait = WebDriverWait(
                self.driver,
                self.timeout,
            )

            # Aguarda até que a página apresente algum dos textos
            # que indicam que seu conteúdo principal foi carregado.
            wait.until(self._page_is_loaded)

        # Trata o caso em que o conteúdo não carregou
        # dentro do tempo máximo.
        except TimeoutException as error:
            raise SnykScrapingError(
                "O tempo limite foi excedido ao consultar "
                f"{dependency.name!r} no Snyk."
            ) from error

        # Trata outros erros produzidos pelo WebDriver.
        except WebDriverException as error:
            raise SnykScrapingError(
                "O navegador apresentou uma falha ao consultar "
                f"{dependency.name!r} no Snyk."
            ) from error

        # Obtém todo o texto visível da página.
        page_text = self._get_page_text()

        # Verifica se a página indica que o pacote não existe.
        if self._package_not_found(page_text):
            raise SnykPackageNotFoundError(
                f"Pacote não encontrado no Snyk: "
                f"{dependency.name!r}."
            )

        # Extrai o Package Health Score.
        score = self._extract_score(page_text)

        # Extrai ou estima a quantidade de vulnerabilidades.
        vulnerabilities = self._extract_vulnerabilities(
            page_text
        )

        # Cria e devolve o model com os resultados.
        return SnykModel(
            score=score,
            vulnerabilities=vulnerabilities,
        )

    # Verifica se o conteúdo principal da página foi carregado.
    #
    # O Selenium chama essa função repetidamente
    # durante o WebDriverWait.
    @staticmethod
    def _page_is_loaded(
        driver: WebDriver,
    ) -> bool:

        # Localiza o body, que contém o texto visível da página.
        body = driver.find_element(
            By.TAG_NAME,
            "body",
        )

        # Obtém o texto visível.
        page_text = body.text

        # Retorna True quando encontra algum indicador
        # de carregamento ou de página inexistente.
        return any(
            indicator in page_text
            for indicator in (
                "Package Health Score",
                "Direct Vulnerabilities",
                "Page not found",
                "404",
            )
        )

    # Obtém o texto visível de toda a página.
    def _get_page_text(self) -> str:

        # Localiza o elemento body.
        body = self.driver.find_element(
            By.TAG_NAME,
            "body",
        )

        # Devolve seu texto.
        return body.text

    # Verifica se a página representa um pacote inexistente.
    @staticmethod
    def _package_not_found(
        page_text: str,
    ) -> bool:

        # Converte o texto para minúsculas para facilitar
        # comparações sem diferenciar maiúsculas e minúsculas.
        normalized_text = page_text.lower()

        # Retorna True caso alguma mensagem de erro seja encontrada.
        return any(
            indicator in normalized_text
            for indicator in (
                "page not found",
                "package not found",
                "404 not found",
            )
        )

    # Extrai o Score do texto da página.
    @staticmethod
    def _extract_score(
        page_text: str,
    ) -> int | None:

        # Procura um trecho semelhante a:
        #
        # Package Health Score
        # 91/100
        #
        # \s+ representa um ou mais espaços ou quebras de linha.
        # (\d{1,3}) captura um número de um a três dígitos.
        match = re.search(
            r"Package Health Score\s+(\d{1,3})/100",
            page_text,
            flags=re.IGNORECASE,
        )

        # Se o padrão não for encontrado, devolve None.
        if match is None:
            return None

        # group(1) contém o número capturado.
        score = int(match.group(1))

        # Validação defensiva para impedir valores fora do intervalo.
        if not 0 <= score <= 100:
            return None

        # Devolve o Score convertido para inteiro.
        return score

    # Extrai a quantidade de vulnerabilidades.
    def _extract_vulnerabilities(
        self,
        page_text: str,
    ) -> int | None:

        # Primeiro, procura links de vulnerabilidades do Snyk.
        #
        # Um mesmo link pode aparecer mais de uma vez,
        # por isso utilizaremos um conjunto para remover duplicações.
        vulnerability_links = self.driver.find_elements(
            By.CSS_SELECTOR,
            'a[href*="/vuln/SNYK-"]',
        )

        # Cria um conjunto vazio.
        unique_links: set[str] = set()

        # Percorre todos os elementos encontrados.
        for link in vulnerability_links:

            # Obtém o endereço armazenado no atributo href.
            href = link.get_attribute("href")

            # Adiciona apenas endereços válidos.
            if href:
                unique_links.add(href)

        # Se foram encontrados links únicos,
        # a quantidade será o tamanho do conjunto.
        if unique_links:
            return len(unique_links)

        # Alguns pacotes não possuem vulnerabilidades conhecidas.
        normalized_text = page_text.lower()

        # Nesse caso, devolvemos zero.
        if (
            "no known security issues" in normalized_text
            or "no known vulnerabilities" in normalized_text
        ):
            return 0

        # Tenta localizar uma quantidade explícita no texto.
        #
        # Exemplos:
        # 2 vulnerabilities
        # 1 vulnerability
        match = re.search(
            r"(\d+)\s+(?:direct\s+)?"
            r"vulnerabilit(?:y|ies)",
            page_text,
            flags=re.IGNORECASE,
        )

        # Se encontrou, converte para inteiro.
        if match is not None:
            return int(match.group(1))

        # Quando não for possível determinar,
        # devolve None em vez de inventar um valor.
        return None