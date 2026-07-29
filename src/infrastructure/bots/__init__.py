# Importa o bot responsável pelo portal Snyk.
from .snyk_bot import SnykBot


# Define a interface pública do pacote bots.
__all__ = [
    "SnykBot",
]