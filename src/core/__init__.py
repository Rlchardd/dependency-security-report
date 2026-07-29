from .settings import settings
from .constants import get_environment_config
from .logger import create_logger

constants = get_environment_config(
    settings.environment
)

logger = create_logger(
    level=constants.log_level
)

__all__ = [
    "constants",
    "logger",
    "settings",
]