"""The episode list for CS61C L18, State and Timing: order, titles and output names.

Episode numbers, title cards, "next episode" lines, the series-end card and
the video file names all come from here.
"""

SOURCE_LANG = "en"          # the episode files are written in English
LANGS = ["en"]
BURN_CAPTIONS = False       # subtitles go to the .srt next to the video, not onto the frame

SERIES_NAME = {"en": "CS61C · State and Timing"}

TEXT_FONT = "latex"         # prose, numbers and formulas on screen all come from LaTeX (one typeface)

# Voice-over: the voice and speed chosen by ear for the Newton-Schulz series (cs182/newton-schulz).
# engine "edge" (online) reads "voice"; engine "kokoro" (offline) reads "kokoro_voice".
TTS = {"engine": "edge", "rate": "-4%",
       "voice": {"en": "en-US-AndrewNeural"}, "kokoro_voice": {"en": "am_michael"}}
# pauses in seconds: between sentences, between the paragraphs of one beat, after a beat
PACE = {"sentence": 0.75, "paragraph": 1.6, "beat": 1.8}

EPISODES = [
    # notes.txt: "Signals, Waveforms, and the Clock"; "The Register" §1-2; "Timing" §2.1-2.3
    {"file": "ep01_runaway_sum.py", "scene": "Ep01RunawaySum",
     "title": {"en": "The Sum That Ran Away"},
     "sub": {"en": "An adder · a feedback wire · why circuits need a clock"},
     "slug": {"en": "the-sum-that-ran-away"}},
    # "The Register" §3; "Summary" (register example, exercises)
    {"file": "ep02_flip_flop.py", "scene": "Ep02FlipFlop",
     "title": {"en": "Inside the Register"},
     "sub": {"en": "Flip-flops · setup time · hold time · clock-to-q"},
     "slug": {"en": "inside-the-register"}},
    # "Timing a Synchronous System" §2.4, 3, 4; "Summary" (relationships)
    {"file": "ep03_clock_speed.py", "scene": "Ep03ClockSpeed",
     "title": {"en": "How Fast Can the Clock Tick?"},
     "sub": {"en": "The critical path · maximum frequency · hold violations"},
     "slug": {"en": "how-fast-can-the-clock-tick"}},
    # "Finite State Machines"; "Summary" (two-state machine)
    {"file": "ep04_three_ones.py", "scene": "Ep04ThreeOnes",
     "title": {"en": "Three Ones in a Row"},
     "sub": {"en": "A machine with memory · states · from a diagram to gates"},
     "slug": {"en": "three-ones-in-a-row"}},
    # "Pipelining for Performance"; "Signals, Waveforms, and the Clock" §5
    {"file": "ep05_pipelining.py", "scene": "Ep05Pipelining",
     "title": {"en": "A Register to Go Faster"},
     "sub": {"en": "Pipelining · throughput against latency · the general model"},
     "slug": {"en": "a-register-to-go-faster"}},
]
