class LogColor:
    """
    A class to encapsulate ANSI escape codes for log colors.
    """

    DEBUG = "\033[1;35m"  # Bright Magenta
    INFO = "\033[1;32m"  # Bright Green
    WARNING = "\033[1;33m"  # Bright Yellow
    ERROR = "\033[1;31m"  # Bright Red
    CRITICAL = "\033[1;31m"  # Bright Red
    NAME = "\033[1;33m"  # Bright Yellow (for module names or [name])
    TIMESTAMP = "\033[1;37m"  # Bright White
    HEADER = "\033[1;32m"  # Bright Green (e.g., [Storm])
    METRIC_LABEL = "\033[1;36m"  # Bright Cyan
    RESET = "\033[0m"


class LogColorNoBold:
    """
    A class to encapsulate ANSI escape codes for log colors without bold formatting.
    """

    DEBUG = "\033[35m"  # Magenta
    INFO = "\033[32m"  # Green
    WARNING = "\033[33m"  # Yellow
    ERROR = "\033[31m"  # Red
    CRITICAL = "\033[31m"  # Red
    NAME = "\033[33m"  # Yellow (for module names or [name])
    TIMESTAMP = "\033[37m"  # White
    HEADER = "\033[32m"  # Green (e.g., [Storm])
    METRIC_LABEL = "\033[36m"  # Cyan
    RESET = "\033[0m"
