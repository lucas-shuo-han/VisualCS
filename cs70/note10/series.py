"""STRICT TEMPLATE for series.py: one language, one episode. Edit the REPLACE lines."""

SOURCE_LANG = "en"                       # REPLACE with "zh" for a Chinese video
LANGS = [SOURCE_LANG]                    # strict mode: one language

SERIES_NAME = {"en": "Königsberg Bridges and Eulerian Tours"}   # REPLACE (key = SOURCE_LANG)

# Pauses of the voice in seconds: after a sentence, a paragraph (a line break in a beat), a beat.
# These give about 130 to 150 words per minute. Do not change them unless check.py's pace line says WARN.
PACE = {"sentence": 0.6, "paragraph": 1.3, "beat": 1.2}

EPISODES = [
    # REPLACE: file name, class name in that file, title, one-line subtitle, output file name
    {"file": "ep01_königsberg.py", "scene": "Ep01Königsberg",
     "title": {"en": "Königsberg Bridges"},
     "sub": {"en": "Euler's theorem on Eulerian tours"},
     "slug": {"en": "königsberg-bridges"}},
]
