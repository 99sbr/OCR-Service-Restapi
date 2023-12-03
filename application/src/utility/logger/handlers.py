from logging.handlers import TimedRotatingFileHandler, SocketHandler
from pathlib import Path
import logging
from dotenv import load_dotenv
import os
import sys
import yaml
# Load environment variables from .env file
load_dotenv()


class Struct:
    """
    Simple class for creating objects with attributes from a dictionary.

    Example:
        >>> data = {'name': 'John', 'age': 30, 'city': 'New York'}
        >>> person = Struct(**data)
        >>> print(person.name)
        John
        >>> print(person.age)
        30
    """

    def __init__(self, **entries):
        self.__dict__.update(entries)


class Handlers:
    """
    Utility class for configuring logging handlers based on a YAML configuration file.

    Attributes:
        conf_path (Path): The path to the logging configuration file.
        formatter (logging.Formatter): The logging formatter.
        log_filename (Path): The path to the log file.
        rotation (str): The log rotation setting.

    Methods:
        _load_logging_config(conf_path: Path) -> Struct:
            Loads the logging configuration from the specified file.

        get_console_handler() -> logging.StreamHandler:
            Retrieves a console logging handler.

        get_file_handler() -> TimedRotatingFileHandler:
            Retrieves a file logging handler with timed rotation.

        get_socket_handler() -> SocketHandler:
            Retrieves a socket logging handler with default listening address.

        get_handlers() -> List[logging.Handler]:
            Retrieves a list of configured logging handlers.
    """

    def __init__(self):
        self.conf_path = Path().joinpath(
            os.environ['SETTING_FOLDER'], os.environ['LOG_CONFIG_FILENAME'])
        logging_config = Handlers._load_logging_config(self.conf_path)
        self.formatter = logging.Formatter(logging_config.FORMATTER)
        self.log_filename = Path().joinpath(
            os.environ['LOG_FOLDER_NAME'], logging_config.FILENAME)
        self.rotation = logging_config.ROTATION

    @staticmethod
    def _load_logging_config(conf_path):
        """
        Loads the logging configuration from the specified file.

        Args:
            conf_path (Path): The path to the logging configuration file.

        Returns:
            Struct: An object containing the logging configuration.
        """
        with open(conf_path) as file:
            config = yaml.safe_load(file)
        config_object = Struct(**config)
        return config_object

    def get_console_handler(self):
        """
        :return:
        """
        console_handler = logging.StreamHandler(sys.stdout.flush())
        console_handler.setFormatter(self.formatter)
        return console_handler

    def get_file_handler(self):
        """

        :return:
        """
        file_handler = TimedRotatingFileHandler(
            self.log_filename, when=self.rotation)
        file_handler.setFormatter(self.formatter)
        return file_handler

    def get_socket_handler(self):
        socket_handler = SocketHandler(
            '127.0.0.1', 19996)  # default listening address
        return socket_handler

    def get_handlers(self):
        return [self.get_console_handler(), self.get_file_handler(), self.get_socket_handler()]
