from storm.core.pipes import Pipe

class ValidateNonEmptyPipe(Pipe):
    async def transform(self, value, metadata=None):
        if not value or not isinstance(value, str):
            raise ValueError("Value must be a non-empty string")
        return value
