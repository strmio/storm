# src/storm/core/controller.py

from storm.core.router.router import Router


class ControllerBase:
    def __init__(self, base_path="", middleware=None):
        if middleware is None:
            middleware = []
        base_path = base_path
        self.middleware = middleware
        self.router = Router()
