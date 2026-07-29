import logging

LOGGER_NAME: str = "dependency_security_report"

def create_logger(
    level: str = "INFO",
) -> logging.Logger:


    logger = logging.getLogger(
        LOGGER_NAME
    )


    numeric_level = getattr(
        logging,
        level.upper(),
        logging.INFO,
    )


    logger.setLevel(
        numeric_level
    )


    if logger.handlers:


        for handler in logger.handlers:


            handler.setLevel(
                numeric_level
            )


        return logger


    console_handler = logging.StreamHandler()


    console_handler.setLevel(
        numeric_level
    )

    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        ),

        datefmt="%d/%m/%Y %H:%M:%S",
    )

    console_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        console_handler
    )

    logger.propagate = False


    return logger