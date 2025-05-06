from contextvars import ContextVar

from storm.common.decorators.injectable import Injectable

# from storm.core.adapters.http_response import HttpResponse


@Injectable()
class ExecutionContext:
    """
    A class-based implementation to manage execution context using ContextVar.
    """

    _context_var: ContextVar = ContextVar("execution_context", default=None)

    @classmethod
    def set(cls, data):
        """
        Set the execution context for the current request.

        :param data: The context data to set (can be of any type).
        """
        cls._context_var.set(data)

    @classmethod
    def get(cls):
        """
        Get the execution context for the current request.

        :return: The context data (can be of any type) or None if not set.
        """
        return cls._context_var.get()

    @classmethod
    def clear(cls):
        """
        Clear the execution context.
        """
        cls._context_var.set(None)

    @classmethod
    def set_request(cls, request):
        """
        Set the request context data.

        :param request: Request data (can be of any type).
        """
        context = cls.get() or {}
        if not isinstance(context, dict):
            raise TypeError("Context must be a dictionary to set request data.")
        context["request"] = request
        cls.set(context)

    @classmethod
    def get_request(cls):
        """
        Get the request context data.

        :return: The request data or None if not set.
        """
        context = cls.get()
        if isinstance(context, dict):
            return context.get("request", {})
        return None

    @classmethod
    def set_response(cls, response):
        """
        Set the response context data.

        :param response: Response data (can be of any type).
        """
        context = cls.get() or {}
        if not isinstance(context, dict):
            raise TypeError("Context must be a dictionary to set response data.")
        context["response"] = response
        cls.set(context)

    @classmethod
    def get_response(cls):
        """
        Get the response context data.

        :return: The response data or None if not set.
        """
        context = cls.get()
        if isinstance(context, dict):
            return context.get("response", {})
        return None

    @classmethod
    def set_context(cls, key: str, value):
        """
        Set a generic context value by key.

        :param key: The key for the context data.
        :param value: The value to store.
        """
        context = cls.get() or {}
        if not isinstance(context, dict):
            raise TypeError("Context must be a dictionary to set key-value pairs.")
        context[key] = value
        cls.set(context)

    @classmethod
    def get_context(cls, key: str, default=None):
        """
        Get a generic context value by key.

        :param key: The key for the context data.
        :param default: The default value to return if the key is not found.
        :return: The context value for the given key, or the default value.
        """
        context = cls.get()
        if isinstance(context, dict):
            return context.get(key, default)
        return default
