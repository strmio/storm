from .pipe import Pipe

class ParseIntPipe(Pipe):
    """
    Pipe to parse a value as an integer.
    """
    async def transform(self, value, metadata=None):
        try:
            return int(value)
        except ValueError:
            param_name = metadata.get("param_name", "unknown")
            raise ValueError(f"Invalid value for parameter '{param_name}': {value}. Expected an integer.")
