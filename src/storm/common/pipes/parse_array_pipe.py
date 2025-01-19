from .pipe import Pipe


class ParseArrayPipe(Pipe):
    """
    Pipe to parse and validate a value as an array of items.
    """
    def __init__(self, delimiter=",", item_pipe=None):
        """
        :param delimiter: The delimiter to split the array string.
        :param item_pipe: An optional pipe to apply to each item in the array.
        """
        self.delimiter = delimiter
        self.item_pipe = item_pipe

    async def transform(self, value, metadata=None):
        try:
            items = value.split(self.delimiter)
            if self.item_pipe:
                items = [await self.item_pipe.transform(item) for item in items]
            return items
        except Exception as e:
            raise ValueError(f"Invalid array value: {value}. {str(e)}")
