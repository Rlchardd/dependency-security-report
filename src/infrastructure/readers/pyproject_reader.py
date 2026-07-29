import tomllib
from src.domain.models import DependencyModel
from src.infrastructure.readers.dependency_reader import (
    DependencyReader,
)
from src.infrastructure.readers.dependency_parser import (
    DependencyParser,
)
from src.share.exceptions import DependencyParseError

class PyProjectReader(DependencyReader):


    def read(self) -> list[DependencyModel]:


        content = self._read_text()

        try:

            data = tomllib.loads(content)

        except tomllib.TOMLDecodeError as error:
            raise DependencyParseError(
                "O arquivo pyproject.toml possui uma "
                f"estrutura TOML inválida: {self.file_path}"
            ) from error

        project_section = data.get("project")

        if not isinstance(project_section, dict):
            raise DependencyParseError(
                "A seção [project] não foi encontrada no "
                f"arquivo: {self.file_path}"
            )

        raw_dependencies = project_section.get("dependencies")

        if not isinstance(raw_dependencies, list):
            raise DependencyParseError(
                "A propriedade project.dependencies não foi "
                f"encontrada ou não é uma lista: {self.file_path}"
            )

        dependencies: list[DependencyModel] = []


        for index, raw_dependency in enumerate(
            raw_dependencies,
            start=1,
        ):

            if not isinstance(raw_dependency, str):
                raise DependencyParseError(
                    "Dependência inválida na posição "
                    f"{index} de project.dependencies."
                )

            dependency = DependencyParser.parse(
                raw_dependency=raw_dependency,
                context=(
                    "project.dependencies, "
                    f"posição {index}"
                ),
            )

            dependencies.append(dependency)

        if not dependencies:
            raise DependencyParseError(
                f"Nenhuma dependência foi encontrada em: "
                f"{self.file_path}"
            )

        return dependencies