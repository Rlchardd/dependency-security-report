# Importa o módulo padrão de logs do Python.
import logging


# Nome usado para identificar os logs da aplicação.
LOGGER_NAME = "dependency_security_report"


# Cria e configura o logger da aplicação.
def create_logger() -> logging.Logger:
    # Obtém um logger com o nome definido acima.
    logger = logging.getLogger(LOGGER_NAME)

    # Define o nível mínimo que será registrado.
    #
    # INFO permite registrar:
    # - INFO
    # - WARNING
    # - ERROR
    # - CRITICAL
    logger.setLevel(logging.INFO)

    # Evita adicionar vários handlers caso este módulo
    # seja importado mais de uma vez.
    if logger.handlers:
        return logger

    # Cria um handler que exibe os logs no terminal.
    console_handler = logging.StreamHandler()

    # Define o nível mínimo do handler.
    console_handler.setLevel(logging.INFO)

    # Define o formato visual dos logs.
    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        ),
        datefmt="%d/%m/%Y %H:%M:%S",
    )

    # Entrega o formato ao handler.
    console_handler.setFormatter(formatter)

    # Adiciona o handler ao logger.
    logger.addHandler(console_handler)

    # Impede que a mesma mensagem seja repetida
    # por loggers superiores.
    logger.propagate = False

    # Devolve o logger configurado.
    return logger


# Cria uma instância que poderá ser importada
# por outras partes da aplicação.
logger = create_logger()