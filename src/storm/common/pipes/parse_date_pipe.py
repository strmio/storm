import datetime
from .pipe import Pipe

class ParseDatePipe(Pipe):
    """
    Pipe to parse and validate a value as a date.
    """
    def __init__(self, date_format="%Y-%m-%d"):
        """
        :param date_format: The date format to parse (default: "%Y-%m-%d").
        """
        self.date_format = date_format

    async def transform(self, value, metadata=None):
        try:
            return datetime.strptime(value, self.date_format)
        except ValueError:
            raise ValueError(f"Invalid date value: {value}. Expected format: {self.date_format}")
