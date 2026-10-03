"""Shared palette and helpers for the CS182 Optimization series (extends the Function Approximation palette).

One color per concept across all episodes:
  data points ......... WHITE          true target f ....... GREY_A (dashed)
  model N_theta ....... BLUE_C         ReLU ramps / hidden units ... TEAL_C
  loss / error / risk . RED_C          regularization lambda ....... ORANGE
  training data ....... GREEN_C        validation data ............. GOLD_C
  test data ........... PURPLE_B
New in this unit (Optimization):
  iterate w_t / path .. YELLOW_C         learning rate eta ........ YELLOW_D
  gradient (arrow) .... near-white       stiff direction (big sigma) MAROON_B
  soft direction (small sigma) TAN       momentum / first moment m  PINK
  second moment v ..... PURPLE_C         noise / SGD .............. pale steel blue
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

C_ITER = YELLOW_C
C_ETA = YELLOW_D
C_GRAD = "#F2F2F2"
C_STIFF = MAROON_B
C_SOFT = "#C9A66B"
C_MOM = PINK
C_V2 = PURPLE_C
C_NOISE = "#8FB8DE"

SERIES = "CS182 · Optimization"


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


# ------------------------------------------------------------------ Optimization-unit helpers


def clipped(ax, xs, ys, lo, hi, color=C_ITER, width=4):
    """Polyline through (xs, ys) up to the first point outside [lo, hi] (a diverging iterate leaves the frame)."""
    n = 0
    for y in ys:
        if lo <= y <= hi:
            n += 1
        else:
            break
    if n < 2:
        return VMobject()
    return polyline(ax, xs[:n], ys[:n], color, width)


def ellipse_pts(ax, a, b, n=120):
    """Closed curve x = a cos t, y = b sin t in the axes' data coordinates."""
    return VMobject(stroke_width=2).set_points_as_corners(
        [ax.c2p(a * np.cos(t), b * np.sin(t)) for t in np.linspace(0, 2 * np.pi, n)])


def contour_family(ax, lams, levels, colors=(BLUE_E, BLUE_D, BLUE_C, TEAL_D, TEAL_C)):
    """Contours {x^T diag(lams) x = c} of a 2-D quadratic; lams = (l_x, l_y) act on the (x, y) data coordinates."""
    out = VGroup()
    for k, c in enumerate(levels):
        e = ellipse_pts(ax, np.sqrt(c / lams[0]), np.sqrt(c / lams[1]))
        e.set_stroke(color=colors[k % len(colors)], width=2)
        out.add(e)
    return out


def path_pts(ax, pts, color=C_ITER, width=3):
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners([ax.c2p(x, y) for x, y in pts])


def path_dots(ax, pts, color=C_ITER, r=0.06):
    return VGroup(*[Dot(ax.c2p(x, y), radius=r, color=color) for x, y in pts])


def assert_on_screen(*mobs, xmax=7.0, ymin=-2.5, ymax=3.6):
    """Assert that mobjects sit inside the frame and above the caption band."""
    for m in mobs:
        assert m.get_left()[0] > -xmax and m.get_right()[0] < xmax, (m.get_left()[0], m.get_right()[0])
        assert m.get_bottom()[1] > ymin and m.get_top()[1] < ymax, (m.get_bottom()[1], m.get_top()[1])
