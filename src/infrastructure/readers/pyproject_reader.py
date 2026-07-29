# Importa a biblioteca padrão usada para interpretar arquivos TOML.
import tomllib

# Importa o model que representa uma dependência.
from src.domain.models import DependencyModel

# Importa a classe-base dos leitores.
from src.infrastructure.readers.dependency_reader import (
    DependencyReader,
)

# Importa o parser compartilhado entre os leitores.
from src.infrastructure.readers.dependency_parser import (
    DependencyParser,
)

# Importa a exceção usada para erros de interpretação.
from src.share.exceptions import DependencyParseError


# Leitor especializado em arquivos pyproject.toml.
class PyProjectReader(DependencyReader):

    # Lê o pyproject.toml e devolve uma lista de DependencyModel.
    def read(self) -> list[DependencyModel]:

        # Lê todo o conteúdo do arquivo como texto.
        content = self._read_text()

        try:
            # Converte o conteúdo TOML em um dicionário Python.
            data = tomllib.loads(content)

        # Trata erros na estrutura ou sintaxe TOML.
        except tomllib.TOMLDecodeError as error:
            raise DependencyParseError(
                "O arquivo pyproject.toml possui uma "
                f"estrutura TOML inválida: {self.file_path}"
            ) from error

        # Procura a seção [project].
        project_section = data.get("project")

        # Confirma que a seção existe e é um dicionário.
        if not isinstance(project_section, dict):
            raise DependencyParseError(
                "A seção [project] não foi encontrada no "
                f"arquivo: {self.file_path}"
            )

        # Obtém a lista project.dependencies.
        raw_dependencies = project_section.get("dependencies")

        # Confirma que dependencies é uma lista.
        if not isinstance(raw_dependencies, list):
            raise DependencyParseError(
                "A propriedade project.dependencies não foi "
                f"encontrada ou não é uma lista: {self.file_path}"
            )

        # Lista que armazenará as dependências interpretadas.
        dependencies: list[DependencyModel] = []

        # Percorre as dependências encontradas.
        for index, raw_dependency in enumerate(
            raw_dependencies,
            start=1,
        ):
            # Cada dependência precisa ser uma string.
            if not isinstance(raw_dependency, str):
                raise DependencyParseError(
                    "Dependência inválida na posição "
                    f"{index} de project.dependencies."
                )

            # Envia o texto ao parser compartilhado.
            dependency = DependencyParser.parse(
                raw_dependency=raw_dependency,
                context=(
                    "project.dependencies, "
                    f"posição {index}"
                ),
            )

            # Adiciona o DependencyModel à lista.
            dependencies.append(dependency)

        # Impede o retorno de uma lista vazia.
        if not dependencies:
            raise DependencyParseError(
                f"Nenhuma dependência foi encontrada em: "
                f"{self.file_path}"
            )

        # Devolve todos os models encontrados.
        return dependencies