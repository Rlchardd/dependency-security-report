# Importa Literal para restringir os valores aceitos
# pelo parâmetro environment.
# Nesse caso, o ambiente deverá ser:
# "hg" para homologação
# ou
# "pd" para produção.
from typing import Literal

# Importa a classe que define o formato
# das configurações de ambiente.
from .environment_config import EnvironmentConfig


# Cria uma função responsável por selecionar
# as configurações do ambiente atual.
# O parâmetro environment recebe somente:
# "hg" ou "pd".
# O retorno será um objeto EnvironmentConfig.
def get_environment_config(
    environment: Literal["hg", "pd"],
) -> EnvironmentConfig:

    # Verifica se o ambiente recebido é produção.
    if environment == "pd":

        # Importa o objeto constants criado em pd.py.
        # Esse import fica dentro do if para carregar
        # apenas o ambiente realmente utilizado.
        from .pd import constants

        # Devolve as configurações de produção.
        return constants

    # Caso o ambiente não seja "pd",
    # utilizamos as configurações de homologação.
    # Como a tipagem aceita apenas "hg" ou "pd",
    # neste ponto o valor esperado é "hg".
    from .hg import constants

    # Devolve as configurações de homologação.
    return constants


# Define quais elementos desta pasta fazem parte
# da interface pública do pacote.
# Isso permite que outros módulos importem:
# from src.core.constants import (
#     EnvironmentConfig,
#     get_environment_config,
# )
__all__ = [
    "EnvironmentConfig",
    "get_environment_config",
]