# reflect.py

from typing import Any, Dict, List, Optional, Union
from weakref import WeakKeyDictionary

MetadataKey = Any
MetadataValue = Any
PropertyKey = Union[str, int]


class Reflect:
    """
    Reflect-metadata API implementation in Python, mimicking TypeScript's reflect-metadata.
    """

    _metadata: "WeakKeyDictionary[object, Dict[str, Dict[MetadataKey, MetadataValue]]]" = WeakKeyDictionary()

    @classmethod
    def _get_target_metadata(cls, target: object, create: bool = False) -> Dict:
        if target not in cls._metadata:
            if not create:
                return {}
            cls._metadata[target] = {}
        return cls._metadata[target]

    @classmethod
    def define_metadata(
        cls,
        metadata_key: MetadataKey,
        metadata_value: MetadataValue,
        target: object,
        property_key: Optional[PropertyKey] = None,
    ) -> None:
        """
        Define a metadata entry on the target or its property.

        :param metadata_key: The key for the metadata.
        :param metadata_value: The value to store.
        :param target: The target class or object.
        :param property_key: Optional property key of the target.
        """
        target_meta = cls._get_target_metadata(target, create=True)
        key = str(property_key) if property_key is not None else "__class__"
        if key not in target_meta:
            target_meta[key] = {}
        target_meta[key][metadata_key] = metadata_value

    @classmethod
    def has_metadata(
        cls,
        metadata_key: MetadataKey,
        target: object,
        property_key: Optional[PropertyKey] = None,
    ) -> bool:
        """
        Check if metadata exists for the given key on the target or property.

        :param metadata_key: The key to check.
        :param target: The target class or object.
        :param property_key: Optional property key of the target.
        :return: True if metadata exists.
        """
        key = str(property_key) if property_key is not None else "__class__"
        meta = cls._get_target_metadata(target)
        return key in meta and metadata_key in meta[key]

    @classmethod
    def get_metadata(
        cls,
        metadata_key: MetadataKey,
        target: object,
        property_key: Optional[PropertyKey] = None,
    ) -> Optional[MetadataValue]:
        """
        Retrieve metadata for the given key on the target or property.

        :param metadata_key: The key to retrieve.
        :param target: The target class or object.
        :param property_key: Optional property key of the target.
        :return: Metadata value or None.
        """
        key = str(property_key) if property_key is not None else "__class__"
        meta = cls._get_target_metadata(target)
        return meta.get(key, {}).get(metadata_key)

    @classmethod
    def get_metadata_keys(cls, target: object, property_key: Optional[PropertyKey] = None) -> List[MetadataKey]:
        """
        Get all metadata keys for the target or its property.

        :param target: The target class or object.
        :param property_key: Optional property key of the target.
        :return: List of metadata keys.
        """
        key = str(property_key) if property_key is not None else "__class__"
        meta = cls._get_target_metadata(target)
        return list(meta.get(key, {}).keys())

    @classmethod
    def delete_metadata(
        cls,
        metadata_key: MetadataKey,
        target: object,
        property_key: Optional[PropertyKey] = None,
    ) -> bool:
        """
        Delete metadata for the given key on the target or its property.

        :param metadata_key: The key to delete.
        :param target: The target class or object.
        :param property_key: Optional property key of the target.
        :return: True if metadata was found and deleted.
        """
        key = str(property_key) if property_key is not None else "__class__"
        meta = cls._get_target_metadata(target)
        if key in meta and metadata_key in meta[key]:
            del meta[key][metadata_key]
            return True
        return False

    @classmethod
    def clear(cls) -> None:
        """
        Clear all stored metadata (for testing or reset).
        """
        cls._metadata.clear()
