# Importa o repositório responsável pela planilha.
from .excel_repository import ExcelRepository


# Define a interface pública do pacote repositories.
__all__ = [
    "ExcelRepository",
]