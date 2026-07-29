from datetime import datetime

from pydantic import BaseModel, Field

class PackageReportModel(BaseModel):
    # Nome da dependência.
    name: str = Field(
        ...,
        description="Nome da dependência.",
    )

    project_version: str | None = Field(
        default=None,
        description="Versão declarada no projeto.",
    )

    description: str | None = Field(
        default=None,
        description="Descrição da dependência.",
    )

    score: int | None = Field(
        default=None,
        ge=0,
        le=100,
        description="Pontuação do pacote no Snyk.",
    )

    license: str | None = Field(
        default=None,
        description="Licença da dependência.",
    )

    latest_version: str | None = Field(
        default=None,
        description="Última versão disponível.",
    )

    vulnerabilities: int | None = Field(
        default=None,
        ge=0,
        description="Quantidade de vulnerabilidades.",
    )

    last_publication: datetime | None = Field(
        default=None,
        description="Data da última publicação.",
    )