import asyncio
from rich.console import Console
from rich.traceback import Traceback


class TracebackHandler:
    def __init__(self):
        self.console = Console()

    async def _print_traceback_async(
        self, exc_value: Exception, exc_traceback=None, exc_type=type(BaseException)
    ):
        """
        Asynchronously render and print the traceback for a given exception.

        Args:
            exception (BaseException): The exception to render and print.
        """
        if exc_traceback is None:
            exc_traceback = exc_value.__traceback__
        traceback = Traceback.from_exception(exc_type, exc_value, exc_traceback)
        self.console.print(traceback)

    def handle_exception(
        self, exc_value: Exception, exc_traceback=None, exc_type=type(BaseException)
    ):
        """
        Schedule the asynchronous traceback printing without blocking.

        Args:
            exception (BaseException): The exception to be handled.
        """
        asyncio.create_task(
            self._print_traceback_async(exc_value, exc_traceback, exc_type)
        )
