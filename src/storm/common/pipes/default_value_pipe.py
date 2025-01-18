from .pipe import Pipe

class DefaultValuePipe(Pipe):
    """
    Pipe to assign a default value if the input is None.
    """
    def __init__(self, default_value):
        """
        :param default_value: The default value to use if the input is None.
        """
        self.default_value = default_value

    async def transform(self, value, metadata=None):
        return value if value is not None else self.default_value
