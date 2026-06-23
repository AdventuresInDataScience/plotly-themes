"""plotly-themes package."""

from typing import Any

__all__ = ["__version__", "apply_theme"]

__version__ = "0.1.0"


def apply_theme(figure: Any, template: str = "plotly") -> Any:
    figure.update_layout(template=template)
    return figure
