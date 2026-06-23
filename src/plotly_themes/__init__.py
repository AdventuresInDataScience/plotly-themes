"""plotly-themes: a collection of fun, ready-to-use visual themes for Plotly.

Importing this package patches Plotly by registering every bundled theme into
``plotly.io.templates``. After import you can do, for example::

    import plotly_themes  # noqa: F401  (registers all themes on import)
    import plotly.io as pio

    pio.templates.default = "matrix"

Each theme lives in its own module under ``plotly_themes.themes``. To add a new
theme, drop a new file in that package exposing two module-level names:

    NAME = "my_theme"                      # the key used in pio.templates
    TEMPLATE = go.layout.Template(...)     # the template itself

It will be discovered and registered automatically.
"""

from __future__ import annotations

import importlib
import pkgutil
from typing import List

import plotly.io as pio

from . import themes

__all__ = ["register_all", "registered_themes"]

_REGISTERED: List[str] = []


def register_all() -> List[str]:
    """Discover every theme module and register it into ``pio.templates``.

    Returns the list of registered theme names. Safe to call more than once.
    """
    _REGISTERED.clear()
    for module_info in pkgutil.iter_modules(themes.__path__):
        if module_info.name.startswith("_"):
            continue
        module = importlib.import_module(f"{themes.__name__}.{module_info.name}")
        name = getattr(module, "NAME", None)
        template = getattr(module, "TEMPLATE", None)
        if name is None or template is None:
            continue
        pio.templates[name] = template
        _REGISTERED.append(name)
    return list(_REGISTERED)


def registered_themes() -> List[str]:
    """Return the names of themes registered by this package."""
    return list(_REGISTERED)


# Patch Plotly on import.
register_all()
