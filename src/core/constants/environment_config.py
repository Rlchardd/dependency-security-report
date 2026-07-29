
from dataclasses import dataclass

@dataclass(
    frozen=True,
    slots=True,
)
class EnvironmentConfig:

    name: str

    headless: bool

    log_level: str

    output_filename: str