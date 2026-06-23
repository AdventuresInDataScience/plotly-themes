"""Extend a theme so non-cartesian subplots match its 2D look.

A Plotly template's ``layout.paper_bgcolor``/``plot_bgcolor``/``colorway`` cover
the figure canvas and all 2D cartesian charts (bar, line, scatter, heatmap, box,
violin, histogram, pie, sunburst, …). But 3D (``scene``), polar, geo and ternary
subplots carry their *own* background and axis colours that don't inherit from
the 2D ones — so on, say, a dark theme a 3D or radar chart would otherwise show
a default light background.

Rather than hand-write that for every theme, we derive it from the colours the
theme already defines and fill in any values it hasn't set itself.
"""

from __future__ import annotations

import plotly.graph_objects as go


def _axis_color(axis, attr):
    value = getattr(axis, attr, None)
    return value


def enrich_subplots(template: go.layout.Template) -> go.layout.Template:
    """Fill in scene/polar/geo/ternary styling from the template's 2D colours.

    Only applied when the theme sets a background colour (i.e. has an opinion to
    propagate); light/unstyled themes keep Plotly's sensible defaults. Existing
    explicit values on the template are preserved.
    """
    lay = template.layout
    paper = lay.paper_bgcolor
    plot = lay.plot_bgcolor or paper
    if plot is None:
        return template  # theme doesn't set a background; leave defaults alone

    xax = lay.xaxis
    grid = _axis_color(xax, "gridcolor")
    line = _axis_color(xax, "linecolor")
    text = None
    if xax.tickfont is not None:
        text = xax.tickfont.color
    if text is None and lay.font is not None:
        text = lay.font.color

    axis3d = {
        "backgroundcolor": plot,
        "showbackground": True,
        "gridcolor": grid,
        "zerolinecolor": grid,
        "color": text,
    }
    polar_axis = {"gridcolor": grid, "linecolor": line, "color": text}
    ternary_axis = {"gridcolor": grid, "linecolor": line, "color": text}

    # ``update`` merges, so anything a theme already set explicitly wins.
    lay.scene.update(xaxis=axis3d, yaxis=axis3d, zaxis=axis3d)
    lay.polar.update(bgcolor=plot, angularaxis=polar_axis, radialaxis=polar_axis)
    lay.geo.update(
        bgcolor=paper,
        landcolor=plot,
        lakecolor=plot,
        coastlinecolor=line,
        framecolor=line,
        countrycolor=grid,
    )
    lay.ternary.update(bgcolor=plot, aaxis=ternary_axis, baxis=ternary_axis, caxis=ternary_axis)
    return template
