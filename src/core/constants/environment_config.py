# Importa dataclass, utilizada para criar uma classe
# voltada principalmente ao armazenamento de dados.
from dataclasses import dataclass


# @dataclass gera automaticamente métodos como:
# __init__, __repr__ e __eq__.
#
# frozen=True impede que os atributos sejam alterados
# depois que o objeto for criado.
#
# slots=True restringe os atributos disponíveis
# aos campos definidos nesta classe.
@dataclass(
    frozen=True,
    slots=True,
)
class EnvironmentConfig:
    # Nome descritivo do ambiente.
    #
    # Exemplos:
    # "homologation"
    # "production"
    name: str

    # Define se o Chrome será executado
    # sem abrir uma janela visível.
    headless: bool

    # Define o nível mínimo dos logs.
    #
    # Exemplos:
    # "DEBUG"
    # "INFO"
    log_level: str

    # Define o nome do arquivo Excel
    # gerado naquele ambiente.
    output_filename: str