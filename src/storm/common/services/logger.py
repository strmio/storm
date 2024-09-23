import logging
import colorlog
from pythonjsonlogger import jsonlogger

class Logger:
    def __init__(self, name: str = "storm"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Check if the logger already has handlers to avoid adding them multiple times
        if not self.logger.hasHandlers():
            self._setup_console_handler()
            self._setup_file_handler()

    def _setup_console_handler(self):
        """Set up console handler with colorized output."""
        console_handler = logging.StreamHandler()
        console_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def _setup_file_handler(self):
        """Set up file handler with JSON formatting."""
        file_handler = logging.FileHandler("storm.log")
        file_formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def set_context(self, context: dict):
        """Set the context for logging (e.g., request ID, user ID)."""
        self.context = context

    def _add_context(self, msg: str) -> str:
        """Add context information to the log message."""
        if hasattr(self, 'context'):
            context_info = ' '.join([f"{key}={value}" for key, value in self.context.items()])
            return f"{context_info} {msg}"
        return msg

    def debug(self, msg: str):
        self.logger.debug(self._add_context(msg))

    def info(self, msg: str):
        self.logger.info(self._add_context(msg))

    def warning(self, msg: str):
        self.logger.warning(self._add_context(msg))

    def error(self, msg: str):
        self.logger.error(self._add_context(msg))

    def critical(self, msg: str):
        self.logger.critical(self._add_context(msg))
