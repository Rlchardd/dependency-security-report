# Importa as ferramentas usadas para interpretar
# declarações de dependências Python.
from packaging.requirements import (
    InvalidRequirement,
    Requirement,
)

# Importa o model que representa uma dependência.
from src.domain.models import DependencyModel

# Importa a exceção usada quando uma dependência
# não puder ser interpretada.
from src.share.exceptions import DependencyParseError


# Classe responsável exclusivamente por interpretar
# declarações de dependências.
class DependencyParser:

    # Método estático porque não precisa acessar
    # atributos de uma instância por meio de self.
    @staticmethod
    def parse(
        raw_dependency: str,
        context: str,
    ) -> DependencyModel:

        # Tenta interpretar o texto recebido.
        try:
            requirement = Requirement(raw_dependency)

        # Trata especificamente dependências inválidas.
        except InvalidRequirement as error:
            raise DependencyParseError(
                f"Dependência inválida em {context}: "
                f"{raw_dependency!r}"
            ) from error

        # Extrai a versão ou a restrição de versão.
        version = DependencyParser._extract_version(
            requirement
        )

        # Cria e devolve o model padronizado.
        return DependencyModel(
            name=requirement.name,
            version=version,
        )

    # Método interno responsável por extrair
    # a versão da declaração.
    @staticmethod
    def _extract_version(
        requirement: Requirement,
    ) -> str | None:

        # Converte o especificador de versão em texto.
        specifier = str(requirement.specifier)

        # Se não houver versão declarada, devolve None.
        if not specifier:
            return None

        # Caso seja uma versão exata, remove o operador ==.
        if specifier.startswith("==") and "," not in specifier:
            return specifier.removeprefix("==")

        # Para operadores como >=, <= e ~=,
        # mantém o especificador completo.
        return specifier