"""Lego theme: primary brick colours, bold black outlines, and chunky rounded
"brick" bars topped with big round "stud" markers."""

import plotly.graph_objects as go

NAME = "lego"

_BG = "#FFFFFF"
_INK = "#1B1B1B"
_FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _BG,
        "plot_bgcolor": "#F2F2F2",
        "font": {"family": _FONT, "size": 15, "color": _INK},
        "title": {"font": {"family": _FONT, "size": 28, "color": _INK}},
        # Classic LEGO brick colours: red, yellow, blue, green, orange, black.
        "colorway": ["#D01012", "#F6D316", "#0057A6", "#00852B", "#FF6F00", "#1B1B1B"],
        "colorscale": {
            "sequential": [[0, "#F6D316"], [0.5, "#FF6F00"], [1, "#D01012"]],
        },
        "hovermode": "closest",
        "hoverlabel": {
            "bgcolor": "#FFFFFF",
            "bordercolor": _INK,
            "font": {"family": _FONT, "color": _INK},
        },
        "xaxis": {
            "gridcolor": "#FFFFFF",
            "linecolor": _INK,
            "linewidth": 2,
            "zerolinecolor": _INK,
            "tickcolor": _INK,
            "tickfont": {"color": _INK},
        },
        "yaxis": {
            "gridcolor": "#FFFFFF",
            "linecolor": _INK,
            "linewidth": 2,
            "zerolinecolor": _INK,
            "tickcolor": _INK,
            "tickfont": {"color": _INK},
        },
        "legend": {"bgcolor": "#FFFFFF", "bordercolor": _INK, "borderwidth": 2},
    },
    data={
        # Moulded-plastic bricks: rounded corners + heavy black outline.
        "bar": [
            go.Bar(marker={"cornerradius": 6, "line": {"color": _INK, "width": 3}})
        ],
        # Big round "studs" on thick lines.
        "scatter": [
            go.Scatter(
                mode="lines+markers",
                line={"width": 4},
                marker={"symbol": "circle", "size": 14, "line": {"color": _INK, "width": 2}},
            )
        ],
    },
)
