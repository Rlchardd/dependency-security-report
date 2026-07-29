# Importa o módulo logging da biblioteca padrão do Python.
#
# Ele permite registrar informações sobre a execução,
# avisos, erros e mensagens de depuração.
import logging


# Define um nome único para o logger da aplicação.
#
# Esse nome permite recuperar sempre o mesmo logger
# em diferentes partes do sistema.
LOGGER_NAME: str = "dependency_security_report"


# Cria e configura o logger da aplicação.
#
# O parâmetro level recebe o nível mínimo dos logs.
#
# Exemplos:
# "DEBUG"
# "INFO"
# "WARNING"
# "ERROR"
#
# -> logging.Logger indica que a função devolve
# um objeto Logger configurado.
def create_logger(
    level: str = "INFO",
) -> logging.Logger:

    # Obtém um logger utilizando o nome da aplicação.
    #
    # Se já existir um logger com esse nome,
    # o Python devolve o mesmo objeto.
    logger = logging.getLogger(
        LOGGER_NAME
    )

    # Converte o texto recebido para o valor numérico
    # utilizado internamente pelo módulo logging.
    #
    # Exemplo:
    # "DEBUG" → logging.DEBUG → 10
    # "INFO"  → logging.INFO  → 20
    #
    # level.upper() garante letras maiúsculas.
    #
    # logging.INFO será usado como valor padrão
    # caso o texto informado não corresponda
    # a um nível válido.
    numeric_level = getattr(
        logging,
        level.upper(),
        logging.INFO,
    )

    # Define o nível mínimo aceito pelo logger.
    #
    # Se o nível for DEBUG, mensagens DEBUG,
    # INFO, WARNING, ERROR e CRITICAL aparecem.
    #
    # Se o nível for INFO, mensagens DEBUG
    # ficam ocultas.
    logger.setLevel(
        numeric_level
    )

    # Verifica se esse logger já possui handlers.
    #
    # Handler é o componente responsável por decidir
    # onde as mensagens serão exibidas ou gravadas.
    #
    # Essa verificação evita criar mensagens duplicadas
    # quando o módulo é importado mais de uma vez.
    if logger.handlers:

        # Percorre os handlers que já existem.
        for handler in logger.handlers:

            # Atualiza o nível de cada handler.
            #
            # Isso permite alterar o logger entre
            # DEBUG e INFO sem criar outro handler.
            handler.setLevel(
                numeric_level
            )

        # Devolve o logger já existente e atualizado.
        return logger

    # Cria um handler que envia as mensagens
    # para o terminal.
    console_handler = logging.StreamHandler()

    # Define o nível mínimo aceito pelo handler.
    console_handler.setLevel(
        numeric_level
    )

    # Cria o formato visual das mensagens.
    #
    # %(asctime)s:
    # data e horário.
    #
    # %(levelname)s:
    # nível da mensagem, como INFO ou ERROR.
    #
    # %(message)s:
    # texto enviado ao logger.
    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        ),

        # Define o formato da data e do horário.
        datefmt="%d/%m/%Y %H:%M:%S",
    )

    # Aplica o formato criado ao handler do terminal.
    console_handler.setFormatter(
        formatter
    )

    # Adiciona o handler ao logger.
    #
    # A partir daqui, o logger sabe que deve
    # exibir as mensagens no terminal.
    logger.addHandler(
        console_handler
    )

    # Impede que a mensagem seja repassada
    # para o logger principal do Python.
    #
    # Isso evita que o mesmo log seja exibido
    # duas vezes.
    logger.propagate = False

    # Devolve o logger completamente configurado.
    return logger