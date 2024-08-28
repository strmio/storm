class Guard:
    """
    Base class for all guards. Guards are used to determine if a request should proceed to the controller's action.
    """
    async def can_activate(self, request, metadata=None):
        """
        Determine whether the request should proceed.
        :param request: The incoming request object.
        :param metadata: Additional metadata that might be needed for the guard.
        :return: True if the request is allowed to proceed, False otherwise.
        """
        raise NotImplementedError("Guards must implement the can_activate method.")
