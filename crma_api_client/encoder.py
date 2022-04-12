"""Contains JSON encoders"""

from datetime import date, datetime
from enum import Enum
import functools
import json
from typing import Any


class CommonEncoder(json.JSONEncoder):
    """Custom JSON encoder to serialize commonly-used objects"""

    def _encode(self, obj: Any) -> Any:
        """Method to handle serialization of custom objects

        Defaults to stringifying the object.

        Args:
            obj: Node in the data structure to serialize

        Returns:
            transformed data structure to include in final JSON output

        """
        if isinstance(obj, (str, bool, int, float)):
            return obj
        elif isinstance(obj, bytes):
            return obj.decode()
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return str(obj)
        elif isinstance(obj, set):
            return {self._encode(key): True for key in obj}
        elif isinstance(obj, Enum):
            return obj.value

        for method in ("to_dict", "dict"):
            to_dict_method = getattr(obj, method, None)
            if callable(to_dict_method):
                obj = to_dict_method()
                break

        if isinstance(obj, dict):
            return {
                self._encode(key): self._encode(value) for key, value in obj.items()
            }
        elif isinstance(obj, (list, tuple)):
            return [self._encode(value) for value in obj]

        return str(obj)

    def encode(self, obj: Any) -> str:
        """Method to handle serialization of objects

        Proxies to custom internal method.

        Args:
            obj: Node in the data structure to serialize

        Returns:
            serialized JSON output

        """
        return super().encode(self._encode(obj))


#: Function to serialize a data structure using the CommonEncoder
json_dumps_common = functools.partial(json.dumps, cls=CommonEncoder)
