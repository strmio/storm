import atexit
import code
import os
import readline
import rlcompleter
import sys

# from storm.core.repl.repl_logger import ReplLogger
from storm.common.services.logger import Logger as ReplLogger

from .commands import help, list_controllers, list_services, reload, show_routes


class StormRepl:
    """
    REPL for Storm framework, providing an interactive shell for developers
    to interact with their Storm applications.
    """

    def __init__(self, app):
        self.app = app
        self.logger = ReplLogger(self.__class__.__name__)
        self.context = {
            "app": app,
            "help": help,
            "list_services": lambda: list_services(app),
            "list_controllers": lambda: list_controllers(app),
            "reload": lambda: reload(app),
            "show_routes": lambda: show_routes(app),
        }
        self.banner = "Storm REPL - Type 'help()' for a list of available commands."
        # self.setup_history()
        self.setup_autocompletion()
        sys.ps1 = "strm $ "

    def setup_history(self):
        """
        Sets up command history for the REPL.
        """
        self.logger.info("Setting up REPL history")
        history_file = os.path.expanduser("~/.storm_repl_history")
        try:
            readline.read_history_file(history_file)
        except FileNotFoundError:
            open(history_file, "wb").close()
        atexit.register(readline.write_history_file, history_file)

    def setup_autocompletion(self):
        """
        Enables autocompletion in the REPL using rlcompleter.
        """
        readline.set_completer(rlcompleter.Completer(self.context).complete)
        readline.parse_and_bind("tab: complete")

    def start(self):
        """
        Starts the interactive REPL session.
        """
        self.logger.info("Starting REPL session")
        code.interact(banner=self.banner, local=self.context)


def start_repl(app):
    """
    Starts the Storm REPL with the given application context\n

    :param app: An instance of the Storm application.
    """
    repl = StormRepl(app)
    repl.start()
