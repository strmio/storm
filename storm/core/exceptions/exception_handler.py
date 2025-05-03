from storm.common.services.logger import Logger


class ExceptionHandler:
    """
    Exception handler class to handle exceptions in a consistent manner.
    """

    def __init__(self):
        self.__logger = Logger(self.__class__.__name__)

    def handle_exception(self, exception: Exception) -> None:
        """
        Handle the given exception.

        :exception: (Exception) The exception to handle.
        """
        # Log the exception or perform any other necessary actions
        self.__logger.error(exception)
