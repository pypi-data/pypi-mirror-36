"""Heatmap implementation."""
from .signatures import bivariate_recipe, color
import altair as alt
from autosig import autosig, Signature, param
from math import sqrt


def maxbins(data):
    """Return a pair of ints with reasonable defaults for binning in heatmap."""
    n = sqrt(data.shape[0])

    return data, n * 4 // 3, n * 3 // 4


@autosig(bivariate_recipe + Signature(
    color=color(default=2, position=3),
    aggregate=param(
        default="average",
        position=4,
        docstring="""`str`
    The aggregation function to set the color of each mark, see https://altair-viz.github.io/user_guide/encoding.html#encoding-aggregates for available options""",
    ),
))
def heatmap(data,
            x=0,
            y=1,
            color=2,
            aggregate="average",
            height=300,
            width=400):
    """Generate a heatmap."""
    data, nx, ny = maxbins(data)
    return (alt.Chart(data, height=height, width=width).mark_rect().encode(
        x=alt.X(x, bin=alt.Bin(maxbins=nx)),
        y=alt.Y(y, bin=alt.Bin(maxbins=ny)),
        color=alt.Color(
            aggregate + "(" + color + "):Q",
            scale=alt.Scale(scheme="greenblue")),
    ))


@autosig(bivariate_recipe)
def count_heatmap(data, x=0, y=1, height=300, width=400):
    """Create a heatmap of the count of points in each square."""
    return heatmap(
        data,
        x=x,
        y=y,
        color="x",
        aggregate="count",
        height=height,
        width=width)
