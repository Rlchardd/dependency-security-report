from packaging.requirements import (
    InvalidRequirement,
    Requirement,
)
from src.domain.models import DependencyModel
from src.share.exceptions import DependencyParseError

class DependencyParser:

    @staticmethod
    def parse(
        raw_dependency: str,
        context: str,
    ) -> DependencyModel:

        try:
            requirement = Requirement(raw_dependency)

        except InvalidRequirement as error:
            raise DependencyParseError(
                f"Dependência inválida em {context}: "
                f"{raw_dependency!r}"
            ) from error

        version = DependencyParser._extract_version(
            requirement
        )

        return DependencyModel(
            name=requirement.name,
            version=version,
        )

    @staticmethod
    def _extract_version(
        requirement: Requirement,
    ) -> str | None:

        specifier = str(requirement.specifier)

        if not specifier:
            return None

        if specifier.startswith("==") and "," not in specifier:
            return specifier.removeprefix("==")

        return specifier