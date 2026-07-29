# Importa a classe que define o formato
# obrigatório das configurações de ambiente.
from .environment_config import EnvironmentConfig


# Cria o objeto com as configurações
# específicas do ambiente de homologação.
#
# Mantemos o nome "constants" porque o arquivo
# de produção também disponibilizará um objeto
# com esse mesmo nome.
constants = EnvironmentConfig(
    # Nome descritivo do ambiente.
    name="homologation",

    # False mantém o navegador visível.
    #
    # Isso facilita acompanhar, testar e depurar
    # a automação durante o desenvolvimento.
    headless=False,

    # DEBUG permite exibir logs mais detalhados.
    log_level="DEBUG",

    # Define um nome específico para o relatório
    # gerado no ambiente de homologação.
    #
    # Assim, ele não sobrescreve o relatório
    # utilizado em produção.
    output_filename="dependency_report_hg.xlsx",
)