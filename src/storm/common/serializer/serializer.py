class Serializer:
    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)

    @classmethod
    def from_dict(cls, data):
        """
        Validate and deserialize the incoming data from a dictionary.
        """
        obj = cls(**data)
        obj.validate()
        return obj

    def validate(self):
        """
        Custom validation logic can go here (e.g., required fields).
        This should be overridden in child classes.
        """
        pass

    def to_dict(self):
        """
        Serialize the object to a dictionary.
        """
        return {key: getattr(self, key) for key in self.__annotations__.keys()}
