import json

from storm.common.exceptions.http import BadRequestException
from storm.common.pipes.pipe import Pipe


class JsonToDictPipe(Pipe):
    async def transform(self, value, metadata=None):
        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            raise BadRequestException("Invalid JSON format") from e
