from packaging.requirements import (
    InvalidRequirement,
    Requirement,
)


from src.domain.models import DependencyModel


from src.infrastructure.readers.dependency_reader import (
    DependencyReader,
)


from src.share.exceptions import DependencyParseError



class RequirementsReader(DependencyReader):

    
    def read(self) -> list[DependencyModel]:

        
        dependencies: list[DependencyModel] = []

        
        for line_number, raw_line in enumerate(
            self._read_lines(),
            start=1,
        ):

            
            line = self._clean_line(
                raw_line=raw_line,
                line_number=line_number,
            )

           
            if line is None:
                continue

           
            try:

            
                requirement = Requirement(line)

            
            except InvalidRequirement as error:
                raise DependencyParseError(
                    f"Dependência inválida na linha "
                    f"{line_number}: {raw_line!r}"
                ) from error

            
            version = self._extract_version(requirement)

            
            dependency = DependencyModel(
                name=requirement.name,
                version=version,
            )

            dependencies.append(dependency)

       
        if not dependencies:
            raise DependencyParseError(
                f"Nenhuma dependência válida foi encontrada em: "
                f"{self.file_path}"
            )

        
        return dependencies

    @staticmethod
    def _clean_line(
        raw_line: str,
        line_number: int,
    ) -> str | None:

        
        line = raw_line.strip()

        
        if not line:

            
            return None

        
        if line.startswith("#"):
            return None

       
        if " #" in line:

            
            line = line.split(" #", maxsplit=1)[0].strip()


        unsupported_prefixes = (
            "-r ",
            "--requirement ",
            "-e ",
            "--editable ",
        )

        if line.startswith(unsupported_prefixes):
            raise DependencyParseError(
                f"Formato não suportado na linha "
                f"{line_number}: {raw_line!r}"
            )

        return line

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