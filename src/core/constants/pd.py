# Importa a classe que define o formato
# obrigatório das configurações de ambiente.
from .environment_config import EnvironmentConfig


# Cria o objeto com as configurações
# específicas do ambiente de produção.
# O nome "constants" é igual ao utilizado em hg.py.
# Isso permite que o seletor de ambientes devolva
# sempre uma interface padronizada.
constants = EnvironmentConfig(
    # Nome descritivo do ambiente.
    name="production",

    # True executa o Chrome sem abrir
    # uma janela visível na tela.
    headless=True,

    # INFO registra as etapas importantes da aplicação,
    # sem o nível de detalhamento do DEBUG.
    log_level="INFO",

    # Define o nome do relatório oficial
    # gerado no ambiente de produção.
    output_filename="dependency_report.xlsx",
)