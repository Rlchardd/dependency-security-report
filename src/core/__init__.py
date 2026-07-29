# Importa primeiro as configurações gerais da aplicação.
#
# Durante essa importação, o Settings lê o arquivo .env
# e identifica o ambiente configurado.
from .settings import settings

# Importa a função responsável por selecionar
# as constantes de homologação ou produção.
from .constants import get_environment_config

# Importa a função que cria e configura o logger.
from .logger import create_logger


# Seleciona as constantes correspondentes
# ao ambiente lido pelo Settings.
#
# Exemplo:
# settings.environment == "hg"
#     → carrega as constantes de homologação
#
# settings.environment == "pd"
#     → carrega as constantes de produção
constants = get_environment_config(
    settings.environment
)


# Cria o logger utilizando o nível definido
# pelo ambiente selecionado.
#
# Homologação:
# constants.log_level == "DEBUG"
#
# Produção:
# constants.log_level == "INFO"
logger = create_logger(
    level=constants.log_level
)


# Define os objetos públicos disponibilizados
# pelo pacote src.core.
#
# Isso permite utilizar:
#
# from src.core import constants, logger, settings
__all__ = [
    "constants",
    "logger",
    "settings",
]