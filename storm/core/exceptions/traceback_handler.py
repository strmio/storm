import asyncio
from rich.console import Console
from rich.traceback import Traceback


class TracebackHandler:
    def __init__(self):
        self.console = Console()

    async def _print_traceback_async(
        self, exception: Exception, tb=None, excecption_type=type(BaseException)
    ):
        """
        Asynchronously render and print the traceback for a given exception.

        Args:
            exception (BaseException): The exception to render and print.
        """
        if tb is None:
            tb = exception.__traceback__
        traceback = Traceback.from_exception(excecption_type, exception, tb)
        self.console.print(traceback)

    def handle_exception(
        self, exception: Exception, tb=None, excecption_type=type(BaseException)
    ):
        """
        Schedule the asynchronous traceback printing without blocking.

        Args:
            exception (BaseException): The exception to be handled.
        """
        loop = asyncio.get_event_loop()
        coro = self._print_traceback_async(exception, tb, excecption_type)

        if loop.is_running():
            loop.create_task(coro)
        else:
            asyncio.run(coro)
