class Reflector:
    def __init__(self):
        # Internal storage for metadata
        self._metadata = {}

    def set_metadata(self, key, value, target):
        """
        Attach metadata to a specific target (class, method, or function).
        """
        if not hasattr(target, "__metadata__"):
            target.__metadata__ = {}
        target.__metadata__[key] = value

    def get_metadata(self, key, target):
        """
        Retrieve metadata for a specific key from a target.
        """
        if hasattr(target, "__metadata__") and key in target.__metadata__:
            return target.__metadata__[key]
        return None

    def get_all_metadata(self, target):
        """
        Retrieve all metadata for a specific target.
        """
        if hasattr(target, "__metadata__"):
            return target.__metadata__
        return {}

    def has_metadata(self, key, target):
        """
        Check if metadata with a specific key exists for the target.
        """
        if hasattr(target, "__metadata__"):
            return key in target.__metadata__
        return False
