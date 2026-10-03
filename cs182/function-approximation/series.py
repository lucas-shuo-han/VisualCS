"""Episode list for CS182 · Function Approximation (English only)."""

SOURCE_LANG = "en"
LANGS = ["en"]
SERIES_NAME = {"en": "CS182 · Function Approximation"}

EPISODES = [
    {"file": "ep01_samples.py", "scene": "Ep01Samples",
     "title": {"en": "Learning a Function from Samples"},
     "sub": {"en": "what are we trying to learn, and what makes it hard?"}, "slug": {"en": "samples"}},
    {"file": "ep02_relu_ramps.py", "scene": "Ep02ReluRamps",
     "title": {"en": "ReLU Ramps Are a Spline Basis"},
     "sub": {"en": "how a sum of bent lines draws any piecewise-linear curve"}, "slug": {"en": "relu-ramps"}},
    {"file": "ep03_layer.py", "scene": "Ep03Layer",
     "title": {"en": "From Ramps to a Layer"},
     "sub": {"en": "affine, ReLU, affine: the pattern behind every network"}, "slug": {"en": "layer"}},
    {"file": "ep04_risk.py", "scene": "Ep04Risk",
     "title": {"en": "Looking Where the Light Is"},
     "sub": {"en": "training loss is a proxy, not the goal"}, "slug": {"en": "risk"}},
    {"file": "ep05_holdout.py", "scene": "Ep05Holdout",
     "title": {"en": "Hold Out What Will Be New"},
     "sub": {"en": "a model that never looks at the lungs"}, "slug": {"en": "holdout"}},
]
