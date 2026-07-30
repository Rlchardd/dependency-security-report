from datetime import datetime
from pydantic import BaseModel, Field



class PyPiModel(BaseModel):

    name: str = Field(
        ...,
        description="Nome oficial do pacote no PyPI.",
    )

    description: str | None = Field(
        default=None,
        description="Descrição resumida do pacote.",
    )

    license: str | None = Field(
        default=None,
        description="Licença informada pelo pacote.",
    )


    latest_version: str | None = Field(
        default=None,
        description="Última versão disponível no PyPI.",
    )


    last_publication: datetime | None = Field(
        default=None,
        description="Data da publicação mais recente.",
    )