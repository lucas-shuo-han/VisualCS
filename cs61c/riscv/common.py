"""Shared building blocks for the CS61C RISC-V video series.

Every episode is a single `NarratedScene`: captions are timed so each one stays
on screen long enough to read, and are also exported as an .srt file next to
the rendered video (handy for adding a voice-over later).
"""

from __future__ import annotations

import math
import re

from manim import *

# ---------------------------------------------------------------- fonts & palette

CJK = "Noto Sans CJK SC"
MONO = "DejaVu Sans Mono"
BG = "#0B0D12"

config.background_color = BG

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


def mono(s, size=24, color=C_TEXT, **kw) -> Text:
    return Text(s, font=MONO, font_size=size, color=color, disable_ligatures=True, **kw)


def zh(s, size=30, color=C_TEXT, **kw) -> Text:
    return Text(s, font=CJK, font_size=size, color=color, **kw)


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


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def span(s: str, color) -> str:
    if color is None:
        return esc(s)
    return f'<span foreground="{hexc(color)}">{esc(s)}</span>'


def highlight(line: str, lang: str = "asm") -> str:
    """Return Pango markup with syntax colors for one line of asm or C."""
    out = []
    seen_mnem = False
    regex = ASM_TOKEN if lang == "asm" else C_TOKEN
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
            elif tok in C_KEYWORDS:
                color = C_KEYWORD
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
        self.src = list(lines)
        self.lang = lang
        self.lines = VGroup()
        for s in self.src:
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


# ---------------------------------------------------------------- registers


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
    """A 32-bit instruction drawn as colored fields.

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
    """Standard RV32 instruction formats as BitField field lists."""
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


def box_label(text, color=BLUE_C, w=None, h=0.8, font_size=28, font=CJK) -> VGroup:
    t = Text(text, font=font, font_size=font_size, color=WHITE)
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
    toks = re.findall(r"[A-Za-z0-9_\-\.\[\]\(\)\{\}:+*/<>=#&|~^%',$]+|\s+|.", text)
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
    return max(1.8, 0.5 + cjk / cps + other * 0.28)


class NarratedScene(Scene):
    """Scene with timed, burned-in captions (also exported as .srt)."""

    caption_size = 30
    caption_y = -3.42

    def setup(self):
        self.camera.background_color = BG
        self._cap = None
        self._cap_text = None
        self._cap_t0 = 0.0
        self._cap_need = 0.0

    # -- captions
    def _make_caption(self, text):
        t = Text(wrap_caption(text), font=CJK, font_size=self.caption_size,
                 color=C_TEXT, line_spacing=0.9)
        t.move_to([0, self.caption_y, 0])
        if t.get_bottom()[1] < -3.92:
            t.shift(UP * (-3.92 - t.get_bottom()[1]))
        bg = BackgroundRectangle(t, color=BG, fill_opacity=0.72, buff=0.12)
        return VGroup(bg, t)

    def _flush(self):
        if self._cap is None:
            return
        remaining = self._cap_need - (self.time - self._cap_t0)
        if remaining > 0.02:
            self.wait(remaining)

    def _close_sub(self):
        if self._cap_text is not None:
            dur = self.time - self._cap_t0
            if dur > 0:
                self.add_subcaption(self._cap_text, duration=dur, offset=-dur)
            self._cap_text = None

    def say(self, text, *anims, need=None, extra=0.0, run_time=None):
        """Show caption `text` (after the previous one has been readable long
        enough) while playing `anims`."""
        if run_time is not None:
            for a in anims:
                a.run_time = run_time
        self._flush()
        self._close_sub()
        new = self._make_caption(text)
        swap = [FadeIn(new, run_time=0.4)]
        if self._cap is not None:
            swap.append(FadeOut(self._cap, run_time=0.3))
        self._cap_t0 = self.time
        self.play(*swap, *anims)
        self._cap, self._cap_text = new, text
        self._cap_need = (reading_time(text) if need is None else need) + extra

    def hold(self, extra=0.0):
        """Wait until the current caption has been readable, plus `extra`."""
        self._flush()
        if extra > 0:
            self.wait(extra)

    def uncaption(self):
        self._flush()
        self._close_sub()
        if self._cap is not None:
            self.play(FadeOut(self._cap, run_time=0.3))
            self._cap = None

    def clear_stage(self, *keep, run_time=0.8):
        """Fade out everything except the caption and `keep`."""
        keep_ids = {id(m) for k in keep for m in k.get_family()}
        mobs = [m for m in self.mobjects
                if m is not self._cap and id(m) not in keep_ids]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    # -- set pieces
    def heading(self, text, color=YELLOW_D) -> VGroup:
        t = zh(text, 34, color)
        t.to_corner(UL, buff=0.45)
        line = Line(t.get_left(), t.get_right(), stroke_color=color, stroke_width=2)
        line.next_to(t, DOWN, buff=0.1)
        return VGroup(t, line)

    def title_card(self, ep, title, subtitle=None):
        tag = mono("CS61C  ·  RISC-V", 28, GREY_B)
        num = zh(f"第 {ep} 集", 30, YELLOW_D)
        t = Text(title, font=CJK, font_size=60, color=WHITE, weight=BOLD)
        parts = [tag, num, t]
        if subtitle:
            parts.append(zh(subtitle, 30, GREY_A))
        grp = VGroup(*parts).arrange(DOWN, buff=0.4)
        self.play(FadeIn(tag, shift=DOWN * 0.3), FadeIn(num, shift=DOWN * 0.3))
        self.play(Write(t), run_time=1.6)
        if subtitle:
            self.play(FadeIn(parts[-1], shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(grp, shift=UP * 0.3))

    def end_card(self, lines, next_title=None, footer=None):
        self.uncaption()
        self.clear_stage()
        head = zh("小结", 40, YELLOW_D)
        items = VGroup(*[
            VGroup(Dot(color=YELLOW_D, radius=0.06), zh(s, 30)).arrange(RIGHT, buff=0.25)
            for s in lines
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        grp = VGroup(head, items).arrange(DOWN, buff=0.5)
        if grp.height > 6.4:
            grp.scale_to_fit_height(6.4)
        grp.move_to(UP * 0.35)
        self.play(FadeIn(head, shift=DOWN * 0.2))
        for it in items:
            self.play(FadeIn(it, shift=RIGHT * 0.2), run_time=0.6)
            self.wait(reading_time(it[1].text) * 0.8)
        self.wait(1.5)
        if next_title or footer:
            nxt = zh(footer or f"下一集：{next_title}", 30, GREY_A).to_edge(DOWN, buff=0.5)
            self.play(FadeIn(nxt, shift=UP * 0.2))
            self.wait(2.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.5)


# ---------------------------------------------------------------- instruction-format episodes


def bits_to_hex(bits: str) -> str:
    return f"0x{int(bits, 2):08X}"


class FormatScene(NarratedScene):
    """Helpers shared by the two instruction-format episodes."""

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
