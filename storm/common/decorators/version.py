def Version(version):
    """
    Decorator to specify the version of a route.
    This decorator can be used to annotate a function with a version string.
    It can be used in conjunction with other decorators like @Get, @Post, etc.

    :version (str): The version string to associate with the function.
    """

    def decorator(func):
        # If the function is already wrapped (e.g., by @Get), update its metadata
        if hasattr(func, "_route"):
            func._route["version"] = version
            func.route_version = version
        else:
            # If Version is used before @Get, store it temporarily
            func.version = version
        return func

    return decorator
