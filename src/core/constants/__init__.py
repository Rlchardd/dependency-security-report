from typing import Literal
from .environment_config import EnvironmentConfig
def get_environment_config(
    environment: Literal["hg", "pd"],
) -> EnvironmentConfig:


    if environment == "pd":


        from .pd import constants


        return constants

    from .hg import constants


    return constants

__all__ = [
    "EnvironmentConfig",
    "get_environment_config",
]