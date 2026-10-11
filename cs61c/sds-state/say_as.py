"""Pronunciations for the State and Timing series (read by tts.py).

The narration is written in words already ("clock to q", "nanoseconds"); these catch
the notation that still reaches the voice from title cards and end cards.
Check with `python <skill>/scripts/captions.py cs61c/sds-state 1 --spoken`.
"""

SAY_AS = {
    "CS61C": {"en": "C S sixty one C"},
    "clk-to-q": {"en": "clock to q"},
    "clock-to-q": {"en": "clock to q"},
    "CLK": {"en": "clock"},
    "FSM": {"en": "F S M"},
    "AND": {"en": "and"},            # "AND gates": the caps are for the reader, not the voice
    "GHz": {"en": "gigahertz"},
    "MHz": {"en": "megahertz"},
}

REWRITES = [
    (r"\bS([0-2])\b", {"en": r"S \1"}),
    (r"(\d) ?ns\b", {"en": r"\1 nanoseconds"}),
    (r"(\d) ?ps\b", {"en": r"\1 picoseconds"}),
]
