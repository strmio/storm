# src/storm/common/decorators.py

def add_metadata(key, value):
    """
    A decorator that adds metadata to a function.

    :param key: The metadata key
    :param value: The metadata value
    :return: The decorated function with additional metadata
    """
    def decorator(func):
        if not hasattr(func, '_storm_metadata'):
            func._storm_metadata = {}
        func._storm_metadata[key] = value
        return func
    return decorator

def get_metadata(func, key):
    """
    Retrieves metadata from a function.

    :param func: The function from which to retrieve metadata
    :param key: The metadata key
    :return: The metadata value, or None if not found
    """
    return getattr(func, '_storm_metadata', {}).get(key)
