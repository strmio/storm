from contextvars import ContextVar
from storm.common.decorators.injectable import Injectable


@Injectable()
class ExecutionContext:
    """
    A class-based implementation to manage execution context using ContextVar.
    """

    def __init__(self):
        # Initialize the ContextVar to store the context for each request
        self._context_var = ContextVar("execution_context", default=None)

    def set(self, data):
        """
        Set the execution context for the current request.

        :param data: The context data to set (can be of any type).
        """
        self._context_var.set(data)

    def get(self):
        """
        Get the execution context for the current request.

        :return: The context data (can be of any type) or None if not set.
        """
        return self._context_var.get()

    def clear(self):
        """
        Clear the execution context.
        """
        self._context_var.set(None)

    def set_request(self, request):
        """
        Set the request context data.

        :param request: Request data (can be of any type).
        """
        context = self.get() or {}
        if not isinstance(context, dict):
            raise TypeError("Context must be a dictionary to set request data.")
        context["request"] = request
        self.set(context)

    def get_request(self):
        """
        Get the request context data.

        :return: The request data or None if not set.
        """
        context = self.get()
        if isinstance(context, dict):
            return context.get("request", {})
        return None

    def set_response(self, response):
        """
        Set the response context data.

        :param response: Response data (can be of any type).
        """
        context = self.get() or {}
        if not isinstance(context, dict):
            raise TypeError("Context must be a dictionary to set response data.")
        context["response"] = response
        self.set(context)

    def get_response(self):
        """
        Get the response context data.

        :return: The response data or None if not set.
        """
        context = self.get()
        if isinstance(context, dict):
            return context.get("response", {})
        return None

    def set_context(self, key: str, value):
        """
        Set a generic context value by key.

        :param key: The key for the context data.
        :param value: The value to store.
        """
        context = self.get() or {}
        if not isinstance(context, dict):
            raise TypeError("Context must be a dictionary to set key-value pairs.")
        context[key] = value
        self.set(context)

    def get_context(self, key: str, default=None):
        """
        Get a generic context value by key.

        :param key: The key for the context data.
        :param default: The default value to return if the key is not found.
        :return: The context value for the given key, or the default value.
        """
        context = self.get()
        if isinstance(context, dict):
            return context.get(key, default)
        return default


# Create a global instance of ExecutionContext for reuse
execution_context = ExecutionContext()
