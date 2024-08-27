class Pipe:
    """
    Base class for all pipes. Pipes are used to transform or validate data before it reaches the controller.
    """
    async def transform(self, value, metadata=None):
        """
        Transform or validate the given value.
        :param value: The value to be transformed or validated.
        :param metadata: Additional metadata that might be needed for transformation.
        :return: The transformed or validated value.
        """
        raise NotImplementedError("Pipes must implement the transform method.")
