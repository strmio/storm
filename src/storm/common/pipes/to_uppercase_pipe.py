from storm.common.pipes.pipe import Pipe

class ToUpperCasePipe(Pipe):
    async def transform(self, value, metadata=None):
        if isinstance(value, str):
            return value.upper()
        return value
