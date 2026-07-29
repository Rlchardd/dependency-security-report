
from pydantic import BaseModel, Field

class SnykModel(BaseModel):

    score: int | None = Field(
        default=None,
        ge=0,
        le=100,
        description="Pontuação do pacote no portal Snyk.",
    )

    vulnerabilities: int | None = Field(
        default=None,
        ge=0,
        description="Quantidade de vulnerabilidades encontradas.",
    )