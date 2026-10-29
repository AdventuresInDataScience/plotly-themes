"""Tests that every bundled theme registers and produces a valid Plotly template."""

import plotly.graph_objects as go
import plotly.io as pio
import pytest

import plotly_themes

REGISTERED = plotly_themes.registered_themes()


def test_import_registers_themes():
    assert len(REGISTERED) >= 1
    # A few we expect to always be present.
    for expected in ("matrix", "cyberpunk", "financial_times", "lego"):
        assert expected in REGISTERED


@pytest.mark.parametrize("name", REGISTERED)
def test_theme_is_registered_in_plotly(name):
    assert name in pio.templates


@pytest.mark.parametrize("name", REGISTERED)
def test_theme_template_is_valid(name):
    template = pio.templates[name]
    assert isinstance(template, go.layout.Template)
    # Every theme should at least define a colourway.
    assert template.layout.colorway, f"{name} has no colorway"


@pytest.mark.parametrize("name", REGISTERED)
def test_theme_palette_has_depth(name):
    # Every theme should support at least medium-cardinality charts without the
    # colourway repeating too soon.
    colorway = pio.templates[name].layout.colorway
    assert len(colorway) >= 10, f"{name} colourway only has {len(colorway)} colours"


@pytest.mark.parametrize("name", REGISTERED)
def test_theme_applies_to_a_figure(name):
    fig = go.Figure()
    fig.add_bar(x=[1, 2, 3], y=[3, 1, 2])
    fig.update_layout(template=name)
    # Validate by serialising — raises if the template is malformed.
    assert fig.to_plotly_json()["layout"]["template"] is not None


@pytest.mark.parametrize("name", REGISTERED)
def test_dark_themes_style_noncartesian_subplots(name):
    # Themes that set a plot background should propagate it to 3D/polar/geo/
    # ternary subplots so those chart types match the theme too.
    lay = pio.templates[name].layout
    if lay.plot_bgcolor is None and lay.paper_bgcolor is None:
        pytest.skip(f"{name} sets no background")
    expected = lay.plot_bgcolor or lay.paper_bgcolor
    assert lay.polar.bgcolor == expected
    assert lay.scene.xaxis.backgroundcolor == expected
    assert lay.ternary.bgcolor == expected


def test_register_all_is_idempotent():
    first = plotly_themes.register_all()
    second = plotly_themes.register_all()
    assert sorted(first) == sorted(second)
