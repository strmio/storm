import re
from storm.common.pipes.pipe import Pipe

class EmailValidationPipe(Pipe):
    EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    async def transform(self, value, metadata=None):
        if not re.match(self.EMAIL_REGEX, value):
            raise ValueError("Invalid email address")
        return value
