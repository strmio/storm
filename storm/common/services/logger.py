import logging
from typing import Optional, Dict
from .helpers import LogColorNoBold as LogColor
from storm.core.context import AppContext


level_colors = {
    "DEBUG": LogColor.DEBUG,
    "INFO": LogColor.INFO,
    "WARNING": LogColor.WARNING,
    "ERROR": LogColor.ERROR,
    "CRITICAL": LogColor.CRITICAL,
}


class Logger:
    """
    A custom logger with support for colored console logging and plain file logging.
    """

    def __init__(self, name: str = "storm"):
        """
        Initialize the logger.

        :param name: The name of the logger.
        :param log_file: The log file name for file logging.
        """
        # Get the application settings from AppContext
        self.app_settings = AppContext.get_settings()
        self.name = name
        self.log_file = self.app_settings.log_file_path
        self.context: Optional[Dict[str, str]] = None
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.hasHandlers():
            self._initialize_handlers()

    def _initialize_handlers(self):
        """Initialize console and file handlers."""
        self._setup_console_handler()
        if self.app_settings.log_to_file:
            # Only set up file handler if logging to file is enabled
            self._setup_file_handler()

    def _setup_console_handler(self):
        """Set up a console handler with colored output."""
        console_handler = logging.StreamHandler()

        # Custom formatter for colored output
        class ColoredFormatter(logging.Formatter):
            def format(self, record):
                # Get the color for the log level
                log_color = getattr(LogColor, record.levelname, LogColor.RESET)

                # Apply color to levelname and message
                log_color = level_colors.get(record.levelname, LogColor.RESET)
                levelname = f"{log_color}{record.levelname}{LogColor.RESET}"
                message = f"{log_color}{record.getMessage()}{LogColor.RESET}"

                # Logger name in bright yellow
                name = f"{LogColor.NAME}[{record.name}]{LogColor.RESET}"

                # Prefix with [Storm] in green and timestamp in white
                prefix = f"{LogColor.HEADER}[Storm] {record.process} -{LogColor.RESET}"
                timestamp = f"{LogColor.TIMESTAMP}{self.formatTime(record, self.datefmt)}{LogColor.RESET}"

                formatted_message = self._fmt % {
                    "asctime": timestamp,
                    "levelname": levelname,
                    "name": name,
                    "message": message,
                }
                return f"{prefix} {formatted_message}"

        console_formatter = ColoredFormatter(
            fmt="%(asctime)s %(levelname)-7s %(name)s %(message)s",
            datefmt="%Y-%m-%d, %I:%M:%S %p",
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def _setup_file_handler(self):
        """Set up a file handler with plain text formatting."""
        file_handler = logging.FileHandler(self.log_file)
        file_formatter = logging.Formatter(
            fmt="[Storm] %(process)d - %(asctime)s %(levelname)-7s [%(name)s] %(message)s",
            datefmt="%Y-%m-%d, %I:%M:%S %p",
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def set_context(self, context: Dict[str, str]):
        """
        Set the context for logging (e.g., request ID, user ID).

        :param context: A dictionary containing context key-value pairs.
        """
        self.context = context

    def _add_context(self, msg: str) -> str:
        """
        Add context information to the log message.

        :param msg: The original log message.
        :return: The log message with added context information, if available.
        """
        if self.context:
            context_info = " ".join(
                [f"{key}={value}" for key, value in self.context.items()]
            )
            return f"{context_info} {msg}"
        return msg

    def debug(self, msg: str):
        """Log a debug message."""
        self.logger.debug(self._add_context(msg))

    def info(self, msg: str):
        """Log an informational message."""
        self.logger.info(self._add_context(msg))

    def warning(self, msg: str):
        """Log a warning message."""
        self.logger.warning(self._add_context(msg))

    def error(self, msg: str):
        """Log an error message."""
        self.logger.error(self._add_context(msg))

    def critical(self, msg: str):
        """Log a critical error message."""
        self.logger.critical(self._add_context(msg))
