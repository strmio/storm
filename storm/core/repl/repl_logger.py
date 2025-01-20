import logging

class ReplLogger:
    def __init__(self, name='REPL'):
        """
        Initializes the REPL logger with a default name and console handler.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Console handler with colored output
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(self._get_formatter())

        self.logger.addHandler(console_handler)

    def _get_formatter(self):
        """
        Returns a custom formatter for the REPL logs.
        """
        return logging.Formatter(
            "\033[1;34m%(asctime)s\033[0m - \033[1;32m%(name)s\033[0m - \033[1;33m%(levelname)s\033[0m - %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def critical(self, message):
        self.logger.critical(message)
