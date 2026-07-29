from pydantic import BaseModel, Field


class DependencyModel(BaseModel):

    name: str = Field(
        ...,
        description="Nome da dependência Python.",
    )

    version: str | None = Field(
        default=None,
        description="Versão declarada no projeto, quando disponível.",
    )