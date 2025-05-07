import code
import selectors
import sys
import threading

from storm.core.services.system_monitor import SystemMonitor


class ReplManager:
    """
    A class to manage the REPL (Read-Eval-Print Loop) lifecycle for the Storm application.

    Attributes:
        app: The main StormApplication instance.
        repl_thread: The thread responsible for listening to the Enter key.
        shutdown_event: An event to signal the listener to stop.
    """

    def __init__(self, app, system_monitor: SystemMonitor | None = None, prompt=">>>"):
        """
        Initialize the REPL Manager.

        :param app: The main StormApplication instance.
        """
        self.app = app
        self.repl_thread = None
        self.system_monitor = system_monitor
        self.shutdown_event = threading.Event()
        self.selector = selectors.DefaultSelector()
        self.prompt = prompt
        self.banner = "Welcome to the REPL (Type 'ctrl-D' to return to the app)."

    def start(self):
        """
        Start the REPL listener thread.
        """
        self.repl_thread = threading.Thread(target=self._repl_listener, daemon=True)
        self.repl_thread.start()

    def shutdown(self):
        """
        Signal the REPL manager to stop and wait for the thread to finish.
        """
        self.shutdown_event.set()
        if self.repl_thread and self.repl_thread.is_alive():
            self.repl_thread.join()

    def _repl_listener(self):
        """
        Continuously listen for the Enter key and open the REPL.
        """
        self.selector.register(sys.stdin, selectors.EVENT_READ)

        while not self.shutdown_event.is_set():
            try:
                events = self.selector.select(timeout=1)  # Check every second for input
                for key, _ in events:
                    if key.fileobj == sys.stdin:
                        input_line = sys.stdin.readline().strip()
                        if input_line == "":  # Empty line means Enter was pressed
                            if self.system_monitor:
                                self.system_monitor.stop()
                            self._open_repl()
            except Exception as e:
                self.app.logger.error(f"Error in REPL listener: {e}")
            finally:
                if self.shutdown_event.is_set():
                    ...

        self.selector.close()

    def _open_repl(self):
        """
        Open an interactive REPL in the terminal.
        """
        self.app.logger.info("Opening REPL. Type 'exit()' to return to the app.")
        try:
            # Launch Python interactive shell with access to the app context
            local_context = {
                "app": self.app,
                "modules": self.app.modules,
                "__prompt__": self.prompt,
            }
            console = code.InteractiveConsole(locals=local_context)
            console.interact(banner=self.banner, exitmsg=None)
        except Exception as e:
            self.app.logger.error(f"Error in REPL: {e}")
        finally:
            self.app.logger.info("REPL closed.")
            self.system_monitor.continue_() if self.system_monitor else None
