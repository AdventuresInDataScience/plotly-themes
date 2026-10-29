"""Visual effects that go beyond what a Plotly template can express.

A template only sets *per-trace defaults* — it cannot add new traces. Effects
like a neon "glow" need a wider, translucent copy of each line drawn underneath
the real one, so they are implemented here as figure post-processors.
"""

from __future__ import annotations

from typing import List

import plotly.colors as pc
import plotly.graph_objects as go

__all__ = ["add_glow"]

# Plotly's default qualitative palette, used to resolve a trace's colour when it
# relies on the active colourway rather than an explicit one.
_DEFAULT_COLORWAY = pc.qualitative.Plotly

_LINE_TRACE_TYPES = ("scatter", "scattergl")


def _to_rgba(color: str, alpha: float) -> str:
    """Best-effort conversion of a CSS/hex/rgb colour string to an ``rgba(...)``.

    Falls back to returning the original colour unchanged if it can't be parsed
    (the glow then still reads as a wider underlay, just without added alpha).
    """
    if not isinstance(color, str):
        return color
    c = color.strip()
    try:
        if c.startswith("#"):
            r, g, b = pc.hex_to_rgb(c)
            return f"rgba({r}, {g}, {b}, {alpha})"
        if c.startswith("rgb(") or c.startswith("rgba("):
            nums = c[c.index("(") + 1 : c.index(")")].split(",")
            r, g, b = (float(n) for n in nums[:3])
            return f"rgba({r:g}, {g:g}, {b:g}, {alpha})"
    except (ValueError, IndexError):
        pass
    return c


def _draws_line(trace) -> bool:
    if trace.type not in _LINE_TRACE_TYPES:
        return False
    mode = trace.mode
    # Default scatter mode draws lines unless markers/text were requested instead.
    if mode is None:
        return True
    return "lines" in mode


def add_glow(
    fig: go.Figure,
    *,
    layers: int = 4,
    width_growth: float = 4.0,
    max_opacity: float = 0.18,
    colorway: List[str] | None = None,
) -> go.Figure:
    """Add a soft neon/lightsaber glow beneath every line trace, in place.

    For each line trace, several progressively wider and fainter copies of the
    line are inserted underneath it, producing a bloom around the bright core.

    Args:
        fig: the figure to modify (also returned, for chaining).
        layers: number of glow copies per line (more = smoother falloff).
        width_growth: how much wider each successive glow layer gets, in px.
        max_opacity: opacity of the innermost (brightest) glow layer; outer
            layers fade towards transparent.
        colorway: palette used to resolve colours for traces that don't set
            their own line colour. Defaults to the figure's template colourway,
            then Plotly's default palette.

    Returns:
        The same figure, with glow traces prepended so they render underneath.
    """
    if colorway is None:
        tpl = fig.layout.template
        colorway = list(
            (tpl.layout.colorway if tpl and tpl.layout else None)
            or _DEFAULT_COLORWAY
        )

    glow_traces: List[go.Scatter] = []
    # Plotly cycles the colourway across *all* traces in order, so track the
    # index over every trace (bars included) — not just the line traces — to
    # resolve the colour each line will actually be drawn in.
    color_index = 0
    for trace in fig.data:
        if not _draws_line(trace):
            color_index += 1
            continue
        # Resolve and pin the trace's colour so the glow matches exactly even
        # after we reorder the trace list.
        color = trace.line.color
        if color is None:
            color = colorway[color_index % len(colorway)]
            trace.line.color = color
        color_index += 1

        base_width = trace.line.width if trace.line.width is not None else 2
        # Build from widest/faintest to narrowest/brightest so the bright core
        # sits closest to the real line.
        for layer in range(layers, 0, -1):
            opacity = max_opacity * layer / layers
            width = base_width + width_growth * layer
            glow_traces.append(
                go.Scatter(
                    x=trace.x,
                    y=trace.y,
                    mode="lines",
                    line={
                        "color": _to_rgba(color, opacity),
                        "width": width,
                        "shape": trace.line.shape,
                        "smoothing": trace.line.smoothing,
                    },
                    hoverinfo="skip",
                    showlegend=False,
                    legendgroup=trace.legendgroup,
                    xaxis=trace.xaxis,
                    yaxis=trace.yaxis,
                )
            )

    if glow_traces:
        # ``fig.data`` can't be assigned new traces directly (only reordered), so
        # append the glow traces and then move them in front of the originals.
        n_original = len(fig.data)
        fig.add_traces(glow_traces)
        reordered = list(fig.data[n_original:]) + list(fig.data[:n_original])
        fig.data = reordered
    return fig
