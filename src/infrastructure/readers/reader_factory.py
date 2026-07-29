from pathlib import Path

from src.infrastructure.readers.dependency_reader import DependencyReader
from src.infrastructure.readers.pyproject_reader import PyProjectReader
from src.infrastructure.readers.requirements_reader import RequirementsReader
from src.share.exceptions import DependencyFileError


class ReaderFactory:

    @staticmethod
    def create(file_path: Path) -> DependencyReader:
        file_name = file_path.name.lower()

        if file_name == "requirements.txt":
            return RequirementsReader(file_path=file_path)

        if file_name == "pyproject.toml":
            return PyProjectReader(file_path=file_path)

        raise DependencyFileError(
            f"Formato de arquivo não suportado: {file_path.name}. "
            "Utilize requirements.txt ou pyproject.toml."
        )