"""Generate a preview PNG for every registered theme into docs/images/.

Run with:  uv run --native-tls python scripts/generate_previews.py
"""

from __future__ import annotations

import math
from pathlib import Path

import plotly.graph_objects as go
import plotly.io as pio

import plotly_themes

OUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "images"


def sample_figure(theme: str) -> go.Figure:
    """A representative figure exercising bars, lines and markers."""
    x = list(range(1, 13))
    line_y = [10 + 6 * math.sin(i / 1.7) + i * 0.4 for i in x]
    line2_y = [8 + 5 * math.cos(i / 2.1) + i * 0.25 for i in x]
    bar_y = [4 + 3 * abs(math.sin(i / 1.3)) for i in x]

    fig = go.Figure()
    fig.add_bar(x=x, y=bar_y, name="Volume")
    fig.add_scatter(x=x, y=line_y, mode="lines+markers", name="Series A")
    fig.add_scatter(x=x, y=line2_y, mode="lines+markers", name="Series B")
    fig.update_layout(
        template=theme,
        title=f"plotly-themes — {theme}",
        xaxis_title="Month",
        yaxis_title="Value",
        width=900,
        height=500,
        margin=dict(l=70, r=30, t=70, b=60),
    )
    return fig


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name in sorted(plotly_themes.registered_themes()):
        fig = sample_figure(name)
        out = OUT_DIR / f"{name}.png"
        fig.write_image(str(out), scale=1)
        print(f"wrote {out.relative_to(OUT_DIR.parent.parent)}")
    print(f"\n{len(plotly_themes.registered_themes())} previews written to {OUT_DIR}")


if __name__ == "__main__":
    main()
