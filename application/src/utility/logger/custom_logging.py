import logging
from typing import List

from application.src.utility.logger.handlers import Handlers


class LogHandler(object):
    """
    Utility class for managing loggers with multiple handlers.

    Attributes:
        available_handlers (List): A list of available log handlers.

    Methods:
        get_logger(logger_name: str) -> logging.Logger:
            Retrieves a configured logger with specified name and attached handlers.

            Args:
                logger_name (str): The name of the logger.

            Returns:
                logging.Logger: A configured logger instance.

            Example:
                >>> log_handler = LogHandler()
                >>> logger = log_handler.get_logger("example_logger")
                >>> logger.info("This is a log message.")
    """

    def __init__(self):
        self.available_handlers: List = Handlers().get_handlers()

    def get_logger(self, logger_name):
        """

        :param logger_name:
        :return:
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        if logger.hasHandlers():
            logger.handlers.clear()
        for handler in self.available_handlers:
            logger.addHandler(handler)
        logger.propagate = False
        return logger
