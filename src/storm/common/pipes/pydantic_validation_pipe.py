from pydantic import BaseModel, ValidationError

from storm.common.exceptions.http import BadRequestException
from .pipe import Pipe

class PydanticValidationPipe(Pipe):
    """
    Pipe to validate and transform input data using Pydantic models.
    """
    def __init__(self, model: BaseModel):
        """
        :param model: A Pydantic model class to validate the input data.
        """
        self.model = model

    async def transform(self, value, metadata=None):
        """
        Validate and transform the input data using the provided Pydantic model.
        :param value: The value to validate and transform.
        :param metadata: Optional metadata for additional context.
        :return: The validated and transformed data.
        :raises ValueError: If validation fails.
        """
        try:
            return self.model.model_validate(value)
        except ValidationError as e:
            raise BadRequestException(f"Pydantic validation error: {e}")
