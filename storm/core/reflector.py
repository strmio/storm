class Reflector:
    @staticmethod
    def set_metadata(target, key, value):
        """
        Attach metadata to a specific target (class, method, or function).
        """
        if not hasattr(target, "__metadata__"):
            target.__metadata__ = {}
        target.__metadata__[key] = value

    @staticmethod
    def get_metadata(key, target):
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

    @staticmethod
    def has_metadata(key, target):
        """
        Check if metadata with a specific key exists for the target.
        """
        if hasattr(target, "__metadata__"):
            return key in target.__metadata__
        return False

    @staticmethod
    def set_watermark(target, value):
        """
        Set a watermark on the target.
        """
        if not hasattr(target, "__watermark__"):
            target.__watermark__ = value
        else:
            raise ValueError("Watermark already set on target.")

    @staticmethod
    def get_watermark(target):
        """
        Get the watermark from the target.
        """
        if hasattr(target, "__watermark__"):
            return target["__watermark__"]
        return None

    @staticmethod
    def has_watermark(target):
        """
        Check if a watermark exists on the target.
        """
        return hasattr(target, "__watermark__")

    @staticmethod
    def check_watermark(target, value):
        """
        Check if the watermark is set on the target.
        """
        return hasattr(target, "__watermark__") and target["__watermark__"] == value
