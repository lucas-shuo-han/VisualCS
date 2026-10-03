"""Episode list for CS182 · Optimization (English only)."""

SOURCE_LANG = "en"
LANGS = ["en"]
SERIES_NAME = {"en": "CS182 · Optimization"}

EPISODES = [
    {"file": "ep01_gd_least_squares.py", "scene": "Ep01GdLeastSquares",
     "title": {"en": "Gradient Descent on Least Squares"},
     "sub": {"en": "one learning rate, many directions"}, "slug": {"en": "gd-least-squares"}},
    {"file": "ep02_null_space.py", "scene": "Ep02NullSpace",
     "title": {"en": "Where Gradient Descent Cannot Go"},
     "sub": {"en": "more parameters than data, and the solution it picks"}, "slug": {"en": "null-space"}},
    {"file": "ep03_ridge.py", "scene": "Ep03Ridge",
     "title": {"en": "Ridge: Distrusting Weak Directions"},
     "sub": {"en": "what a penalty does, one singular direction at a time"}, "slug": {"en": "ridge"}},
    {"file": "ep04_early_stopping.py", "scene": "Ep04EarlyStopping",
     "title": {"en": "Early Stopping and the Knobs"},
     "sub": {"en": "regularization hiding inside gradient descent"}, "slug": {"en": "early-stopping"}},
    {"file": "ep05_sgd.py", "scene": "Ep05Sgd",
     "title": {"en": "Stochastic Gradient Descent"},
     "sub": {"en": "a noisy step that is right on average"}, "slug": {"en": "sgd"}},
    {"file": "ep06_momentum.py", "scene": "Ep06Momentum",
     "title": {"en": "Momentum as a Low-Pass Filter"},
     "sub": {"en": "averaging the gradients to calm the bouncing"}, "slug": {"en": "momentum"}},
    {"file": "ep07_damping.py", "scene": "Ep07Damping",
     "title": {"en": "Damping and Stability of Momentum"},
     "sub": {"en": "two roots decide how fast a mode converges"}, "slug": {"en": "damping"}},
    {"file": "ep08_adam.py", "scene": "Ep08Adam",
     "title": {"en": "Adam and AdamW"},
     "sub": {"en": "normalizing every coordinate, and decoupling weight decay"}, "slug": {"en": "adam"}},
    {"file": "ep09_standardize_init.py", "scene": "Ep09StandardizeInit",
     "title": {"en": "Standardize Inputs, Initialize Weights"},
     "sub": {"en": "setting the stage so that optimization can work"}, "slug": {"en": "standardize-init"}},
]
