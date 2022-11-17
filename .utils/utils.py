from typing import Any


def val_of_key(obj: dict, key_path: list[str], fallback: Any) -> Any:
    curObj = obj
    while len(key_path) > 0:
        try:
            curObj = curObj[key_path.pop(0)]
        except KeyError:
            return fallback
    return curObj