"""Episode list for CS182 · Scaling and muP (English only)."""

SOURCE_LANG = "en"
LANGS = ["en"]
SERIES_NAME = {"en": "CS182 · Scaling and muP"}

EPISODES = [
    {"file": "ep01_steepest.py", "scene": "Ep01Steepest",
     "title": {"en": "Steepest Descent Under a Norm"},
     "sub": {"en": "pick a norm and a step size, and an optimizer falls out"}, "slug": {"en": "steepest"}},
    {"file": "ep02_spectral.py", "scene": "Ep02Spectral",
     "title": {"en": "Matrices Want the Spectral Norm"},
     "sub": {"en": "the best step for a weight matrix flattens every singular value to one"}, "slug": {"en": "spectral"}},
    {"file": "ep03_rms.py", "scene": "Ep03Rms",
     "title": {"en": "The RMS Norm"},
     "sub": {"en": "the norm that Xavier initialization was quietly preserving"}, "slug": {"en": "rms"}},
    {"file": "ep04_muon.py", "scene": "Ep04Muon",
     "title": {"en": "Muon: Orthogonalize Cheaply"},
     "sub": {"en": "Newton-Schulz iterations replace the SVD"}, "slug": {"en": "muon"}},
    {"file": "ep05_transfer.py", "scene": "Ep05Transfer",
     "title": {"en": "The Right Scaling Transfers"},
     "sub": {"en": "tune a small network, copy the hyperparameter to a big one"}, "slug": {"en": "transfer"}},
    {"file": "ep06_mup.py", "scene": "Ep06Mup",
     "title": {"en": "Maximal Update Parametrization"},
     "sub": {"en": "keep activations and updates the same size at every width"}, "slug": {"en": "mup"}},
]
