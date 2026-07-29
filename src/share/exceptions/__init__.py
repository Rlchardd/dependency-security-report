# Importa as exceções criadas no módulo
# application_exceptions.py.
from .application_exceptions import (
    ApplicationError,
    DependencyFileError,
    DependencyParseError,
    PyPiApiError,
    PyPiPackageNotFoundError,
    SnykPackageNotFoundError,
    SnykScrapingError,
    SpreadsheetError,
)


# Define quais exceções poderão ser importadas
# diretamente pelo pacote src.share.exceptions.
__all__ = [
    "ApplicationError",
    "DependencyFileError",
    "DependencyParseError",
    "PyPiApiError",
    "PyPiPackageNotFoundError",
    "SnykPackageNotFoundError",
    "SnykScrapingError",
    "SpreadsheetError",
]