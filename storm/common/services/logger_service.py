import datetime
import threading
from typing import List, Optional, Callable, Any

from storm.common import Injectable

LogLevel = str
LOG_LEVELS: List[LogLevel] = ["log", "error", "warn", "debug", "verbose", "fatal"]


def current_timestamp() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class LogBufferRecord:
    def __init__(self, method: Callable, args: tuple):
        self.method = method
        self.args = args


class LoggerService:
    def log(self, message: Any, *optional_params: Any):
        pass

    def error(self, message: Any, *optional_params: Any):
        pass

    def warn(self, message: Any, *optional_params: Any):
        pass

    def debug(self, message: Any, *optional_params: Any):
        pass

    def verbose(self, message: Any, *optional_params: Any):
        pass

    def fatal(self, message: Any, *optional_params: Any):
        pass

    def set_log_levels(self, levels: List[LogLevel]):
        pass


class ConsoleLogger(LoggerService):
    def __init__(
        self,
        context: Optional[str] = None,
        timestamp: bool = False,
        log_levels: Optional[List[LogLevel]] = None,
    ):
        self.context = context
        self.timestamp = timestamp
        self.log_levels = log_levels or LOG_LEVELS

    def _format_message(self, level: str, message: Any, *optional_params: Any) -> str:
        prefix = f"[{level.upper()}]"
        timestamp = f"[{current_timestamp()}]" if self.timestamp else ""
        context = f"[{self.context}]" if self.context else ""
        return f"{timestamp} {prefix} {context} {message} {' '.join(map(str, optional_params))}".strip()

    def _log(self, level: str, message: Any, *optional_params: Any):
        if level in self.log_levels:
            print(self._format_message(level, message, *optional_params))

    def log(self, message: Any, *optional_params: Any):
        self._log("log", message, *optional_params)

    def error(self, message: Any, *optional_params: Any):
        self._log("error", message, *optional_params)

    def warn(self, message: Any, *optional_params: Any):
        self._log("warn", message, *optional_params)

    def debug(self, message: Any, *optional_params: Any):
        self._log("debug", message, *optional_params)

    def verbose(self, message: Any, *optional_params: Any):
        self._log("verbose", message, *optional_params)

    def fatal(self, message: Any, *optional_params: Any):
        self._log("fatal", message, *optional_params)

    def set_log_levels(self, levels: List[LogLevel]):
        self.log_levels = levels


@Injectable()
class Logger(LoggerService):
    _log_buffer: List[LogBufferRecord] = []
    _static_instance: LoggerService = ConsoleLogger()
    _log_levels: List[LogLevel] = LOG_LEVELS
    _buffer_lock = threading.Lock()
    _is_buffering: bool = False

    def __init__(self, context: Optional[str] = None, timestamp: bool = False):
        self.local_instance = ConsoleLogger(context, timestamp, Logger._log_levels)

    @classmethod
    def attach_buffer(cls):
        with cls._buffer_lock:
            cls._is_buffering = True

    @classmethod
    def detach_buffer(cls):
        with cls._buffer_lock:
            cls._is_buffering = False

    @classmethod
    def flush(cls):
        with cls._buffer_lock:
            cls._is_buffering = False
            for record in cls._log_buffer:
                record.method(*record.args)
            cls._log_buffer.clear()

    def _buffer_or_log(self, method: Callable, *args: Any):
        if Logger._is_buffering:
            with Logger._buffer_lock:
                Logger._log_buffer.append(LogBufferRecord(method, args))
        else:
            method(*args)

    def log(self, message: Any, *optional_params: Any):
        self._buffer_or_log(self.local_instance.log, message, *optional_params)

    def error(self, message: Any, *optional_params: Any):
        self._buffer_or_log(self.local_instance.error, message, *optional_params)

    def warn(self, message: Any, *optional_params: Any):
        self._buffer_or_log(self.local_instance.warn, message, *optional_params)

    def debug(self, message: Any, *optional_params: Any):
        self._buffer_or_log(self.local_instance.debug, message, *optional_params)

    def verbose(self, message: Any, *optional_params: Any):
        self._buffer_or_log(self.local_instance.verbose, message, *optional_params)

    def fatal(self, message: Any, *optional_params: Any):
        self._buffer_or_log(self.local_instance.fatal, message, *optional_params)

    @classmethod
    def override_logger(cls, logger: LoggerService):
        cls._static_instance = logger

    @classmethod
    def is_level_enabled(cls, level: LogLevel) -> bool:
        return level in cls._log_levels
