import os
from importlib import import_module
from types import ModuleType
from typing import Any, Dict, Optional, Tuple

# Define global variables
__globals__: Dict[Tuple[str, str], Any] = {}
DEFAULT_ALIAS = "default"


def _get_faa_globals__() -> Optional[ModuleType]:
    module_name = os.environ.get("FAA_GLOBALS", "")
    if not module_name:
        return None
    try:
        module = import_module(module_name)
    except ImportError as e:
        raise ImportError(f"Cannot import FAA_GLOBALS module {module_name}") from e
    global __globals__
    __globals__ = getattr(module, "__globals__", {})
    return module


# Get global variables from the module specified by the environment variable FAA_GLOBALS
__faa_globals__: Optional[ModuleType] = _get_faa_globals__()


def get_global(name: str, *, alias: str = DEFAULT_ALIAS) -> Any:
    """Get global variable"""
    if (name, alias) not in __globals__:
        if alias == DEFAULT_ALIAS and _exists_faa_global(name):
            return getattr(__faa_globals__, name)
        raise ValueError(f"global[{name},{alias}] not found, please call `set_global` first")
    return __globals__[(name, alias)]


def set_global(
    name: str,
    value: Any,
    *,
    alias: str = DEFAULT_ALIAS,
    overwrite: bool = False,
) -> bool:
    """Set global variable"""
    if exists_global(name, alias=alias) and not overwrite:
        return False
    __globals__[(name, alias)] = value
    return True


def exists_global(name: str, *, alias: str = DEFAULT_ALIAS) -> bool:
    """Judge whether the global variable exists"""
    return (name, alias) in __globals__ or (alias == DEFAULT_ALIAS and _exists_faa_global(name))


def _exists_faa_global(name: str) -> bool:
    """Judge whether the global variable exists in the FAA_GLOBALS module"""
    return __faa_globals__ is not None and hasattr(__faa_globals__, name)


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
