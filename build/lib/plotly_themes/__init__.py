"""plotly-themes package."""

from typing import Any

__all__ = ["__version__", "apply_theme"]

__version__ = "0.1.0"


def apply_theme(figure: Any, template: str = "plotly") -> None:
    """Apply a Plotly template name to a figure in-place.

    Parameters
    ----------
    figure:
        A Plotly-compatible figure object that exposes ``update_layout``.
    template:
        A valid Plotly template name, such as ``plotly`` or ``plotly_dark``.
    """
    figure.update_layout(template=template)
