# plotly-themes

A collection of fun, ready-to-use visual themes for [Plotly](https://plotly.com/python/).
**Just import the package** and every theme is registered into Plotly's template
registry — pick one and go.

These aren't just background colours and palettes: each theme leans into Plotly's
styling to feel distinct — glowing alpha area fills, cross-hatched bars, rounded
"brick"/LCARS bars, digital step lines, hollow draughting markers, themed fonts,
dotted/dashed grids and more.

```python
import plotly_themes          # registers all themes on import
import plotly.express as px

fig = px.bar(x=["a", "b", "c"], y=[3, 1, 2], template="cyberpunk")
fig.show()
```

Or make a theme the default for your whole session:

```python
import plotly_themes
import plotly.io as pio

pio.templates.default = "matrix"
```

## Install

```bash
pip install plotly-themes
```

Or, with [uv](https://docs.astral.sh/uv/) for local development:

```bash
uv sync
```

## Themes

| | |
|---|---|
| **matrix** — phosphor green, digital step lines | **cyberpunk** — neon glow fills, rounded bars |
| ![matrix](docs/images/matrix.png) | ![cyberpunk](docs/images/cyberpunk.png) |
| **star_wars** — opening-crawl yellow, lightsaber glow | **star_trek** — 90s LCARS rounded console |
| ![star_wars](docs/images/star_wars.png) | ![star_trek](docs/images/star_trek.png) |
| **synthwave** — 80s sunset neon, dotted grid | **blueprint** — cross-hatched bars on draughting blue |
| ![synthwave](docs/images/synthwave.png) | ![blueprint](docs/images/blueprint.png) |
| **financial_times** — FT salmon paper, serif | **lego** — rounded brick bars, "stud" markers |
| ![financial_times](docs/images/financial_times.png) | ![lego](docs/images/lego.png) |
| **coke** — Coca-Cola ribbon splines, red wash | **xkcd** — hand-drawn comic, fat spline lines |
| ![coke](docs/images/coke.png) | ![xkcd](docs/images/xkcd.png) |
| **tableau** — classic Tableau 10 palette | **powerbi** — Power BI palette, rounded columns |
| ![tableau](docs/images/tableau.png) | ![powerbi](docs/images/powerbi.png) |
| **nike** — bold condensed type, value labels | **gameboy** — DMG green LCD, 8-bit pixel steps |
| ![nike](docs/images/nike.png) | ![gameboy](docs/images/gameboy.png) |
| **amber_terminal** — vintage amber CRT readout | **nord** — cool, muted arctic palette |
| ![amber_terminal](docs/images/amber_terminal.png) | ![nord](docs/images/nord.png) |
| **dracula** — dark slate with vivid pastels | |
| ![dracula](docs/images/dracula.png) | |

> **Note on the `xkcd` theme:** the hand-drawn look relies on a comic font. For the
> full effect, install [Humor Sans / xkcd Script](https://github.com/ipython/xkcd-font);
> otherwise it falls back to Comic Sans, then a plain sans-serif.

List the themes this package registered at runtime:

```python
import plotly_themes
print(plotly_themes.registered_themes())
```

## Adding a new theme

Themes are auto-discovered, so adding one is just dropping a file into
[`src/plotly_themes/themes/`](src/plotly_themes/themes/). Each module exposes two
names:

```python
# src/plotly_themes/themes/my_theme.py
import plotly.graph_objects as go

NAME = "my_theme"                       # the key used in pio.templates
TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": "#101010",
        "plot_bgcolor": "#101010",
        "colorway": ["#ff0066", "#00ccff", "#ffcc00"],
        # ...
    },
)
```

That's it — `import plotly_themes` will find and register it automatically.

## Regenerating the preview images

The images above are produced by [`scripts/generate_previews.py`](scripts/generate_previews.py),
which renders a sample figure for each theme. It uses Plotly's static image export
([kaleido](https://github.com/plotly/Kaleido)), which requires a Chrome/Chromium
install:

```bash
uv run python scripts/generate_previews.py
```

## License

MIT
