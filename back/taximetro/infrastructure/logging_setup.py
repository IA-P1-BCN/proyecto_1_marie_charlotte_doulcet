import logging 

def configure_logging(log_file="taximetro.log", level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.handlers.clear()

    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)

    return logger 