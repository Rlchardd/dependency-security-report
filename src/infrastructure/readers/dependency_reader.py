from abc import ABC, abstractmethod
from pathlib import Path
from src.domain.models import DependencyModel
from src.share.exceptions import DependencyFileError

class DependencyReader(ABC):


    def __init__(self, file_path: Path) -> None:

        self.file_path = file_path

    def _validate_file(self) -> None:
        # Verifica se o caminho existe.
        if not self.file_path.exists():
            raise DependencyFileError(
                "Arquivo de dependências não encontrado: "
                f"{self.file_path}"
            )

        if not self.file_path.is_file():
            raise DependencyFileError(
                "O caminho informado não representa um arquivo: "
                f"{self.file_path}"
            )


    def _read_text(self) -> str:

        self._validate_file()

        try:

            return self.file_path.read_text(
                encoding="utf-8"
            )

        except OSError as error:
            raise DependencyFileError(
                "Não foi possível ler o arquivo: "
                f"{self.file_path}"
            ) from error

        except UnicodeError as error:
            raise DependencyFileError(
                "O arquivo não pôde ser interpretado como UTF-8: "
                f"{self.file_path}"
            ) from error


    def _read_lines(self) -> list[str]:

        content = self._read_text()

        return content.splitlines()

    @abstractmethod
    def read(self) -> list[DependencyModel]:
        raise NotImplementedError