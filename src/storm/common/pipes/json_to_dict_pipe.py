import json
from storm.core.pipes import Pipe

class JsonToDictPipe(Pipe):
    async def transform(self, value, metadata=None):
        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON format") from e
