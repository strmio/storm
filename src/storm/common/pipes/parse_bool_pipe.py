from storm.common.pipes.pipe import Pipe


class ParseBoolPipe(Pipe):
    """
    Pipe to parse and validate a value as a boolean.
    """
    async def transform(self, value, metadata=None):
        truthy = {"true", "1", "yes", "on"}
        falsy = {"false", "0", "no", "off"}
        str_value = str(value).strip().lower()
        if str_value in truthy:
            return True
        elif str_value in falsy:
            return False
        raise ValueError(f"Invalid boolean value: {value}")
