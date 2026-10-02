"""The episode list: order, titles and output names.

Episode numbers, title cards, "next episode" lines, the series-end card and
the video file names all come from here.
"""

SOURCE_LANG = "en"          # the episode files are written in English
LANGS = ["en"]

SERIES_NAME = {"en": "CS182 · Discussion 5"}

EPISODES = [
    {"file": "ep01_newton_schulz.py", "scene": "Ep01NewtonSchulz",
     "title": {"en": "Newton–Schulz: Where Does a Singular Value Go?"},
     "sub": {"en": "From an ellipse to a circle · fixed points · √3 and √5 · alternating basins"},
     "slug": {"en": "newton-schulz-where-does-a-singular-value-go"}},
]
