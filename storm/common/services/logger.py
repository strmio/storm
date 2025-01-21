import logging
from typing import Optional, Dict


class Logger:
    """
    A custom logger with support for colored console logging and plain file logging.
    """

    # Define ANSI escape codes for colors
    LOG_COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",   # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",   # Red
        "CRITICAL": "\033[1;31m",  # Bold Red
        "NAME": "\033[33m",    # Yellow for logger name and brackets
        "RESET": "\033[0m",    # Reset to default color
    }

    def __init__(self, name: str = "storm", log_file: str = "storm.log"):
        """
        Initialize the logger.

        :param name: The name of the logger.
        :param log_file: The log file name for file logging.
        """
        self.name = name
        self.log_file = log_file
        self.context: Optional[Dict[str, str]] = None
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.hasHandlers():
            self._initialize_handlers()

    def _initialize_handlers(self):
        """Initialize console and file handlers."""
        self._setup_console_handler()
        self._setup_file_handler()

    def _setup_console_handler(self):
        """Set up a console handler with colored output."""
        console_handler = logging.StreamHandler()

        # Custom formatter for colored output
        class ColoredFormatter(logging.Formatter):
            def format(self, record):
                # Get the color for the log level
                log_color = Logger.LOG_COLORS.get(record.levelname, Logger.LOG_COLORS["RESET"])

                # Apply color to the log level and message
                levelname = f"{log_color}{record.levelname}{Logger.LOG_COLORS['RESET']}"
                message = f"{log_color}{record.getMessage()}{Logger.LOG_COLORS['RESET']}"

                # Apply yellow color to the logger name with brackets
                name_color = Logger.LOG_COLORS["NAME"]
                name = f"{name_color}[{record.name}]{Logger.LOG_COLORS['RESET']}"

                # Always display the `[Storm]` part in green
                prefix_color = Logger.LOG_COLORS["INFO"]  # Using green (defined for INFO)
                prefix = f"{prefix_color}[Storm] {record.process} - {Logger.LOG_COLORS['RESET']}"

                # Replace placeholders in the format string
                formatted_message = self._fmt % {
                    "asctime": self.formatTime(record, self.datefmt),
                    "levelname": levelname,
                    "name": name,
                    "message": message,
                }
                return f"{prefix} {formatted_message}"

        console_formatter = ColoredFormatter(
            fmt="%(asctime)s %(levelname)-7s %(name)s %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S',
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def _setup_file_handler(self):
        """Set up a file handler with plain text formatting."""
        file_handler = logging.FileHandler(self.log_file)
        file_formatter = logging.Formatter(
            fmt="[Storm] %(process)d - %(asctime)s %(levelname)-7s [%(name)s] %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S',
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
            context_info = " ".join([f"{key}={value}" for key, value in self.context.items()])
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
