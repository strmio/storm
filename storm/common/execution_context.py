from contextvars import ContextVar

class ExecutionContext:
    """
    A class-based implementation to manage execution context using ContextVar.
    """

    def __init__(self):
        # Initialize the ContextVar to store the context for each request
        self._context_var = ContextVar('execution_context', default={})

    def set(self, data: dict):
        """
        Set the execution context for the current request.

        :param data: A dictionary containing the context data.
        """
        self._context_var.set(data)

    def get(self) -> dict:
        """
        Get the execution context for the current request.

        :return: A dictionary containing the context data.
        """
        return self._context_var.get()

    def clear(self):
        """
        Clear the execution context.
        """
        self._context_var.set({})


# Create a global instance of ExecutionContext for reuse
execution_context = ExecutionContext()
