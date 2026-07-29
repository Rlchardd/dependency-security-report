# Disponibiliza o logger e as configurações
# diretamente pelo pacote src.core.
from .logger import logger
from .settings import settings


__all__ = [
    "logger",
    "settings",
]