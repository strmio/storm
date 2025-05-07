# storm/decorators/version.py
from storm.common.constants import VERSION_METADATA
from storm.common.utils.shared import deduplicate_preserve_order
from storm.core.di.reflect import Reflect


class Version:
    """
    Method decorator that assigns version metadata to a route handler.

    Equivalent to NestJS's @Version()

    :param version: A version string, or list of version strings
    """

    def __init__(self, version):
        if isinstance(version, list):
            self.version = deduplicate_preserve_order(version)  # remove duplicates
        else:
            self.version = version

    def __call__(self, func):
        Reflect.define_metadata(VERSION_METADATA, self.version, func)
        return func
