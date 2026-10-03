"""The episode list: order, titles and output names.

Episode numbers, title cards, "next episode" lines, the series-end card and
the video file names all come from here.
"""

SOURCE_LANG = "en"          # the episode files are written in English
LANGS = ["en"]
BURN_CAPTIONS = False       # subtitles go to the .srt next to the video, not onto the frame

SERIES_NAME = {"en": "CS182 · Discussion 5"}

TEXT_FONT = "latex"         # prose, numbers and formulas on screen all come from LaTeX (one typeface)

# Voice-over. Listen to the candidates with `python audition.py` (preview/voices/), then set them here.
# engine "edge" (online) reads "voice"; engine "kokoro" (offline) reads "kokoro_voice".
TTS = {"engine": "edge", "rate": "-4%",
       "voice": {"en": "en-US-AndrewNeural"}, "kokoro_voice": {"en": "am_michael"}}
# pauses in seconds: between sentences, between the paragraphs of one beat, after a beat
PACE = {"sentence": 0.75, "paragraph": 1.6, "beat": 1.8}

EPISODES = [
    {"file": "ep01_inventing_p.py", "scene": "Ep01InventingP",
     "title": {"en": "Newton–Schulz: You Could Have Invented It"},
     "sub": {"en": "From an ellipse to a circle · matrix products only · two wishes"},
     "slug": {"en": "newton-schulz-you-could-have-invented-it"}},
    {"file": "ep02_two_thresholds.py", "scene": "Ep02TwoThresholds",
     "title": {"en": "Newton–Schulz: Where Does a Singular Value Go?"},
     "sub": {"en": "Fixed points · the cobweb picture · √3 and √5"},
     "slug": {"en": "newton-schulz-where-does-a-singular-value-go"}},
    {"file": "ep03_the_gap.py", "scene": "Ep03TheGap",
     "title": {"en": "Newton–Schulz: Between √3 and √5"},
     "sub": {"en": "Flips and stripes · why the stripes fill the gap · back to the matrix"},
     "slug": {"en": "newton-schulz-between-root-3-and-root-5"}},
]
