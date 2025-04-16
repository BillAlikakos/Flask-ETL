import logging

class Logger:
    @staticmethod
    def get_logger():
        logger = logging.getLogger("etl")
        if not logger.hasHandlers():
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        return logger
