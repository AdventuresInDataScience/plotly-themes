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
def test_theme_applies_to_a_figure(name):
    fig = go.Figure()
    fig.add_bar(x=[1, 2, 3], y=[3, 1, 2])
    fig.update_layout(template=name)
    # Validate by serialising — raises if the template is malformed.
    assert fig.to_plotly_json()["layout"]["template"] is not None


def test_register_all_is_idempotent():
    first = plotly_themes.register_all()
    second = plotly_themes.register_all()
    assert sorted(first) == sorted(second)
