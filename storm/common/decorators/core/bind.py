# storm/decorators/bind.py

from typing import Callable


class Bind:
    """
    Simulates parameter decorators by calling provided decorators with
    (target, method name, parameter index) at method definition time.

    :param decorators: A list of simulated parameter decorators
    """

    def __init__(self, *decorators: Callable):
        self.decorators = decorators

    def __call__(self, method: Callable) -> Callable:
        method_name = method.__name__
        target = method

        for index, decorator in enumerate(self.decorators):
            decorator(target, method_name, index)

        return method
