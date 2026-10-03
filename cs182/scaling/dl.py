"""Shared palette and helpers for the CS182 Scaling and muP series (extends the Function Approximation palette).

One color per concept across all five episodes:
  data points ......... WHITE          true target f ....... GREY_A (dashed)
  model N_theta ....... BLUE_C         ReLU ramps / hidden units ... TEAL_C
  loss / error / risk . RED_C          regularization lambda ....... ORANGE
  training data ....... GREEN_C        validation data ............. GOLD_C
  test data ........... PURPLE_B
New in this unit:
  gradient g .......... MAROON_B        update step / Delta ......... YELLOW_D
  singular values ..... PINK             width / RMS scale ........... TEAL_B
  standard scaling .... RED_C (as loss/blow-up)   muP scaling ... GREEN_C
"""

import numpy as np

from manim_kit import *  # noqa: F401,F403

C_DATA = WHITE
C_TARGET = GREY_A
C_MODEL = BLUE_C
C_RAMP = TEAL_C
C_LOSS = RED_C
C_LAM = ORANGE
C_TRAIN = GREEN_C
C_VAL = GOLD_C
C_TEST = PURPLE_B

C_GRAD = MAROON_B
C_STEP = YELLOW_D
C_SV = PINK
C_WIDTH = TEAL_B
C_STD = RED_C
C_MUP = GREEN_C

SERIES = "CS182 · Scaling and muP"


def relu(z):
    return np.maximum(0.0, z)


def mt(tex, size=0.8, color=C_TEXT):
    """MathTex scaled to a comfortable on-screen size."""
    return MathTex(tex, color=color).scale(size)


def mts(parts, size=0.8, colors=None):
    """MathTex from a list of parts; `colors` maps part index -> color."""
    m = MathTex(*parts).scale(size)
    for i, c in (colors or {}).items():
        m[i].set_color(c)
    return m


def make_axes(x_range, y_range, w=7.0, h=3.6, **kw):
    return Axes(x_range=x_range, y_range=y_range, x_length=w, y_length=h,
                axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2, **kw})


def plot(axes, f, color=C_MODEL, x_range=None, width=4, **kw):
    """Plot a python/numpy function on `axes` (vectorised or not)."""
    xr = x_range or [axes.x_range[0], axes.x_range[1]]
    return axes.plot(lambda x: float(f(x)), x_range=xr, color=color, stroke_width=width,
                     use_smoothing=False, **kw)


def polyline(axes, xs, ys, color=C_MODEL, width=4):
    pts = [axes.c2p(x, y) for x, y in zip(xs, ys)]
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)


def dots(axes, xs, ys, color=C_DATA, r=0.09):
    return VGroup(*[Dot(axes.c2p(x, y), radius=r, color=color) for x, y in zip(xs, ys)])


def tick_labels(axes, xs, size=20, dy=0.18, fmt="{:g}"):
    return VGroup(*[txt(fmt.format(x), size, GREY_B).next_to(axes.c2p(x, axes.y_range[0]), DOWN, buff=dy) for x in xs])


def caption_free_y(y):
    """Assert that a y coordinate is above the caption band."""
    assert y > -2.9, y
