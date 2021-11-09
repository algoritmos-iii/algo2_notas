"""
A module with some helper functions to assist in application parts
"""

import json
import dataclasses


class EnhancedJSONEncoder(json.JSONEncoder):
    """
    An enhanced JSON encoder with the ability to serialize
    dataclasses
    """

    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

def stringify(dict: dict) -> str:
    return json.dumps(dict, cls=EnhancedJSONEncoder, ensure_ascii=False)