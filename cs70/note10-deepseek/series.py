"""STRICT TEMPLATE for series.py: one language, one episode. Edit the REPLACE lines."""

SOURCE_LANG = "en"                       # REPLACE with "zh" for a Chinese video
LANGS = [SOURCE_LANG]                    # strict mode: one language

SERIES_NAME = {"en": "Graphs, Visually"}   # REPLACE (key = SOURCE_LANG)

# Pauses of the voice in seconds: after a sentence, a paragraph (a line break in a beat), a beat.
# These give about 130 to 150 words per minute. Do not change them unless check.py's pace line says WARN.
PACE = {"sentence": 0.9, "paragraph": 1.7, "beat": 1.7}
TTS = {"engine": "edge", "rate": "-6%"}

EPISODES = [
    # REPLACE: file name, class name in that file, title, one-line subtitle, output file name
    {"file": "ep01_konigsberg.py", "scene": "Ep01Konigsberg",
     "title": {"en": "The Seven Bridges of Königsberg"},
     "sub": {"en": "Eulerian tours"},
     "slug": {"en": "seven-bridges"}},
    {"file": "ep02_graph_language.py", "scene": "Ep02GraphLanguage",
     "title": {"en": "The Language of Graphs"},
     "sub": {"en": "vertices, edges, degrees, walks and connectivity"},
     "slug": {"en": "language-of-graphs"}},
    {"file": "ep03_trees.py", "scene": "Ep03Trees",
     "title": {"en": "Complete Graphs and Trees"},
     "sub": {"en": "the most edges, and the fewest that still connect"},
     "slug": {"en": "complete-graphs-and-trees"}},
    {"file": "ep04_planar.py", "scene": "Ep04Planar",
     "title": {"en": "Planar Graphs and Euler's Formula"},
     "sub": {"en": "drawing without crossings"},
     "slug": {"en": "planar-graphs"}},
    {"file": "ep05_hypercubes.py", "scene": "Ep05Hypercubes",
     "title": {"en": "Hypercubes"},
     "sub": {"en": "many connections from few edges"},
     "slug": {"en": "hypercubes"}},
]
