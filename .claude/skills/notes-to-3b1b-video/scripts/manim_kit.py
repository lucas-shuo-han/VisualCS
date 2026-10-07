"""manim_kit — building blocks for 3Blue1Brown-style explainer videos.

Copy this file next to your episode files and `from manim_kit import *`.

Contents (search for the section banners):
  language & series ..... LANG, tr(), EN, series.py / i18n tables (see below)
  fonts & palette ....... SANS / MONO picked from installed fonts, BG, semantic colors
  text helpers .......... txt(), mono(), num(), tex_text(), box_label(), file_icon()
  captions .............. wrap_caption(), reading_time(), sentences()
  NarratedScene ......... say() / cue() / hold() / clear_stage() / heading() / title_card() / end_card()
                          zoom_to() / zoom_back() / pin()   (the camera can move)
                          fast_forward() / preview_only()
  code .................. CodeListing (asm / c / python highlighting), pc_arrow()
  bits .................. bit_row(), set_bit_row(), BitField, FormatScene helpers
  machine state ......... RegBox, reg_column(), RegisterFile, MemoryView, WordColumn, alu_shape()
  ML / math ............. nn_diagram(), heatmap()  (see references/visual-patterns.md for more)

Every episode is one NarratedScene, narrated in beats:

    self.say("Two or three connected sentences about one picture. The voice reads them "
             "one at a time, with a pause after each. The subtitle shows one sentence at a time.",
             FadeIn(thing))
    self.cue("The voice reads them", Indicate(thing))   # when the voice reaches these words

A line break inside the text of a beat starts a new paragraph: a longer pause.

Subtitles are drawn on the frame and exported as an .srt next to the video, one
sentence at a time with the same timing. With BURN_CAPTIONS = False in series.py
(or KIT_CAPTIONS=0) nothing is drawn on the frame and the .srt is the only subtitle.

Optional files next to this one (see the skill's references/bilingual-and-voice.md):
  series.py ............. episode order, titles per language, SOURCE_LANG, LANGS.
                          title_card() / end_card() then need no arguments and
                          "next episode" / "the end" are automatic. Also the
                          series-wide choices: BURN_CAPTIONS, TEXT_FONT, PACE
                          (pauses of the voice) and TTS (engine, voice, rate).
  i18n/epNN.py .......... translation tables: a dict per target language
                          (EN = {...}, ZH = {...}) keyed by the source string.
  tts.py (+ say_as.py) .. voice-over (edge-tts) and course pronunciations.

Environment (render.py sets these):
  KIT_LANG=xx        render in language xx; every Text is looked up in the
                     episode's table. With a CJK source language a missing
                     entry is an error (nothing untranslated can slip through).
  KIT_I18N_LAX=1     warn instead of failing on a missing translation.
  KIT_TTS=1          voice-over: each beat is spoken sentence by sentence and
                     lasts until its audio has finished, plus a pause.
  KIT_ONLY=a,b       render only these scene methods (preview.py; see preview_only).
  KIT_CAPTIONS=0|1   override series.py BURN_CAPTIONS (0: subtitles only in the .srt).
  KIT_CHECKS=0       switch off the checks below.

Checks while rendering (lines on stderr, so in the render log; check.py collects them):
  [layout]  two texts on top of each other, a text outside the frame, a text in the
            subtitle band (below y = -2.9), a line or curve running through a text, two
            shapes drawn exactly on top of each other (seven edges that look like five).
            Looked at whenever the picture has settled: after a cue(), at hold(), before
            clear_stage(), at the end of a beat.
  [empty]   nothing was on the stage during a beat.     [textonly] only words were on
            the stage during a beat (a slide, not a picture). Warnings outside --strict.
  [still]   a beat of more than 14 s of narration with a single animation step (26 s:
            two): the picture stands still while the voice talks. Add cue()s.
  [cue]     a cue() phrase that is not in its beat.   [narration] a speak= mismatch.
"""

from __future__ import annotations

import math
import os
import re
import sys

from manim import *

# ---------------------------------------------------------------- language & series

HERE = os.path.dirname(os.path.abspath(__file__))
CJK_LANGS = {"zh", "ja", "ko"}
_CJK_RE = re.compile(r"[　-〿㐀-鿿＀-￯぀-ヿ가-힯]")


def _load_py(path) -> dict:
    ns: dict = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            exec(compile(fh.read(), path, "exec"), ns)
    return ns


_SERIES = _load_py(os.path.join(HERE, "series.py"))
SOURCE_LANG = _SERIES.get("SOURCE_LANG") or os.environ.get("KIT_SOURCE_LANG", "en")
LANG = (os.environ.get("KIT_LANG") or SOURCE_LANG).lower()
TRANSLATING = LANG != SOURCE_LANG
I18N_LAX = os.environ.get("KIT_I18N_LAX") == "1"
TTS = os.environ.get("KIT_TTS") == "1"
CHECKS = os.environ.get("KIT_CHECKS", "1") != "0"
BURN_CAPTIONS = (os.environ["KIT_CAPTIONS"] != "0" if os.environ.get("KIT_CAPTIONS")
                 else bool(_SERIES.get("BURN_CAPTIONS", True)))
# "latex": txt() and num() are typeset by LaTeX, so prose, numbers and formulas share one
# typeface (for a math-heavy series; needs LaTeX). "pango": the caption font.
TEXT_FONT = _SERIES.get("TEXT_FONT", "pango")
# pauses of the voice-over, in seconds: between sentences, between the paragraphs of one
# beat, and after a beat. A derivation wants more (0.75 / 1.6 / 1.8), see narration-writing.md.
PACE = {"sentence": 0.4, "paragraph": 1.0, "beat": 0.8, **_SERIES.get("PACE", {})}
EPISODES = [dict(e, num=i + 1) for i, e in enumerate(_SERIES.get("EPISODES", []))]
_BY_SCENE = {e["scene"]: e for e in EPISODES}
EN = LANG == "en"   # handy for the rare `if EN:` layout branch in an episode

_TABLE: dict[str, str] = {}


class MissingTranslation(KeyError):
    pass


def load_table(n: int) -> dict:
    """Make i18n/epNN.py's table for the current language the active one."""
    _TABLE.clear()
    if TRANSLATING:
        _TABLE.update(_load_py(os.path.join(HERE, "i18n", f"ep{n:02d}.py")).get(LANG.upper(), {}))
    return _TABLE


def tr(s):
    """The string to show for `s` in the current language."""
    if not TRANSLATING or not isinstance(s, str) or not s.strip():
        return s
    if s in _TABLE:
        return _TABLE[s]
    if SOURCE_LANG in CJK_LANGS and _CJK_RE.search(s) and not I18N_LAX:
        raise MissingTranslation(f"no {LANG} for {s!r}: add it to i18n/epNN.py "
                                 f"(i18n_check.py --skeleton prints the missing entries)")
    if SOURCE_LANG in CJK_LANGS and _CJK_RE.search(s):
        print(f"i18n: missing translation: {s!r}", file=sys.stderr)
    return s   # a Latin source can't tell labels ("sp", "0x10") from prose: pass through


def S(key, **kw) -> str:
    """A kit UI string (title/end cards) in the current language."""
    return STRINGS.get(LANG, STRINGS["en"])[key].format(**kw)


def series_name() -> str:
    n = _SERIES.get("SERIES_NAME", "")
    return n.get(LANG, n.get(SOURCE_LANG, "")) if isinstance(n, dict) else n


if TRANSLATING:
    # Route every Text through the table, whoever builds it. MarkupText can't be
    # looked up (its markup is generated), so it must arrive translated.
    _text_init = Text.__init__
    _markup_init = MarkupText.__init__
    # a CJK font draws curly quotes full-width, which gapes in Latin text
    _STRAIGHT = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'"})

    def _text_init_tr(self, text, *a, **kw):
        text = tr(text)
        if isinstance(text, str) and LANG not in CJK_LANGS:
            text = text.translate(_STRAIGHT)
        _text_init(self, text, *a, **kw)

    def _markup_init_checked(self, text, *a, **kw):
        plain = re.sub(r"<[^>]*>", "", text)
        if SOURCE_LANG in CJK_LANGS and _CJK_RE.search(plain) and not I18N_LAX:
            raise MissingTranslation(f"untranslated MarkupText {plain!r}")
        _markup_init(self, text, *a, **kw)

    Text.__init__ = _text_init_tr
    MarkupText.__init__ = _markup_init_checked

# ---------------------------------------------------------------- fonts & palette


def _pick_font(candidates):
    try:
        import manimpango

        have = set(manimpango.list_fonts())
    except Exception:  # pragma: no cover - font listing is best effort
        have = set()
    for c in candidates:
        if c in have:
            return c
    return candidates[-1]


# A CJK-capable sans first when any CJK text can appear: it also covers Latin, so mixed
# captions never fall back mid-line. Latin-only videos use a Latin sans: CJK fonts draw
# math symbols badly (Noto Sans CJK's √ has a detached overbar, "√‾3").
_CJK_SANS = ["Noto Sans CJK SC", "Source Han Sans SC", "PingFang SC"]
_LATIN_SANS = ["Helvetica Neue", "Noto Sans", "Arial", "FreeSans", "DejaVu Sans"]
SANS = os.environ.get("MANIM_KIT_SANS") or _pick_font(
    (_CJK_SANS + _LATIN_SANS if CJK_LANGS & {LANG, SOURCE_LANG} else _LATIN_SANS + _CJK_SANS)
    + ["Sans"])
MONO = os.environ.get("MANIM_KIT_MONO") or _pick_font(
    ["DejaVu Sans Mono", "JetBrains Mono", "Menlo", "Noto Sans Mono", "Monospace"])
CJK = SANS  # backward-compatible alias
BG = "#0B0D12"


def _register_user_fonts():
    """Windows: fonts installed per user are invisible to Pango until the next
    login. Register them for this process as a fallback -- slow (manimpango
    re-adds every file on each text render), so prefer running win_fonts.py."""
    if sys.platform != "win32":
        return
    import glob

    import manimpango

    if "Noto Sans CJK SC" in manimpango.list_fonts():
        return
    d = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts")
    files = [p for pat in ("NotoSansCJK*", "DejaVuSans*") for p in glob.glob(os.path.join(d, pat))]
    if files:
        print("warning: fonts not loaded in this Windows session; registering per process "
              "(slow). Run win_fonts.py once to fix.", file=sys.stderr)
        for p in files:
            manimpango.register_font(p)


_register_user_fonts()

config.background_color = BG

# UI strings of the title and end cards. Add a language by adding a row.
STRINGS = {
    "en": {"episode": "Episode {n}", "summary": "Recap", "next": "Next: {t}",
           "end": "{s} · The End",
           "say_episode": "Episode {n}: {t}.", "say_summary": "To sum up.",
           "say_next": "Next time: {t}.", "say_end": "That's the end of {s}. Thanks for watching!"},
    "zh": {"episode": "第 {n} 集", "summary": "小结", "next": "下一集：{t}",
           "end": "{s} · 完",
           "say_episode": "第 {n} 集：{t}。", "say_summary": "小结一下。",
           "say_next": "下一集：{t}。", "say_end": "{s} 到这里就结束了，感谢观看！"},
}

# syntax colors
C_MNEM = YELLOW_D
C_REG = BLUE_B
C_NUM = GOLD_B
C_LABEL = GREEN_B
C_COMMENT = GREY
C_KEYWORD = PURPLE_B
C_TEXT = "#ECECEC"

# register groups (ABI)
C_T = TEAL_C      # temporaries t0-t6
C_S = BLUE_C      # saved s0-s11
C_A = GOLD_C      # arguments a0-a7
C_RA = RED_C
C_SP = PURPLE_B
C_ZERO = GREY_B

# instruction-format fields
FIELD_COLORS = {
    "opcode": BLUE_C,
    "rd": GREEN_C,
    "funct3": PURPLE_B,
    "rs1": TEAL_C,
    "rs2": GOLD_C,
    "funct7": RED_C,
    "imm": YELLOW_D,
}

ABI_NAMES = [
    "zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2",
    "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5",
    "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7",
    "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6",
]


def abi_color(name: str) -> ManimColor:
    if name == "zero":
        return C_ZERO
    if name == "ra":
        return C_RA
    if name in ("sp", "gp", "tp"):
        return C_SP
    return {"t": C_T, "s": C_S, "a": C_A}.get(name[0], WHITE)


def hexc(c) -> str:
    return ManimColor(c).to_hex()


def hex32(v: int) -> str:
    return f"0x{v & 0xFFFFFFFF:08X}"


def bin_str(v: int, width: int) -> str:
    return format(v & ((1 << width) - 1), f"0{width}b")


_OVERSAMPLE = 4


def crisp_text(s, font, size, color=C_TEXT, **kw) -> Text:
    """Text rendered at 4x size and scaled down. Pango drops or squeezes spaces
    at small font sizes ("priority queue" -> "priorityqueue"); oversampling
    keeps word spacing and kerning right at every size."""
    return Text(s, font=font, font_size=size * _OVERSAMPLE, color=color, **kw).scale(1 / _OVERSAMPLE)


# CJK runs (and the quotes/dashes CJK text uses) inside monospace text
CJK_RUN = re.compile(r"[⺀-鿿＀-￯　-〿぀-ヿ가-힯“”‘’…—]+")


def mono(s, size=24, color=C_TEXT, **kw) -> Text:
    s = tr(s)
    # Name the CJK font for CJK runs: Pango on Windows does not fall back from
    # the monospace font the way fontconfig does on Linux (you'd get boxes).
    t2f = {run: SANS for run in set(CJK_RUN.findall(s))}
    if t2f:
        kw["t2f"] = {**t2f, **kw.get("t2f", {})}
    return crisp_text(s, MONO, size, color, disable_ligatures=True, **kw)


_TEX_ESCAPE = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_", "{": r"\{",
               "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
_TEX_MATH = {"−": "-", "±": r"\pm ", "×": r"\times ", "·": r"\cdot ", "σ": r"\sigma ", "Σ": r"\Sigma ",
             "⇔": r"\Leftrightarrow ", "≈": r"\approx ", "→": r"\to ", "ᵀ": r"^{\top}", "<": "<", ">": ">",
             "|": "|", "≤": r"\le ", "≥": r"\ge ", "=": "="}
TEX_LABEL = 28   # with TEXT_FONT = "latex", labels come in one size


def tex_text(s, size=TEX_LABEL, color=C_TEXT, bold=False):
    """Prose typeset by LaTeX, in the typeface of the formulas. Unicode math
    signs inside it (√3, −1, σ, ×, ⇔ ...) become real math. Text with CJK
    characters falls back to the caption font."""
    s = tr(s)
    if _CJK_RE.search(s):
        return crisp_text(s, SANS, size, color, **({"weight": BOLD} if bold else {}))
    s = "".join(_TEX_ESCAPE.get(c, c) for c in s)
    s = re.sub(r"√(\d+)", lambda m: r"$\sqrt{" + m[1] + "}$", s)
    s = re.sub("[" + re.escape("".join(_TEX_MATH)) + "]", lambda m: "$" + _TEX_MATH[m[0]] + "$", s)
    s = s.replace("$$", "")            # neighbouring math runs join: ±√3 is one formula
    s = s.replace("–", "--").replace("…", r"\dots{}")
    s = re.sub(r"  +", lambda m: " " + r"\ " * (len(m[0]) - 1), s)
    if bold:
        s = r"\textbf{" + s + "}"
    return Tex(s, font_size=size, color=color)


def num(s, size=22, color=C_TEXT):
    """A number on the picture (tick label, coordinate, value): LaTeX math with
    TEXT_FONT = "latex", so 2.2 on an axis looks like 2.2 in a formula;
    otherwise monospace."""
    if TEXT_FONT == "latex":
        return MathTex(str(s).replace("−", "-"), font_size=size, color=color)
    return mono(str(s), size, color)


def txt(s, size=30, color=C_TEXT, **kw):
    """Prose text: the caption font (handles Latin and CJK), or LaTeX with
    TEXT_FONT = "latex" in series.py (one typeface on the whole frame)."""
    if TEXT_FONT == "latex":
        return tex_text(s, TEX_LABEL if size <= 32 else size, color, bold=kw.get("weight") == BOLD)
    return crisp_text(s, SANS, size, color, **kw)


zh = txt  # alias


# ---------------------------------------------------------------- syntax highlight

REG_RE = re.compile(
    r"^(x([0-9]|[12][0-9]|3[01])|zero|ra|sp|gp|tp|fp|pc|t[0-6]|s([0-9]|1[01])|a[0-7])$"
)
ASM_TOKEN = re.compile(
    r"(?P<comment>#.*$)|(?P<ident>[A-Za-z_.][A-Za-z0-9_.]*)"
    r"|(?P<num>-?0x[0-9A-Fa-f_]+|-?\d+)|(?P<ws>\s+)|(?P<other>.)"
)
C_TOKEN = re.compile(
    r"(?P<comment>//.*$)|(?P<ident>[A-Za-z_][A-Za-z0-9_]*)"
    r"|(?P<num>0x[0-9A-Fa-f]+|\d+)|(?P<ws>\s+)|(?P<other>.)"
)
C_KEYWORDS = {
    "int", "char", "if", "else", "while", "for", "return", "void",
    "unsigned", "short", "long", "struct", "const", "static",
}
PY_TOKEN = re.compile(
    r"(?P<comment>#.*$)|(?P<ident>[A-Za-z_][A-Za-z0-9_]*)"
    r"|(?P<num>0x[0-9A-Fa-f]+|\d+(?:\.\d+)?)|(?P<str>'[^']*'|\"[^\"]*\")|(?P<ws>\s+)|(?P<other>.)"
)
PY_KEYWORDS = {
    "def", "return", "if", "elif", "else", "for", "while", "in", "not", "and", "or",
    "import", "from", "class", "None", "True", "False", "lambda", "with", "as", "yield",
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _cjk_spans(s: str) -> str:
    """Escape `s` for Pango markup, wrapping CJK runs in the CJK font (see mono())."""
    out, last = [], 0
    for m in CJK_RUN.finditer(s):
        out.append(esc(s[last:m.start()]))
        out.append(f'<span font_family="{SANS}">{esc(m.group())}</span>')
        last = m.end()
    out.append(esc(s[last:]))
    return "".join(out)


def span(s: str, color) -> str:
    if color is None:
        return _cjk_spans(s)
    return f'<span foreground="{hexc(color)}">{_cjk_spans(s)}</span>'


def highlight(line: str, lang: str = "asm") -> str:
    """Return Pango markup with syntax colors for one line of asm, c or python."""
    out = []
    seen_mnem = False
    regex = {"asm": ASM_TOKEN, "c": C_TOKEN, "python": PY_TOKEN}[lang]
    for m in regex.finditer(line):
        kind, tok = m.lastgroup, m.group()
        color = None
        if kind == "comment":
            color = C_COMMENT
        elif kind == "num":
            color = C_NUM
        elif kind == "ident":
            if lang == "asm":
                if line[m.end():m.end() + 1] == ":":
                    color = C_LABEL
                elif REG_RE.match(tok):
                    color = C_REG
                elif not seen_mnem:
                    color = C_MNEM
                    seen_mnem = True
                else:
                    color = C_LABEL
            elif tok in (PY_KEYWORDS if lang == "python" else C_KEYWORDS):
                color = C_KEYWORD
        elif kind == "str":
            color = C_LABEL
        elif kind == "other":
            color = GREY_A
        out.append(span(tok, color))
    return "".join(out)


class CodeListing(VGroup):
    """Monospace code block. Every line carries an invisible '|' strut so all
    lines share one height and one left edge, which keeps baselines and
    indentation consistent."""

    def __init__(self, lines, lang="asm", font_size=26, line_gap=0.5, **kw):
        super().__init__(**kw)
        # lines are translated whole (MarkupText can't be looked up), so the
        # table can keep the comment column aligned
        self.src = [tr(s) for s in lines]
        self.lang = lang
        self.lines = VGroup()
        for s in self.src:
            # Not oversampled: MarkupText lays out with a fixed Pango width, so a
            # 4x font size would wrap long lines. Monospace spacing is fine as is.
            t = MarkupText(
                "|" + highlight(s, lang), font=MONO, font_size=font_size,
                disable_ligatures=True,
            )
            t[0].set_opacity(0)
            self.lines.add(t)
        for i, t in enumerate(self.lines):
            t.move_to(DOWN * i * line_gap, aligned_edge=LEFT)
        self.add(self.lines)

    def __getitem__(self, i):
        return self.lines[i]

    def __len__(self):
        return len(self.lines)

    def glyphs(self, i, sub=None, occurrence=0) -> VGroup:
        """Glyphs of line i, or of the `occurrence`-th match of `sub` in it."""
        line, s = self.lines[i], self.src[i]
        if sub is None:
            return VGroup(*line[1:])
        start = 0
        for _ in range(occurrence + 1):
            idx = s.index(sub, start)
            start = idx + 1
        a = 1 + sum(1 for ch in s[:idx] if not ch.isspace())
        n = sum(1 for ch in sub if not ch.isspace())
        return VGroup(*line[a:a + n])

    def line_box(self, i, color=YELLOW_D, opacity=0.16, pad=0.25) -> Rectangle:
        h = self.lines[i].height * 1.3
        w = self.lines.width + 2 * pad
        r = Rectangle(width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=opacity)
        r.move_to([self.lines.get_center()[0], self.lines[i].get_center()[1], 0])
        return r

    def left_of(self, i, buff=0.3) -> np.ndarray:
        return np.array([self.lines.get_left()[0] - buff, self.lines[i].get_center()[1], 0])

    def right_of(self, i, buff=0.3) -> np.ndarray:
        return np.array([self.lines.get_right()[0] + buff, self.lines[i].get_center()[1], 0])


def pc_arrow(color=YELLOW_D) -> VMobject:
    return Arrow(LEFT * 0.6, ORIGIN, buff=0, color=color, stroke_width=6,
                 max_tip_length_to_length_ratio=0.45)


# ---------------------------------------------------------------- machine state (registers, memory)


class RegBox(VGroup):
    """A named register: `name [ value ]`."""

    def __init__(self, name, value=0, color=None, width=1.9, fmt="dec",
                 font_size=24, alias=None, name_width=None, **kw):
        super().__init__(**kw)
        self.fmt = fmt
        self.font_size = font_size
        self.value = value
        color = color or abi_color(name)
        self.color_ = color
        self.label = mono(name if alias is None else f"{name}", font_size, color)
        self.box = RoundedRectangle(
            corner_radius=0.06, width=width, height=0.52, stroke_color=color,
            stroke_width=2, fill_color=color, fill_opacity=0.08,
        )
        self.label.next_to(self.box, LEFT, buff=0.18)
        if name_width is not None:
            self.label.align_to(self.box.get_left() + LEFT * (0.18 + name_width), LEFT)
        self.val = self._text(value)
        self.add(self.box, self.label, self.val)

    def _fmt(self, v):
        if isinstance(v, str):
            return v
        if self.fmt == "hex":
            return hex32(v)
        return str(v)

    def _text(self, v):
        return mono(self._fmt(v), self.font_size, WHITE).move_to(self.box)

    def set(self, v) -> Animation:
        """Animate the displayed value changing to v (in place)."""
        self.value = v
        new = self._text(v)
        if new.width > self.box.width * 0.92:
            new.scale_to_fit_width(self.box.width * 0.92)
        return AnimationGroup(
            Transform(self.val, new),
            Indicate(self.box, color=self.color_, scale_factor=1.08),
        )

    def set_now(self, v):
        self.value = v
        new = self._text(v)
        self.val.become(new)
        return self


def reg_column(specs, buff=0.22, **kw) -> VGroup:
    """specs: list of (name, value). Returns a VGroup of RegBox aligned by box."""
    boxes = VGroup(*[RegBox(n, v, **kw) for n, v in specs])
    boxes.arrange(DOWN, buff=buff)
    for b in boxes[1:]:
        b.shift(RIGHT * (boxes[0].box.get_center()[0] - b.box.get_center()[0]))
    return boxes


class RegisterFile(VGroup):
    """All 32 integer registers in a 4 x 8 grid."""

    def __init__(self, cell_w=1.35, cell_h=0.46, font_size=20, values=None, **kw):
        super().__init__(**kw)
        self.font_size = font_size
        self.cells = VGroup()
        self.cell_h = cell_h
        self.names = VGroup()
        self.vals = VGroup()
        values = values or [0] * 32
        for i in range(32):
            col, row = divmod(i, 8)
            rect = Rectangle(width=cell_w, height=cell_h, stroke_color=GREY_B, stroke_width=1.5,
                             fill_color=GREY_E, fill_opacity=0.35)
            rect.move_to([col * (cell_w + 1.7), -row * (cell_h + 0.12), 0])
            name = mono(f"x{i}", font_size, GREY_A).next_to(rect, LEFT, buff=0.15)
            val = mono(str(values[i]), font_size, WHITE).move_to(rect)
            self.cells.add(rect)
            self.names.add(name)
            self.vals.add(val)
        self.add(self.cells, self.names, self.vals)

    def abi_label(self, i) -> Text:
        """ABI name for register i, sized and placed for the grid's current layout."""
        k = self.cells[i].height / self.cell_h
        lab = mono(ABI_NAMES[i], self.font_size, abi_color(ABI_NAMES[i])).scale(k)
        return lab.next_to(self.cells[i], LEFT, buff=0.15 * k)

    def set(self, i, v) -> Animation:
        new = mono(str(v), self.font_size, WHITE).move_to(self.cells[i])
        return Transform(self.vals[i], new)


# ---------------------------------------------------------------- memory


class MemoryView(VGroup):
    """A block of byte-addressed memory drawn as rows of `cols` bytes.

    Addresses increase left-to-right, then top-to-bottom (like a table)."""

    def __init__(self, base, rows, cols=4, data=None, cell_w=0.72, cell_h=0.46,
                 font_size=20, show_offsets=True, addr_color=GREY_B, **kw):
        super().__init__(**kw)
        self.base, self.rows_n, self.cols = base, rows, cols
        self.font_size = font_size
        data = data or {}
        self.cells = VGroup()
        self.texts = VGroup()
        self.addr_labels = VGroup()
        for r in range(rows):
            for c in range(cols):
                rect = Rectangle(width=cell_w, height=cell_h, stroke_color=GREY_B,
                                 stroke_width=1.5, fill_color=GREY_E, fill_opacity=0.3)
                rect.move_to([c * cell_w, -r * cell_h, 0])
                a = base + r * cols + c
                t = self._byte_text(data.get(a)).move_to(rect)
                self.cells.add(rect)
                self.texts.add(t)
            lab = mono(f"0x{base + r * cols:X}", font_size, addr_color)
            lab.next_to(self.cells[r * cols], LEFT, buff=0.2)
            self.addr_labels.add(lab)
        self.add(self.cells, self.texts, self.addr_labels)
        if show_offsets and cols > 1:
            self.offsets = VGroup(*[
                mono(f"+{c}", font_size - 4, GREY).next_to(self.cells[c], UP, buff=0.12)
                for c in range(cols)
            ])
            self.add(self.offsets)

    def _byte_text(self, v):
        s = "··" if v is None else f"{v & 0xFF:02X}"
        return mono(s, self.font_size, GREY if v is None else WHITE)

    def idx(self, addr):
        return addr - self.base

    def cell(self, addr):
        return self.cells[self.idx(addr)]

    def text(self, addr):
        return self.texts[self.idx(addr)]

    def word(self, addr) -> VGroup:
        return VGroup(*[self.cells[self.idx(addr) + k] for k in range(4)])

    def word_texts(self, addr) -> VGroup:
        return VGroup(*[self.texts[self.idx(addr) + k] for k in range(4)])

    def set_byte(self, addr, v) -> Animation:
        new = self._byte_text(v).move_to(self.cell(addr))
        return Transform(self.text(addr), new)

    def set_word(self, addr, v) -> AnimationGroup:
        return AnimationGroup(*[
            self.set_byte(addr + k, (v >> (8 * k)) & 0xFF) for k in range(4)
        ])

    def row_label(self, addr):
        return self.addr_labels[(addr - self.base) // self.cols]


class WordColumn(VGroup):
    """A column of word-sized cells with address labels; higher addresses on top
    (the usual picture for the stack)."""

    def __init__(self, top_addr, n, step=4, cell_w=2.6, cell_h=0.5, font_size=20, **kw):
        super().__init__(**kw)
        self.top_addr, self.step = top_addr, step
        self.cells = VGroup()
        self.texts = VGroup()
        self.addr_labels = VGroup()
        for i in range(n):
            rect = Rectangle(width=cell_w, height=cell_h, stroke_color=GREY_B, stroke_width=1.5,
                             fill_color=GREY_E, fill_opacity=0.3)
            rect.move_to(DOWN * i * cell_h)
            lab = mono(f"0x{top_addr - i * step:X}", font_size, GREY_B).next_to(rect, LEFT, buff=0.2)
            txt = mono("", font_size)
            txt.move_to(rect)
            self.cells.add(rect)
            self.addr_labels.add(lab)
            self.texts.add(txt)
        self.add(self.cells, self.addr_labels, self.texts)
        self.font_size = font_size

    def i_of(self, addr):
        return (self.top_addr - addr) // self.step

    def cell(self, addr):
        return self.cells[self.i_of(addr)]

    def set(self, addr, s, color=WHITE) -> Animation:
        i = self.i_of(addr)
        new = mono(s, self.font_size, color).move_to(self.cells[i])
        return Transform(self.texts[i], new)


# ---------------------------------------------------------------- instruction bits


class BitField(VGroup):
    """A 32-bit word drawn as colored fields (instruction formats, IEEE-754 ...).

    fields: list of (name, width, color[, label]) from bit 31 down to bit 0.
    """

    def __init__(self, fields, bits=None, box_w=0.36, box_h=0.56, font_size=22,
                 label_size=20, show_ranges=True, show_labels=True, **kw):
        super().__init__(**kw)
        assert sum(f[1] for f in fields) == 32, fields
        self.fields = fields
        self.box_w, self.box_h, self.font_size = box_w, box_h, font_size
        self.frames = VGroup()
        self.digits = VGroup()
        self.labels = VGroup()
        self.ranges = VGroup()
        self.field_digits = []
        self.bits = ["0" * f[1] for f in fields]
        x = 0.0
        hi = 31
        for f in fields:
            name, w, color = f[0], f[1], f[2]
            label = f[3] if len(f) > 3 else name
            frame = Rectangle(width=w * box_w, height=box_h, stroke_color=color,
                              stroke_width=2.5, fill_color=color, fill_opacity=0.14)
            frame.move_to([x + w * box_w / 2, 0, 0])
            seps = VGroup(*[
                Line([x + k * box_w, -box_h / 2, 0], [x + k * box_w, box_h / 2, 0],
                     stroke_color=color, stroke_width=0.8, stroke_opacity=0.5)
                for k in range(1, w)
            ])
            frame.add(seps)
            digs = VGroup()
            for k in range(w):
                d = mono("0", font_size, WHITE).move_to([x + (k + 0.5) * box_w, 0, 0])
                d.set_opacity(0)
                digs.add(d)
            self.field_digits.append(digs)
            self.digits.add(*digs)
            lab = (zh if any(ord(ch) > 0x2E7F for ch in label) else mono)(label, label_size, color)
            lab.next_to(frame, UP, buff=0.14)
            if lab.width > frame.width + 0.1:
                lab.scale_to_fit_width(frame.width + 0.1)
            self.labels.add(lab)
            lo = hi - w + 1
            rng = mono(f"{hi}" if w == 1 else f"{hi}:{lo}", label_size - 6, GREY)
            rng.next_to(frame, DOWN, buff=0.1)
            if rng.width > frame.width + 0.05:
                rng.scale_to_fit_width(frame.width + 0.05)
            self.ranges.add(rng)
            self.frames.add(frame)
            x += w * box_w
            hi = lo - 1
        self.add(self.frames, self.digits)
        if show_labels:
            self.add(self.labels)
        if show_ranges:
            self.add(self.ranges)
        self.center()
        if bits is not None:
            self.set_bits_now(bits)

    def field(self, i):
        return self.frames[i]

    def _digit(self, ch, ref):
        return mono(ch, self.font_size, WHITE).move_to(ref)

    def fill_field(self, i, bits: str) -> AnimationGroup:
        digs = self.field_digits[i]
        assert len(bits) == len(digs), (i, bits)
        self.bits[i] = bits
        anims = []
        for d, ch in zip(digs, bits):
            new = self._digit(ch, d.get_center())
            anims.append(Transform(d, new))
        return LaggedStart(*anims, lag_ratio=0.08)

    def set_bits_now(self, bits: str):
        bits = bits.replace(" ", "").replace("_", "")
        assert len(bits) == 32
        k = 0
        for i, f in enumerate(self.fields):
            self.bits[i] = bits[k:k + f[1]]
            k += f[1]
        for d, ch in zip(self.digits, bits):
            d.become(self._digit(ch, d.get_center()))
        return self


def fmt_fields(kind):
    """RV32 instruction formats (R I S B U J) as BitField field lists. A worked
    example of describing any 32-bit layout: list (name, width, color[, label])
    from the most significant field down."""
    F = FIELD_COLORS
    if kind == "R":
        return [("funct7", 7, F["funct7"]), ("rs2", 5, F["rs2"]), ("rs1", 5, F["rs1"]),
                ("funct3", 3, F["funct3"]), ("rd", 5, F["rd"]), ("opcode", 7, F["opcode"])]
    if kind == "I":
        return [("imm[11:0]", 12, F["imm"]), ("rs1", 5, F["rs1"]),
                ("funct3", 3, F["funct3"]), ("rd", 5, F["rd"]), ("opcode", 7, F["opcode"])]
    if kind == "S":
        return [("imm[11:5]", 7, F["imm"]), ("rs2", 5, F["rs2"]), ("rs1", 5, F["rs1"]),
                ("funct3", 3, F["funct3"]), ("imm[4:0]", 5, F["imm"]), ("opcode", 7, F["opcode"])]
    if kind == "B":
        return [("imm[12]", 1, F["imm"], "12"), ("imm[10:5]", 6, F["imm"], "imm[10:5]"),
                ("rs2", 5, F["rs2"]), ("rs1", 5, F["rs1"]), ("funct3", 3, F["funct3"]),
                ("imm[4:1]", 4, F["imm"], "imm[4:1]"), ("imm[11]", 1, F["imm"], "11"),
                ("opcode", 7, F["opcode"])]
    if kind == "U":
        return [("imm[31:12]", 20, F["imm"]), ("rd", 5, F["rd"]), ("opcode", 7, F["opcode"])]
    if kind == "J":
        return [("imm[20]", 1, F["imm"], "20"), ("imm[10:1]", 10, F["imm"]),
                ("imm[11]", 1, F["imm"], "11"), ("imm[19:12]", 8, F["imm"]),
                ("rd", 5, F["rd"]), ("opcode", 7, F["opcode"])]
    raise ValueError(kind)


# ---------------------------------------------------------------- ML / math diagrams


def nn_diagram(sizes=(3, 4, 2), layer_gap=2.2, node_gap=0.75, r=0.2):
    """Fully connected network: returns (group, layers, edges)."""
    layers = VGroup()
    for i, n in enumerate(sizes):
        col = VGroup(*[Circle(r, color=BLUE_B, fill_opacity=0.15, stroke_width=2) for _ in range(n)])
        col.arrange(DOWN, buff=node_gap - 2 * r).move_to(RIGHT * i * layer_gap)
        layers.add(col)
    edges = VGroup()
    for a, b in zip(layers[:-1], layers[1:]):
        for u in a:
            for v in b:
                edges.add(Line(u.get_right(), v.get_left(), stroke_width=1.2, stroke_opacity=0.5, color=GREY_B))
    g = VGroup(edges, layers).move_to(ORIGIN)
    return g, layers, edges


def heatmap(values, cell=0.8, cmap=(BLUE_E, YELLOW_D)):
    """Grid of squares colored by value in [0, 1] (attention weights, confusion matrix ...)."""
    rows = VGroup()
    for i, row in enumerate(values):
        for j, v in enumerate(row):
            sq = Square(cell, stroke_width=1, stroke_color=GREY_D)
            sq.set_fill(interpolate_color(ManimColor(cmap[0]), ManimColor(cmap[1]), v), 1)
            sq.move_to([j * cell, -i * cell, 0])
            rows.add(sq)
    return rows.center()


# ---------------------------------------------------------------- misc shapes


def bit_row(bits: str, color=BLUE_B, box=0.55, font_size=30) -> VGroup:
    """A row of bit boxes; returns VGroup(VGroup(square, digit), ...)."""
    row = VGroup()
    for k, ch in enumerate(bits):
        sq = Square(box, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.12)
        sq.move_to(RIGHT * k * box)
        d = mono(ch, font_size, WHITE if ch == "1" else GREY_B).move_to(sq)
        row.add(VGroup(sq, d))
    row.box, row.font_size = box, font_size
    return row


def set_bit_row(row: VGroup, bits: str) -> AnimationGroup:
    k = row[0][0].width / row.box
    return AnimationGroup(*[
        Transform(cell[1], mono(ch, row.font_size, WHITE if ch == "1" else GREY_B)
                  .scale(k).move_to(cell[0]))
        for cell, ch in zip(row, bits)
    ])


def alu_shape(width=1.6, height=1.2, color=BLUE_C, label="+") -> VGroup:
    w, h = width / 2, height / 2
    notch = 0.18 * width
    poly = Polygon(
        [-w, h, 0], [-notch, h, 0], [0, h - notch, 0], [notch, h, 0], [w, h, 0],
        [w * 0.55, -h, 0], [-w * 0.55, -h, 0],
        stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.12,
    )
    txt = mono(label, 30, color).move_to(poly.get_center() + DOWN * 0.1 * height)
    g = VGroup(poly, txt)
    g.in_left = np.array([-w * 0.55, h, 0])
    g.in_right = np.array([w * 0.55, h, 0])
    return g


def file_icon(name, color=BLUE_C, w=1.3, h=1.6, font_size=22) -> VGroup:
    fold = 0.3
    body = Polygon(
        [-w / 2, h / 2, 0], [w / 2 - fold, h / 2, 0], [w / 2, h / 2 - fold, 0],
        [w / 2, -h / 2, 0], [-w / 2, -h / 2, 0],
        stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.12,
    )
    corner = VMobject(stroke_color=color, stroke_width=2).set_points_as_corners(
        [[w / 2 - fold, h / 2, 0], [w / 2 - fold, h / 2 - fold, 0], [w / 2, h / 2 - fold, 0]])
    label = mono(name, font_size, WHITE).move_to(body)
    if label.width > w * 0.9:
        label.scale_to_fit_width(w * 0.9)
    return VGroup(body, corner, label)


def box_label(text, color=BLUE_C, w=None, h=0.8, font_size=28, font=None) -> VGroup:
    font = font or SANS
    t = crisp_text(text, font, font_size, WHITE)
    w = w or t.width + 0.6
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color,
                         stroke_width=3, fill_color=color, fill_opacity=0.15)
    t.move_to(r)
    return VGroup(r, t)


# ---------------------------------------------------------------- captions

_PUNCT_NO_START = "，。、；：！？）」』》”’,.;:!?)"


def _units(ch: str) -> float:
    return 1.0 if ord(ch) > 0x2E7F else 0.55


def text_units(s: str) -> float:
    return sum(_units(c) for c in s)


_BREAK_AFTER = "，。；：、！？）」』》,;:!?)…"
_NO_END = "“（「『《(\""


def _is_cjk(tok: str) -> bool:
    return len(tok) == 1 and ord(tok) > 0x2E7F


def wrap_caption(text: str, max_units: float = 30) -> str:
    """Wrap a mixed Chinese/English caption into balanced lines (small DP):
    prefer breaks after punctuation, never split an English word, never start
    a line with closing punctuation or end one with an opening quote."""
    total = text_units(text)
    if total <= max_units:
        return text
    # arrows count as word characters so routes like "S→B→A" never break mid-route
    toks = re.findall(r"[A-Za-zÀ-ɏ0-9_\-\.\[\]\(\)\{\}:+*/<>=#&|~^%',$→←]+|\s+|.", text)
    T = len(toks)
    INF = float("inf")

    def line_units(i, j):
        return text_units("".join(toks[i:j]).strip())

    def break_cost(i):
        last, nxt = toks[i - 1], toks[i]
        if nxt[0] in _PUNCT_NO_START or last in _NO_END:
            return INF
        if last in _BREAK_AFTER:
            return -8
        if _is_cjk(last) and _is_cjk(nxt):
            return 5
        return 0

    n0 = math.ceil(total / max_units)
    for n in (n0, n0 + 1, n0 + 2):
        target = total / n
        dp = [[INF] * (T + 1) for _ in range(n + 1)]
        back = [[0] * (T + 1) for _ in range(n + 1)]
        dp[0][0] = 0.0
        for k in range(1, n + 1):
            for i in range(1, T + 1):
                bc = 0.0 if i == T else break_cost(i)
                if bc == INF:
                    continue
                for j in range(i):
                    if dp[k - 1][j] == INF:
                        continue
                    u = line_units(j, i)
                    if u > max_units + 1 or u == 0:
                        continue
                    c = dp[k - 1][j] + 1.2 * abs(u - target) + bc
                    if c < dp[k][i]:
                        dp[k][i], back[k][i] = c, j
        if dp[n][T] < INF:
            cuts, i = [], T
            for k in range(n, 0, -1):
                j = back[k][i]
                cuts.append("".join(toks[j:i]).strip())
                i = j
            return "\n".join(reversed(cuts))
    return text


def reading_time(text: str, cps: float = 5.2) -> float:
    cjk = sum(1 for c in text if ord(c) > 0x2E7F)
    other = len(re.findall(r"[A-Za-z0-9_]+", text))
    if cjk == 0:
        return max(1.8, 0.5 + other * 0.3)   # Latin: ~200 words per minute
    return max(1.8, 0.5 + cjk / cps + other * 0.28)


def sentences(text: str) -> list[str]:
    """The sentences of one paragraph of narration (Latin or CJK)."""
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z\"“(]|[^\x00-\x7f])|(?<=[。？！])\s*", text.strip())
    return [x for x in parts if x]


def split_cue(text: str, max_units: float = 46) -> list[str]:
    """Cut one narration beat into subtitle-sized cues (two caption lines at
    most; widths in CJK-character units, a Latin letter is 0.55): whole
    sentences where they fit, otherwise at commas, otherwise between words.
    Sentences are never merged, so a cue is one sentence or a part of one."""
    def join(a, b):
        cjk_edge = ord(a[-1]) > 0x2E7F or ord(b[0]) > 0x2E7F
        return a + ("" if cjk_edge else " ") + b

    def pack(parts):
        out = []
        for part in parts:
            if out and text_units(join(out[-1], part)) <= max_units:
                out[-1] = join(out[-1], part)
            else:
                out.append(part)
        return out

    def words(clause):   # Latin words, or CJK characters when there are no spaces
        parts = clause.split()
        return parts if len(parts) > 1 else list(clause)

    cues = []
    for sent in re.split(r"(?<=[.?!])\s+|(?<=[。？！])\s*", text.strip()):
        if not sent:
            continue
        if text_units(sent) <= max_units:
            cues.append(sent)
            continue
        for clause in pack([c for c in re.split(r"(?<=[,;:])\s+|(?<=[，；：])\s*", sent) if c]):
            cues += [clause] if text_units(clause) <= max_units else pack(words(clause))
    return cues


class NarratedScene(MovingCameraScene):
    """Scene with timed captions (burned in unless BURN_CAPTIONS is off, and
    always exported as .srt), an optional voice-over, title / end cards, and a
    camera that can move onto the point being talked about."""

    caption_size = 30 if LANG in CJK_LANGS else 28
    caption_units = 30 if LANG in CJK_LANGS else 35   # line width in CJK-character units
    caption_y = -3.42
    series = ""      # series tag on the title card when there is no series.py

    def setup(self):
        self.camera.background_color = BG
        self._cap = None
        self._cap_text = None
        self._cap_t0 = 0.0
        self._cap_need = 0.0
        self._cap_span = 0.0
        self._cap_src = None
        self._sched = []
        self._noted = set()
        self._home = (self.camera.frame.get_center().copy(), self.camera.frame.width)
        name = type(self).__name__
        self.episode = _BY_SCENE.get(name)
        m = re.match(r"Ep(\d+)", name)
        self.ep_no = self.episode["num"] if self.episode else (int(m[1]) if m else 0)
        load_table(self.ep_no)

    # -- fast-forward (for previews of a scene that builds on the stage of earlier ones)
    _ff = False

    def fast_forward(self, *methods):
        """Run scene methods without rendering, voice or captions: every
        animation jumps to its end state and no time passes."""
        self._ff = True
        try:
            for m in methods:
                m()
        finally:
            self._ff = False

    def preview_only(self, *chains):
        """For scripts/preview.py: when KIT_ONLY names scene methods, run just
        those (no title or end card) and return True. Each chain lists scenes that
        draw on one shared stage, in order; the ones before the requested scene are
        fast-forwarded so it finds the stage as it expects.

            def construct(self):
                if self.preview_only(["graph", "slopes", "basins"]):
                    return
                self.title_card() ...
        """
        only = [s for s in os.environ.get("KIT_ONLY", "").split(",") if s]
        if not only:
            return False
        for chain in chains:
            if only[0] in chain[1:]:
                self.fast_forward(*[getattr(self, s) for s in chain[:chain.index(only[0])]])
        for s in only:
            getattr(self, s)()
        self.uncaption()
        return True

    def play(self, *args, **kwargs):
        if not self._ff:
            self._beat_plays += 1
            return super().play(*args, **kwargs)
        from manim.animation.animation import prepare_animation
        anims = [prepare_animation(a) for a in args]
        self.add_mobjects_from_animations(anims)   # as a real play() does, so removers find their mobject
        for a in anims:
            a._setup_scene(self)
            a.begin()
        for a in anims:
            a.finish()
            a.clean_up_from_scene(self)

    def wait(self, *args, **kwargs):
        if not self._ff:
            return super().wait(*args, **kwargs)

    # -- checks (see the module docstring): findings go to stderr, the render goes on
    _beat_no = 0
    _beat_plays = 0
    _beat_had = set()
    _TEXT_TYPES = (Text, MarkupText, SingleStringMathTex)   # MathTex and Tex are the last

    def _note(self, tag, msg):
        key = (tag, msg) if tag == "layout" else (tag, self._beat_no, msg)   # a lasting flaw is said once
        if key not in self._noted:
            self._noted.add(key)
            head = (self._cap_src or "")[:44]
            print(f"[{tag}] beat {self._beat_no} \"{head}\": {msg}", file=sys.stderr, flush=True)

    @staticmethod
    def _ink_box(mob):
        """(x0, y0, x1, y1) of what `mob` actually draws, or None if nothing shows."""
        pts = [f.points for f in mob.family_members_with_points()
               if f.get_fill_opacity() > 0.05 or (f.get_stroke_opacity() > 0.05 and f.get_stroke_width() > 0)]
        if not pts:
            return None
        pts = np.vstack(pts)
        return pts[:, 0].min(), pts[:, 1].min(), pts[:, 0].max(), pts[:, 1].max()

    def _stage(self):
        """(texts, shapes) on stage now: texts as (name, ink box, is it code), shapes as
        the visible non-text mobjects with points. The caption and headings are left out."""
        texts, shapes = [], []

        def walk(m):
            if m is self._cap or getattr(m, "_kit_ui", False):
                return
            if isinstance(m, self._TEXT_TYPES):
                box = self._ink_box(m)
                if box is not None:
                    name = (getattr(m, "original_text", None) or getattr(m, "text", None)
                            or getattr(m, "tex_string", "") or "?")
                    texts.append((" ".join(str(name).split())[:28], box, isinstance(m, MarkupText)))
                return
            if isinstance(m, VMobject) and len(m.points) and (
                    m.get_fill_opacity() > 0.05 or (m.get_stroke_opacity() > 0.05 and m.get_stroke_width() > 0)):
                shapes.append(m)
            for sub in m.submobjects:
                walk(sub)

        for m in self.mobjects:
            walk(m)
        return texts, shapes

    def _layout_check(self):
        if not CHECKS or self._ff:
            return
        try:
            texts, shapes = self._stage()
            # what the beat has shown so far (a stage cleared for the next beat is not "empty")
            self._beat_had |= {"shape"} if shapes else set()
            self._beat_had |= {"code" if code else "text" for _, _, code in texts}
            texts = [(n, b) for n, b, _ in texts]
            seen = set()
            for s in shapes:   # the same geometry twice: parallel edges, a copy left behind
                if not (s.get_stroke_opacity() > 0.05 and s.get_stroke_width() > 0):
                    continue
                key = (type(s).__name__, np.round(s.points, 2).tobytes())
                if key in seen:
                    x, y = s.get_center()[:2]
                    self._note("layout", f"two {type(s).__name__} shapes exactly on top of each other near "
                                         f"({x:.1f}, {y:.1f}): only one is visible")
                seen.add(key)
                if not texts:
                    continue
                p = s.points   # a stroke through a text
                if len(p) <= 8:
                    p = np.linspace(p[0], p[-1], 40)
                for name, (x0, y0, x1, y1) in texts:
                    inside = ((p[:, 0] > x0 + 0.03) & (p[:, 0] < x1 - 0.03)
                              & (p[:, 1] > y0 + 0.03) & (p[:, 1] < y1 - 0.03)).sum()
                    if inside >= 2:
                        self._note("layout", f"a {type(s).__name__} runs through the text '{name}'")
            fr = self.camera.frame
            c, w = self._home
            if abs(fr.width - w) < 1e-6 and np.allclose(fr.get_center(), c):   # not while zoomed in
                hw, hh = w / 2, w * 9 / 32
                for name, (x0, y0, x1, y1) in texts:
                    if x0 < c[0] - hw - 0.02 or x1 > c[0] + hw + 0.02 or y1 > c[1] + hh + 0.02:
                        self._note("layout", f"off the frame: '{name}'")
                    elif y0 < c[1] - 3.0:
                        self._note("layout", f"in the subtitle band (below y = -2.9): '{name}'")
            pad = 0.04   # touching is fine; text has to share real area
            for i, (a, (ax0, ay0, ax1, ay1)) in enumerate(texts):
                for b, (bx0, by0, bx1, by1) in texts[i + 1:]:
                    iw = min(ax1, bx1) - max(ax0, bx0) - 2 * pad
                    ih = min(ay1, by1) - max(ay0, by0) - 2 * pad
                    if iw <= 0 or ih <= 0:
                        continue
                    small = min((ax1 - ax0) * (ay1 - ay0), (bx1 - bx0) * (by1 - by0))
                    if small > 0 and iw * ih > 0.15 * small:
                        self._note("layout", f"overlapping text: '{a}' and '{b}'")
        except Exception as e:   # a check must never break a render
            self._note("layout", f"check skipped ({type(e).__name__}: {e})")

    def _beat_report(self):
        """The beat on stage has been spoken: look at its picture and at how much moved."""
        if not CHECKS or self._ff or self._cap_text is None:
            return
        self._layout_check()
        if not self._beat_had:
            self._note("empty", "nothing was on the stage during this beat")
        elif self._beat_had == {"text"}:
            self._note("textonly", "only words were on the stage during this beat: build the thing "
                                   "the words describe (boxes, arrows, a graph) and change it")
        talk, n = self._cap_span, self._beat_plays
        if n < (3 if talk > 26 else 2 if talk > 14 else 0):
            self._note("still", f"{talk:.0f} s of narration with {n} animation step(s): add cue()s "
                                f"so the picture changes as things are named")

    # -- captions
    _cap_units_cache = {}

    def _cap_units(self):
        """caption_units, lowered when the font that is really in use (a fallback, say)
        is wider than the estimate, so the wrap and the cue split agree on two lines."""
        key = (SANS, self.caption_size, LANG)
        if key not in self._cap_units_cache:
            sample = ("这是一行用来测量字幕宽度的示例文字" if LANG in CJK_LANGS
                      else "The quick brown fox jumps over the lazy dog, then walks home.")
            per_unit = Text(sample, font=SANS, font_size=self.caption_size).width / text_units(sample)
            self._cap_units_cache[key] = min(self.caption_units, int(10.2 / per_unit))
        return self._cap_units_cache[key]

    def _make_caption(self, text):
        # Pango wraps an oversampled line wider than ~10.6 units by itself and draws its
        # last word over the next line: narrow the wrap until every line is inside.
        units = self._cap_units()
        while True:
            wrapped = wrap_caption(text, units)
            widest = max(Text(ln, font=SANS, font_size=self.caption_size).width for ln in wrapped.split("\n"))
            if widest <= 10.4 or units <= 12:
                break
            units -= 2
        t = crisp_text(wrapped, SANS, self.caption_size, C_TEXT, line_spacing=0.9)
        t.move_to([0, self.caption_y, 0])
        if t.get_bottom()[1] < -3.92:
            t.shift(UP * (-3.92 - t.get_bottom()[1]))
        bg = BackgroundRectangle(t, color=BG, fill_opacity=0.72, buff=0.12)
        return VGroup(bg, t)

    def _flush(self):
        if self._cap is None and self._cap_text is None:
            return
        remaining = self._cap_need - (self.time - self._cap_t0)
        if remaining > 0.02:
            self.wait(remaining)

    def _cue_times(self):
        """The subtitle cues of the current beat with the time each starts and
        ends (scene time): one per sentence, at the moment the voice says it;
        a sentence too long for two caption lines is cut at commas and shares
        its time by length."""
        cues, starts, ends = [], [], []
        for k, (_, _, sent, t, d) in enumerate(self._sched):
            end = self._sched[k + 1][3] if k + 1 < len(self._sched) else t + d + PACE["beat"]
            end = min(end, t + d + 1.5)
            parts = split_cue(sent, self._cap_units() * 2 - 4)
            total = sum(len(c) for c in parts)
            whole = end - t
            for c in parts:
                span = whole * len(c) / total
                cues.append(c)
                starts.append(self._cap_t0 + t)
                ends.append(self._cap_t0 + t + span)
                t += span
        return cues, starts, ends

    def _close_sub(self):
        if self._cap is not None:
            self._cap.clear_updaters()
        if getattr(self, "_cap_tick", None) is not None:
            self.remove_updater(self._cap_tick)
            self._cap_tick = None
        if self._cap_text is not None:
            now = self.time
            # one .srt cue per sentence, timed like the voice and the burned caption
            for c, a, b in zip(*self._cue_times()):
                if min(b, now) > a:
                    self.add_subcaption(c, duration=min(b, now) - a, offset=a - now)
            self._cap_text = None
            self._sched = []

    def _caption_reel(self):
        """The burned caption of a beat: one sentence at a time, switching as
        the voice reaches each (same split and times as the .srt). A beat of
        one short sentence is one static caption."""
        cues, starts, _ = self._cue_times()
        frames = [self._make_caption(c) for c in cues]
        if len(frames) == 1:
            return frames[0]

        # All sentences sit in one group and only the current one is opaque. (Swapping
        # the group's children instead leaves the old ones on screen: Manim flattens
        # families when an animation starts.)
        def show(f, on):
            f[0].set_fill(BG, opacity=0.72 if on else 0)
            f[1].set_fill(opacity=1 if on else 0)

        for f in frames[1:]:
            show(f, False)
        holder = VGroup(*frames)
        t0 = self._cap_t0
        state = {"k": 0, "clock": t0}

        def tick(dt):   # a scene updater: Scene.time stands still inside an animation,
            state["clock"] += dt   # and mobject updaters are suspended while they animate
            k = sum(1 for s in starts if s <= state["clock"] + 1e-6) - 1
            if k != state["k"] and k >= 0:
                show(frames[state["k"]], False)
                show(frames[k], True)
                state["k"] = k
            elif state["k"] > 0 and state["clock"] - t0 > 0.45:
                # the FadeIn that brought the caption in keeps re-applying its end state
                # (first sentence on) until the play it belongs to is over: say it again
                show(frames[0], False)
                show(frames[state["k"]], True)
        holder.add_updater(lambda m, dt: None)   # marks the caption as moving, so it is redrawn
        self.add_updater(tick)
        self._cap_tick = tick
        return holder

    def voice(self, text, speak=None, delay=0.15) -> float:
        """Start speaking `text` now as one clip (no-op unless KIT_TTS=1) and
        return how long the voice keeps talking. For a line outside the beats;
        say() schedules its own voice sentence by sentence."""
        if not TTS or not text:
            return 0.0
        import tts
        path, dur = tts.synth(text, LANG, speak=tr(speak) if speak else None)
        self.add_sound(str(path), time_offset=delay)
        return delay + dur

    def _speak(self, paras, speak):
        """Schedule the voice-over of one beat sentence by sentence, with a
        pause after each (longer at the end of a paragraph), and return
        (schedule, seconds until the voice has finished). The schedule holds
        (first char, last char, sentence, start, duration) with character
        positions in the beat's text: cue() and the subtitles read it."""
        text = " ".join(paras)
        sents = [(x, k == len(ss) - 1) for ss in map(sentences, paras) for k, x in enumerate(ss)]
        said = [x for sp in (tr(speak).split("\n") if speak else []) for x in sentences(sp)]
        if len(said) != len(sents):
            if said:
                print(f"[narration] speak= has {len(said)} sentences, the text {len(sents)}: "
                      f"speaking the text instead", file=sys.stderr)
            said = [None] * len(sents)
        sched, t, pos = [], 0.15, 0
        for (x, last), sp in zip(sents, said):
            if TTS:
                import tts
                path, dur = tts.synth(x, LANG, speak=sp)
                self.add_sound(str(path), time_offset=t)
            else:   # silent render: about the time the sentence takes to say
                cjk = sum(1 for c in x if ord(c) > 0x2E7F)
                dur = 0.3 + cjk / 5.2 + 0.36 * len(re.findall(r"[A-Za-z0-9_]+", x))
            at = text.find(x, pos)
            at = pos if at < 0 else at
            sched.append((at, at + len(x), x, t, dur))
            pos = at + len(x)
            t += dur + PACE["paragraph" if last else "sentence"]
        return sched, (sched[-1][3] + sched[-1][4] if sched else 0.0)

    def say(self, text, *anims, need=None, extra=0.0, run_time=None, speak=None):
        """Start the beat `text` (after the previous one has been spoken, plus a
        pause) while playing `anims`. The voice reads it sentence by sentence
        with a pause after each; a line break in the text is a paragraph and
        gets a longer pause. `speak=` gives other words to voice (same number
        of sentences as the text)."""
        if run_time is not None:
            for a in anims:
                a.run_time = run_time
        try:  # optional: wording from narration.md (see narration.py)
            import narration
            text, speak = narration.apply(sys._getframe(1), text, speak)
        except ImportError:
            pass
        src = " ".join(x.strip() for x in text.split("\n") if x.strip())
        paras = [x.strip() for x in tr(text).split("\n") if x.strip()]
        text = " ".join(paras)
        self._flush()
        self._beat_report()
        self._close_sub()
        old = self._cap
        self._cap_t0 = self.time
        if self._ff:   # fast-forward: put the beat's end state on stage, silently, in no time
            self.play(*anims)
            return
        self._sched, talk = self._speak(paras, speak)
        self._cap_span = talk
        self._cap_need = max(need or 0.0, talk + PACE["beat"]) + extra
        self._cap_text, self._cap_src = text, src
        new = self._caption_reel() if BURN_CAPTIONS else None
        if new is not None:
            self._to_screen(new)
        # A sentence reel is added, not faded in: a FadeIn sharing a play() with longer
        # `anims` keeps restoring the first sentence after the reel has moved on (a ghost).
        reel = new is not None and not isinstance(new[0], BackgroundRectangle)
        if reel:
            self.add(new)
        swap = [FadeIn(new, run_time=0.4)] if new is not None and not reel else []
        if old is not None:
            swap.append(FadeOut(old, run_time=0.3))
        self._cap = new
        if swap or anims:
            self.play(*swap, *anims)
        self._beat_no += 1
        self._beat_plays = 1 if anims else 0
        self._beat_had = set()
        self._layout_check()

    def cue(self, phrase, *anims, run_time=None, lead=0.3):
        """Play `anims` when the voice reaches `phrase` (words of the current
        beat): the sentence that holds the phrase has a known start, and the
        phrase's place inside that sentence gives the rest. For long beats:
        say() starts the line, cue() adds each step as it is said."""
        if not self._ff:
            text, src = self._cap_text or "", self._cap_src or ""
            i = text.find(phrase)
            if i < 0 and src.find(phrase) >= 0:
                # a translated render: the phrase is in the source text; use the same
                # place, proportionally, in the translation (no table entry needed)
                i = int(src.find(phrase) / len(src) * len(text))
            if i < 0 or not self._sched:
                print(f"[cue] phrase not in the current line: {phrase!r}", file=sys.stderr)
            else:
                c0, c1, _, t, d = next((x for x in self._sched if x[0] <= i < x[1]), self._sched[-1])
                dt = self._cap_t0 + t + d * max(0, i - c0) / max(1, c1 - c0) - lead - self.time
                if dt > 0.05:
                    self.wait(dt)
        if anims:
            self.play(*anims, **({} if run_time is None else {"run_time": run_time}))
            self._layout_check()

    # -- camera
    def zoom_to(self, target, *anims, width=None, margin=1.6, run_time=2.0):
        """Move the camera onto `target` (a mobject or a point), playing `anims`
        with the move. `width` is the frame width to end with; by default what
        the target needs, times `margin`. The subtitle stays where it is on the
        screen; pin() anything else that should (a formula kept in a corner)."""
        fr = self.camera.frame
        if isinstance(target, Mobject):
            c = target.get_center()
            w = width or max(target.width * margin, target.height * margin * 16 / 9, 1.0)
        else:
            c, w = np.array(target, dtype=float), width or 4.0
        if self._cap is not None and not hasattr(self._cap, "_pin"):
            self.pin(self._cap)
        self.play(fr.animate.set(width=w).move_to(c), *anims, run_time=run_time)

    def zoom_back(self, *anims, run_time=1.6):
        """Return the camera to the whole frame."""
        c, w = self._home
        if self._cap is not None and not hasattr(self._cap, "_pin"):
            self.pin(self._cap)
        self.play(self.camera.frame.animate.set(width=w).move_to(c), *anims, run_time=run_time)

    def pin(self, mob):
        """Keep `mob` where it is on the screen, at the size it has there,
        while the camera moves."""
        fr = self.camera.frame
        mob._pin = [mob.get_center() - fr.get_center(), fr.width, 1.0]

        def stay(m):
            rel, w0, cur = m._pin
            k = fr.width / w0
            if abs(k - cur) > 1e-9:
                m.scale(k / cur)
                m._pin[2] = k
            m.move_to(fr.get_center() + rel * k)

        mob.add_updater(stay)
        return mob

    def _to_screen(self, mob):
        """`mob` was laid out for the whole frame: put it at the same place on
        the screen when the camera is somewhere else, and keep it there."""
        fr = self.camera.frame
        c, w = self._home
        k = fr.width / w
        if abs(k - 1) < 1e-6 and np.allclose(fr.get_center(), c):
            return mob
        rel = mob.get_center() - c
        mob.scale(k).move_to(fr.get_center() + rel * k)
        return self.pin(mob)

    def hold(self, extra=0.0):
        """Wait until the current caption has been read (and spoken), plus `extra`."""
        self._flush()
        self._layout_check()
        if extra > 0:
            self.wait(extra)

    def uncaption(self):
        self._flush()
        self._beat_report()
        self._close_sub()
        if self._cap is not None:
            self.play(FadeOut(self._cap, run_time=0.3))
            self._cap = None

    def clear_stage(self, *keep, run_time=0.8):
        """Fade out everything except the caption and `keep`."""
        self._layout_check()
        keep_ids = {id(m) for k in keep for m in k.get_family()}
        mobs = [m for m in self.mobjects
                if m is not self._cap and id(m) not in keep_ids]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    # -- set pieces
    def heading(self, text, color=YELLOW_D) -> VGroup:
        t = txt(text, 34, color)
        t.to_corner(UL, buff=0.45)
        line = Line(t.get_left(), t.get_right(), stroke_color=color, stroke_width=2)
        line.next_to(t, DOWN, buff=0.1)
        head = VGroup(t, line)
        head._kit_ui = True      # not part of the picture (see the checks)
        return head

    def title_card(self, ep=None, title=None, subtitle=None):
        """Series tag + "Episode n" + title (+ subtitle), spoken with a
        voice-over. With series.py all three come from there; pass ep=None and
        a title for a one-off video."""
        e = self.episode
        if e is not None:
            ep = self.ep_no if ep is None else ep
            title = title or e["title"].get(LANG) or e["title"][SOURCE_LANG]
            subtitle = subtitle or (e.get("sub") or {}).get(LANG)
        else:
            title, subtitle = tr(title), tr(subtitle)
        head = []
        tag = series_name() or self.series
        if tag:
            head.append(txt(tag, 28, GREY_B))
        if ep is not None:
            head.append(txt(S("episode", n=ep), 30, YELLOW_D))
        t = crisp_text(title, SANS, 60, WHITE, weight=BOLD)
        if t.width > 12.5:
            t.scale_to_fit_width(12.5)
        sub = txt(subtitle, 30, GREY_A) if subtitle else None
        if sub is not None and sub.width > 12.5:
            sub.scale_to_fit_width(12.5)
        grp = VGroup(*head, t, *([sub] if sub else [])).arrange(DOWN, buff=0.4)
        if head:
            self.play(*[FadeIn(p, shift=DOWN * 0.3) for p in head])
        t0 = self.time
        talk = self.voice(S("say_episode", n=ep, t=title) if ep is not None else title)
        self.play(Write(t), run_time=1.6)
        if sub:
            self.play(FadeIn(sub, shift=UP * 0.2))
        self.wait(max(1.6, talk + 0.5 - (self.time - t0)))
        self.play(FadeOut(grp, shift=UP * 0.3))

    def end_card(self, lines, next_title=None, footer=None):
        """Recap bullets, then "Next: ..." -- or, on the last episode of
        series.py, "The End". Also closes the last caption (for the .srt)."""
        self.uncaption()
        self.clear_stage()
        lines = [tr(s) for s in lines]
        head = txt(S("summary"), 40, YELLOW_D)
        items = VGroup(*[
            VGroup(Dot(color=YELLOW_D, radius=0.06), txt(s, 30)).arrange(RIGHT, buff=0.25)
            for s in lines
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        grp = VGroup(head, items).arrange(DOWN, buff=0.5)
        if grp.height > 6.4:
            grp.scale_to_fit_height(6.4)
        if grp.width > 13.0:
            grp.scale_to_fit_width(13.0)
        grp.move_to(UP * 0.35)
        talk = self.voice(S("say_summary"))
        self.play(FadeIn(head, shift=DOWN * 0.2))
        if talk > 1.05:
            self.wait(talk - 1.0)
        for it, s in zip(items, lines):
            t0 = self.time
            talk = self.voice(s)
            self.play(FadeIn(it, shift=RIGHT * 0.2), run_time=0.6)
            self.wait(max(reading_time(s) * 0.8, talk + 0.3) - (self.time - t0))
        self.wait(1.5)
        spoken = None
        if footer is None and next_title is None and self.episode is not None:
            k = self.ep_no
            if k < len(EPISODES):
                e = EPISODES[k]
                next_title = e["title"].get(LANG) or e["title"][SOURCE_LANG]
            else:
                footer = S("end", s=series_name())
                spoken = S("say_end", s=series_name())
        if next_title and not footer:
            footer, spoken = S("next", t=tr(next_title)), S("say_next", t=tr(next_title))
        if footer:
            nxt = txt(footer, 30, GREY_A).to_edge(DOWN, buff=0.5)
            t0 = self.time
            talk = self.voice(spoken or footer)
            self.play(FadeIn(nxt, shift=UP * 0.2))
            self.wait(max(2.2, talk + 0.8 - (self.time - t0)))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.5)


# ---------------------------------------------------------------- binary-encoding helpers


def bits_to_hex(bits: str) -> str:
    return f"0x{int(bits, 2):08X}"


class FormatScene(NarratedScene):
    """NarratedScene plus helpers for animating fixed-width binary encodings
    (instruction formats, floating point fields, packet headers ...)."""

    def encode(self, bf, fills, note_size=20, rt=0.9):
        """fills: list of (field index, bits, note). Returns the note mobjects."""
        notes = VGroup()
        for i, bits, note in fills:
            anims = [bf.fill_field(i, bits)]
            if note:
                n = mono(note, note_size, bf.fields[i][2]).next_to(bf.ranges[i], DOWN, buff=0.12)
                if n.width > bf.frames[i].width + 0.3:
                    n.scale_to_fit_width(bf.frames[i].width + 0.3)
                notes.add(n)
                anims.append(FadeIn(n, shift=UP * 0.1))
            self.play(*anims, run_time=rt)
        return notes

    def hex_of(self, bf, y_below, color=YELLOW_D, size=34):
        """Group the 32 digits into nibbles and show the hex value under them."""
        bits = "".join(bf.bits)
        hx = f"{int(bits, 2):08X}"
        nibbles = VGroup()
        anims = []
        for k in range(8):
            grp = VGroup(*bf.digits[4 * k:4 * k + 4])
            h = mono(hx[k], size, color)
            h.move_to([grp.get_center()[0], y_below, 0])
            nibbles.add(h)
            anims.append(TransformFromCopy(grp, h))
        seps = VGroup(*[
            Line(UP * 0.25, DOWN * 0.25, stroke_color=GREY, stroke_width=1.5).move_to(
                [(bf.digits[4 * k - 1].get_center()[0] + bf.digits[4 * k].get_center()[0]) / 2, y_below, 0])
            for k in range(1, 8)
        ])
        self.play(LaggedStart(*anims, lag_ratio=0.1), FadeIn(seps), run_time=1.6)
        final = mono(f"0x{hx}", size + 6, color).move_to([bf.get_center()[0], y_below, 0])
        self.play(ReplacementTransform(nibbles, final[2:]), FadeIn(final[:2]), FadeOut(seps))
        return final

    def fly_bits(self, row, bf, routes, run_time=1.8):
        """Fly digits from a source bit_row into BitField fields.

        routes: list of (field index, [source cell indices]) filling the field
        left to right. Copies land on the field's digit slots, then the field is
        committed so it can be read back (bf.bits) later."""
        copies, fills = [], []
        for fi, srcs in routes:
            slots = bf.field_digits[fi]
            for slot, k in zip(slots, srcs):
                c = row[k][1].copy()
                copies.append((c, slot))
            fills.append((fi, "".join(row[k][1].text for k in srcs)))
        self.play(LaggedStart(*[c.animate.match_height(p).move_to(p).set_color(WHITE) for c, p in copies],
                              lag_ratio=0.05), run_time=run_time)
        for fi, bits in fills:
            self.play(bf.fill_field(fi, bits), run_time=0.01)
        self.remove(*[c for c, _ in copies])
