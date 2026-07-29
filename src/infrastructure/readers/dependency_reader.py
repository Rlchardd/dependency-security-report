# Importa recursos usados para criar uma classe abstrata.
from abc import ABC, abstractmethod

# Importa Path para representar caminhos de arquivos.
from pathlib import Path

# Importa o model que representa uma dependência.
from src.domain.models import DependencyModel

# Importa a exceção usada para problemas de arquivo.
from src.share.exceptions import DependencyFileError


# Classe-base abstrata dos leitores de dependências.
class DependencyReader(ABC):

    # Recebe o caminho do arquivo que será analisado.
    def __init__(self, file_path: Path) -> None:
        # Guarda o caminho dentro do objeto.
        self.file_path = file_path

    # Valida se o caminho existe e representa um arquivo.
    def _validate_file(self) -> None:
        # Verifica se o caminho existe.
        if not self.file_path.exists():
            raise DependencyFileError(
                "Arquivo de dependências não encontrado: "
                f"{self.file_path}"
            )

        # Verifica se o caminho aponta realmente para um arquivo.
        if not self.file_path.is_file():
            raise DependencyFileError(
                "O caminho informado não representa um arquivo: "
                f"{self.file_path}"
            )

    # Lê e devolve todo o conteúdo do arquivo como uma string.
    def _read_text(self) -> str:
        # Valida o arquivo antes de tentar abri-lo.
        self._validate_file()

        try:
            # Lê todo o conteúdo utilizando UTF-8.
            return self.file_path.read_text(
                encoding="utf-8"
            )

        # Trata problemas do sistema operacional.
        except OSError as error:
            raise DependencyFileError(
                "Não foi possível ler o arquivo: "
                f"{self.file_path}"
            ) from error

        # Trata problemas relacionados à codificação do arquivo.
        except UnicodeError as error:
            raise DependencyFileError(
                "O arquivo não pôde ser interpretado como UTF-8: "
                f"{self.file_path}"
            ) from error

    # Lê o conteúdo e devolve uma lista de linhas.
    def _read_lines(self) -> list[str]:
        # Reaproveita o método que lê o texto completo.
        content = self._read_text()

        # Divide o conteúdo nas linhas do arquivo.
        return content.splitlines()

    # Define o contrato que os leitores concretos devem implementar.
    @abstractmethod
    def read(self) -> list[DependencyModel]:
        raise NotImplementedError