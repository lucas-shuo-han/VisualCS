"""Small helper for cue phrases in a bilingual episode.

`cue()` finds its phrase in the beat's text. In a translated render the beat is the
English text, so a Chinese phrase can only be placed by its relative position in the
Chinese source, which drifts when the English is a rewrite rather than a translation.
`L(zh, en)` gives each language its own phrase, so the cue lands on the actual words:

    self.cue(L("但 CPU 并不认识 C", "But a CPU can't run C"), FadeIn(machine))

The English phrase must be a substring of that beat's English text in i18n/epNN.py;
a miss prints "[cue] phrase not in the current line" in the render log.
"""

from manim_kit import EN


def L(zh: str, en: str) -> str:
    return en if EN else zh
