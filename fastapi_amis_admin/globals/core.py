from typing import Any, Dict, Tuple

# Define global variables
__globals__: Dict[Tuple[str, str], Any] = {}


def get_global(name: str, *, alias: str = "default") -> Any:
    """Get global variable"""
    if (name, alias) not in __globals__:
        raise ValueError(f"global[{name},{alias}] not found, please call `set_global` first")
    return __globals__[(name, alias)]


def set_global(name: str, value: Any, *, alias: str = "default") -> None:
    """Set global variable"""
    if (name, alias) in __globals__:
        raise ValueError(f"global[{name},{alias}] already exists")
    __globals__[(name, alias)] = value


def exists_global(name: str, *, alias: str = "default") -> bool:
    """Judge whether the global variable exists"""
    return (name, alias) in __globals__


def remove_global(*, name: str = None, alias: str = None) -> None:
    """Remove global variable"""
    if name is None and alias is None:
        __globals__.clear()
    elif name is not None and alias is None:
        for key in list(__globals__.keys()):
            if key[0] == name:
                __globals__.pop(key)
    elif name is None and alias is not None:
        for key in list(__globals__.keys()):
            if key[1] == alias:
                __globals__.pop(key)
    else:
        __globals__.pop((name, alias), None)
