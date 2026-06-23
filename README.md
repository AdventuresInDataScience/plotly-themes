# plotly-themes
Collection of various themes which can be applied to plotly with a single import

## Installation

```bash
pip install plotly-themes
```

## Usage

```python
import plotly.express as px
from plotly_themes import apply_theme

fig = px.scatter(px.data.iris(), x="sepal_width", y="sepal_length")
apply_theme(fig, template="plotly_dark")
fig.show()
```
