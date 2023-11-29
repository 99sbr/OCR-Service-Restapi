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
    def __init__(self, **entries):
        self.__dict__.update(entries)

class Handlers:

    def __init__(self):
        self.conf_path =  Path().joinpath(os.environ['SETTING_FOLDER'], os.environ['LOG_CONFIG_FILENAME'])
        logging_config = Handlers._load_logging_config(self.conf_path)
        self.formatter = logging.Formatter(logging_config.FORMATTER)
        self.log_filename = Path().joinpath(
            os.environ['LOG_FOLDER_NAME'], logging_config.FILENAME)
        self.rotation = logging_config.ROTATION

    @staticmethod
    def _load_logging_config(conf_path):
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
        socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
        return socket_handler

    def get_handlers(self):
        return [self.get_console_handler(), self.get_file_handler(), self.get_socket_handler()]