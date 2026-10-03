import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---------------------------------------------------------------- the notes' listings, checked


def enc_i(imm, rs1, f3, rd, op):
    return ((imm & 0xFFF) << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op


def enc_s(imm, rs2, rs1, f3, op):
    imm &= 0xFFF
    return ((imm >> 5) << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | ((imm & 0x1F) << 7) | op


def enc_u(imm20, rd, op):
    return ((imm20 & 0xFFFFF) << 12) | (rd << 7) | op


def enc_j(off, rd):
    o = off & 0x1FFFFF
    return ((((o >> 20) & 1) << 31) | (((o >> 1) & 0x3FF) << 21) | (((o >> 11) & 1) << 20)
            | (((o >> 12) & 0xFF) << 12) | (rd << 7) | 0x6F)


def hi20(a):
    return ((a + 0x800) >> 12) & 0xFFFFF


def lo12(a):
    return ((a & 0xFFF) ^ 0x800) - 0x800


RA, SP, A0, A1 = 1, 2, 10, 11
MAIN, PRINTF, STR1 = 0x101B0, 0x10450, 0x20A10
STR1_BYTES = b"Hello, %s!\n\0"
STR2_BYTES = b"world\0"
STR2 = STR1 + len(STR1_BYTES)
CALL_AT = MAIN + 0x18

# hello.o: main's text segment, exactly as listed in the notes (offset, machine code, disassembly)
HELLO_O = [
    (0x00, 0xFFC10113, "addi sp sp -4"),
    (0x04, 0x00112023, "sw   ra 0(sp)"),
    (0x08, 0x00000537, "lui  a0 0x0"),
    (0x0C, 0x00050513, "addi a0 a0 0"),
    (0x10, 0x000005B7, "lui  a1 0x0"),
    (0x14, 0x00058593, "addi a1 a1 0"),
    (0x18, 0x000080E7, "jalr ra 0"),
    (0x1C, 0x00012083, "lw   ra 0(sp)"),
    (0x20, 0x00410113, "addi sp sp 4"),
    (0x24, 0x00000513, "addi a0 zero 0"),
    (0x28, 0x00008067, "jalr ra"),
]
# ... and after linking (a.out), main placed at 0x101B0
A_OUT = [(MAIN + a, w, s) for a, w, s in HELLO_O]
A_OUT[2] = (MAIN + 0x08, 0x00021537, "lui  a0 0x21")
A_OUT[3] = (MAIN + 0x0C, 0xA1050513, "addi a0 a0 -1520 # 20a10 <str1>")
A_OUT[4] = (MAIN + 0x10, 0x000215B7, "lui  a1 0x21")
A_OUT[5] = (MAIN + 0x14, 0xA1C58593, "addi a1 a1 -1508 # 20a1c <str2>")
A_OUT[6] = (MAIN + 0x18, 0x288000EF, "jal  ra 10450    # <printf>")

assert [w for _, w, _ in HELLO_O] == [
    enc_i(-4, SP, 0, SP, 0x13), enc_s(0, RA, SP, 2, 0x23),
    enc_u(0, A0, 0x37), enc_i(0, A0, 0, A0, 0x13),
    enc_u(0, A1, 0x37), enc_i(0, A1, 0, A1, 0x13),
    enc_i(0, RA, 0, RA, 0x67),                       # jalr ra 0(ra): offset still unknown
    enc_i(0, SP, 2, RA, 0x03), enc_i(4, SP, 0, SP, 0x13),
    enc_i(0, 0, 0, A0, 0x13), enc_i(0, RA, 0, 0, 0x67),
]
# str1 at 0x20A10: 0xA10 has bit 11 set, so lui gets 0x21 (not 0x20) and addi gets -1520
assert STR1 == 0x20A10 and hi20(STR1) == 0x21 and lo12(STR1) == -1520 == -0x5F0
assert (hi20(STR1) << 12) + lo12(STR1) == STR1 and lo12(STR1) & 0xFFF == 0xA10
assert len(STR1_BYTES) == 12 and STR2 == 0x20A1C and hi20(STR2) == 0x21 and lo12(STR2) == -1508
assert (0x21 << 12) - 1508 == STR2 and 0x1000 - 0xA1C == 0x5E4 == 1508
assert CALL_AT == 0x101C8 and PRINTF - CALL_AT == 0x288 and CALL_AT + 0x288 == 0x10450
assert A_OUT[2][1] == enc_u(hi20(STR1), A0, 0x37) and A_OUT[3][1] == enc_i(lo12(STR1), A0, 0, A0, 0x13)
assert A_OUT[4][1] == enc_u(hi20(STR2), A1, 0x37) and A_OUT[5][1] == enc_i(lo12(STR2), A1, 0, A1, 0x13)
assert A_OUT[6][1] == enc_j(PRINTF - CALL_AT, RA)
assert [i for i in range(11) if HELLO_O[i][1] != A_OUT[i][1]] == [2, 3, 4, 5, 6]
assert A_OUT[0][0] == 0x101B0 and A_OUT[-1][0] == 0x101D8
# placeholder rows: how many leading hex digits are the (zero) immediate, and the asm token that shows it
HOLES = {2: (5, "0x0"), 3: (3, "0"), 4: (5, "0x0"), 5: (3, "0"), 6: (3, "0")}
for _i, (_n, _) in HOLES.items():
    assert f"{HELLO_O[_i][1]:08x}"[:_n] == "0" * _n
assert format(0x21, "020b") == "00000000000000100001"

C_SRC = [
    "#include <stdio.h>",
    "int main() {",
    '    printf("Hello, %s!\\n", "world");',
    "    return 0;",
    "}",
]
S_TEXT = [".text", "    .align 2", "    .global main", "main:", "    addi sp sp -4", "    sw   ra 0(sp)",
          "    la   a0 str1", "    la   a1 str2", "    call printf", "    lw   ra 0(sp)", "    addi sp sp 4",
          "    li   a0 0", "    ret"]
S_DATA = [".section .rodata", "    .balign 4", "str1:", '    .string "Hello, %s!\\n"', "str2:",
          '    .string "world"']

C_STR = "#E8A87C"
C_HOLE = RED_C
C_DONE = GREEN_B
C_TEXT_SEG = PURPLE_B
C_DATA_SEG = GOLD_C
SZ = 20      # compact listing size (monospace advance ~0.152 per character)
GAP = 0.4


# ---------------------------------------------------------------- helpers


class MarkupListing(CodeListing):
    """A CodeListing built from ready-made markup (one string per line)."""

    def __init__(self, src, markups, font_size=SZ, line_gap=GAP):
        VGroup.__init__(self)
        self.src, self.lang = list(src), "asm"
        self.lines = VGroup()
        for m in markups:
            t = MarkupText("|" + m, font=MONO, font_size=font_size, disable_ligatures=True)
            t[0].set_opacity(0)
            self.lines.add(t)
        for i, t in enumerate(self.lines):
            t.move_to(DOWN * i * line_gap, aligned_edge=LEFT)
        self.add(self.lines)


def plain_listing(lines, color, size=SZ, gap=GAP):
    return MarkupListing(lines, [span(s, color) for s in lines], size, gap)


def hex_line(word, changed=0, size=SZ):
    """One machine word; the first `changed` digits are drawn as newly filled."""
    s = f"{word:08x}"
    m = span(s[:changed], C_DONE) + span(s[changed:], C_TEXT) if changed else span(s, C_TEXT)
    return MarkupListing([s], [m], size)[0]


def color_strings(lst, color=C_STR):
    for i, s in enumerate(lst.src):
        start = 0
        while '"' in s[start:]:
            a = s.index('"', start)
            b = s.index('"', a + 1)
            k = 1 + sum(1 for ch in s[:a] if not ch.isspace())
            n = sum(1 for ch in s[a:b + 1] if not ch.isspace())
            VGroup(*lst.lines[i][k:k + n]).set_color(color)
            start = b + 1


def c_listing(size=26, gap=0.5):
    c = CodeListing(C_SRC, lang="c", font_size=size, line_gap=gap)
    c.glyphs(0, "#include").set_color(C_KEYWORD)
    color_strings(c)
    return c


def addr_s(a):
    return f"{a:>5x}:"


class Disasm(VGroup):
    """objdump-style listing in three columns: address | machine code | instruction."""

    def __init__(self, rows, size=SZ, gap=GAP):
        super().__init__()
        self.size, self.gap = size, gap
        self.addr = plain_listing([addr_s(a) for a, _, _ in rows], GREY_B, size, gap)
        self.hex = plain_listing([f"{w:08x}" for _, w, _ in rows], C_TEXT, size, gap)
        self.asm = CodeListing([s for _, _, s in rows], font_size=size, line_gap=gap)
        self.hex.next_to(self.addr, RIGHT, buff=0.25)
        self.asm.next_to(self.hex, RIGHT, buff=0.35)
        for col in (self.hex, self.asm):
            col.shift(UP * (self.addr[0].get_center()[1] - col[0].get_center()[1]))
        self.add(self.addr, self.hex, self.asm)

    def row_y(self, i):
        return self.addr[i].get_center()[1]

    def digits(self, i, a, b):
        return VGroup(*self.hex[i][1 + a:1 + b])

    def imm(self, i, sub):
        s = self.asm.src[i]
        return self.asm.glyphs(i, sub, s.count(sub) - 1)

    def row(self, i):
        return VGroup(self.addr[i], self.hex[i], self.asm[i])

    def refill(self, i, word, asm, changed):
        """Animations turning row i into `word` / `asm` (first `changed` hex digits highlighted)."""
        new_h = hex_line(word, changed, self.size).move_to(self.hex[i], aligned_edge=LEFT)
        new_a = CodeListing([asm], font_size=self.size)[0].move_to(self.asm[i], aligned_edge=LEFT)
        self.asm.src[i] = asm
        return ReplacementTransform(self.hex[i], new_h), ReplacementTransform(self.asm[i], new_a)


def seg_box(label, color, w, h, size=20, opacity=0.2):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=opacity)
    t = (zh if NEEDS_TR.search(label) else mono)(label, size, WHITE)
    if t.width > w * 0.9:
        t.scale_to_fit_width(w * 0.9)
    return VGroup(r, t.move_to(r))


def grid_table(header, rows, col_x, gap=GAP, hcolor=GREY_B, colors=None):
    """header: zh strings; rows: lists of mono strings; col_x: left x of each column.
    Row k sits at y = -(k + 1) * gap, the header at 0."""
    head = VGroup(*[zh(s, 20, hcolor).move_to([x, 0, 0], aligned_edge=LEFT) for s, x in zip(header, col_x)])
    for h, x0, x1 in zip(head, col_x, col_x[1:]):   # keep a long (English) header out of the next column
        if h.width > x1 - x0 - 0.15:
            h.scale_to_fit_width(x1 - x0 - 0.15, about_edge=LEFT)
    body = VGroup()
    for k, r in enumerate(rows):
        cells = VGroup(*[mono(s, SZ, (colors or [C_TEXT] * len(r))[j]).move_to([x, -(k + 1) * gap, 0],
                                                                             aligned_edge=LEFT)
                         for j, (s, x) in enumerate(zip(r, col_x))])
        body.add(cells)
    width = max(c.get_right()[0] for row in body for c in row) - col_x[0] + 0.2
    rule = Line([col_x[0] - 0.1, -gap / 2, 0], [col_x[0] - 0.1 + width, -gap / 2, 0],
                stroke_color=GREY_D, stroke_width=1.5)
    return VGroup(head, rule, body)


class Ep14HelloWorld(NarratedScene):
    def construct(self):
        self.title_card()
        self.intro()
        colA, s_tab = self.compiler()
        self.assembler(colA, s_tab)
        self.three_kinds()
        self.linker()
        self.quiz_answer()
        self.static_dynamic()
        self.bonus()
        self.finale()
        self.end_card(
            [
                "汇编指示不产生指令，只告诉汇编器如何组织目标文件",
                "hello.o 里未知的地址先填 0，并记进重定位表",
                "文件内的 PC 相对跳转不用重定位，静态数据和外部函数则需要",
                "链接器排好各段、算出符号地址，再逐项补洞",
                "静态链接自给自足；动态链接更省空间、更易升级",
            ],
        )

    # ------------------------------------------------------------------ intro
    def quiz(self):
        title = zh("小测验", 32, YELLOW_D)
        q = zh("哪一步之后，这两条指令的机器码才完全确定？", 26)
        code = CodeListing(["add  x6 x7 x8", "jal  x1 fprintf"], font_size=32, line_gap=0.7)
        opts = VGroup(*[box_label(s, GREY_B, w=2.3, h=0.7, font_size=26) for s in ("编译", "汇编", "链接", "加载")])
        opts.arrange(RIGHT, buff=0.4)
        g = VGroup(title, q, code, opts).arrange(DOWN, buff=0.5).move_to(UP * 0.4)
        g.code, g.opts = code, opts
        return g

    def intro(self):
        code = c_listing().move_to(UP * 0.3)
        tab = mono("hello.c", 28, BLUE_C).next_to(code, UP, buff=0.4).align_to(code, LEFT)
        self.say("上一集讲了 CALL 的四个步骤。这一集，我们跟着一个真实的程序走完全程。",
                 FadeIn(tab, shift=DOWN * 0.2), FadeIn(code, shift=UP * 0.2))
        self.hold()
        self.play(FadeOut(VGroup(tab, code)))
        quiz = self.quiz()
        self.say("先来个小测验：下面两条指令的机器码，要到哪一步之后才完全确定？",
                 LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in quiz], lag_ratio=0.25, run_time=2))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ compiler: hello.c -> hello.s
    def compiler(self):
        c = c_listing().move_to(UP * 0.3)
        c_tab = mono("hello.c", 28, BLUE_C).next_to(c, UP, buff=0.4).align_to(c, LEFT)
        colA = CodeListing(S_TEXT, font_size=SZ, line_gap=0.38)
        colB = CodeListing(S_DATA, font_size=SZ, line_gap=0.38)
        color_strings(colB)
        colA.move_to([-6.45, 2.75, 0], aligned_edge=UL)
        colB.move_to([colA.get_right()[0] + 0.7, 2.75, 0], aligned_edge=UL)
        frame = SurroundingRectangle(VGroup(colA, colB), buff=0.2, corner_radius=0.1,
                                     stroke_color=GREY_D, stroke_width=2)
        s_tab = mono("hello.s", 26, TEAL_C).next_to(frame, UP, buff=0.1).align_to(frame, LEFT).shift(RIGHT * 0.1)
        comp = zh("编译器", 26, BLUE_C)
        self.say("第一步，编译器把 C 代码翻译成汇编，得到 hello.s。", FadeIn(c_tab), FadeIn(c))
        comp.next_to(c, DOWN, buff=0.45)
        self.play(FadeIn(comp, shift=UP * 0.1))
        self.play(FadeOut(VGroup(c_tab, c, comp), shift=LEFT * 0.6),
                  FadeIn(VGroup(s_tab, frame, colA, colB), shift=LEFT * 0.6), run_time=1.2)

        pseudo = VGroup(*[SurroundingRectangle(colA.glyphs(i, m), color=ORANGE, buff=0.05, stroke_width=2.5)
                          for i, m in ((6, "la"), (7, "la"), (8, "call"), (11, "li"), (12, "ret"))])
        self.say("注意 la、call、li、ret 都是伪指令，要留给汇编器展开。",
                 LaggedStart(*[Create(b) for b in pseudo], lag_ratio=0.15))

        spots = [(colA, 0), (colA, 1), (colA, 2), (colB, 0), (colB, 1), (colB, 3), (colB, 5)]
        faint = VGroup(*[lst.line_box(i, color=YELLOW_D, opacity=0.12, pad=0.1) for lst, i in spots])
        self.say("以点开头的是汇编指示（directive）：不产生机器指令，只告诉汇编器怎样组织目标文件。",
                 FadeOut(pseudo), LaggedStart(*[FadeIn(b) for b in faint], lag_ratio=0.1))

        specs = [(".text", "代码段"), (".align 2", "按 2² = 4 字节对齐"), (".global/.globl", "全局符号"),
                 (".section .rodata", "只读数据段"), (".balign 4", "按 4 字节对齐"),
                 (".string", "以 0 结尾的字符串"), (".data", "数据段"), (".word", "32 位的字")]
        tx = frame.get_right()[0] + 0.4
        tbl = VGroup()
        for k, (d, desc) in enumerate(specs):
            row = VGroup(mono(d, SZ, C_MNEM), zh(desc, 20, C_TEXT))
            row[0].move_to([tx, 2.3 - k * 0.5, 0], aligned_edge=LEFT)
            row[1].move_to([tx + 2.65, 2.3 - k * 0.5, 0], aligned_edge=LEFT)
            tbl.add(row)
        for r in tbl[6:]:
            r.shift(DOWN * 0.25)
        tbl_head = zh("汇编指示", 24, YELLOW_D).move_to([tx, 2.85, 0], aligned_edge=LEFT)
        sep = DashedLine([tx, 2.3 - 5.62 * 0.5, 0], [6.8, 2.3 - 5.62 * 0.5, 0], stroke_color=GREY_D,
                         stroke_width=1.5)
        whole = VGroup(tbl_head, tbl, sep)
        if whole.get_right()[0] > 6.8:
            whole.scale((6.8 - tx) / whole.width, about_edge=LEFT)
        self.play(FadeIn(tbl_head))

        cur = [VGroup()]

        def focus(caption, lines, rows, *extra):
            hl = VGroup(*[lst.line_box(i, color=YELLOW_D, opacity=0.34, pad=0.1) for lst, i in lines])
            self.say(caption, FadeOut(cur[0]), FadeIn(hl), *[FadeIn(tbl[r], shift=LEFT * 0.2) for r in rows],
                     *extra)
            cur[0] = hl

        focus(".text 表示接下来是代码段；.align 2 按 2² = 4 字节对齐。", [(colA, 0), (colA, 1)], [0, 1])
        focus(".global（也写作 .globl）把 main 声明为全局符号，别的文件也能引用它。", [(colA, 2)], [2])
        self.play(Circumscribe(colA.glyphs(3, "main"), color=C_LABEL))
        focus("接着切换到只读数据段 .rodata，同样按 4 字节对齐。",
              [(colB, 0), (colB, 1)], [3, 4])
        focus(".string 存入以 0 结尾的字符串，标签 str1、str2 标出它们的起点。",
              [(colB, 3), (colB, 5)], [5])
        self.play(Circumscribe(colB.glyphs(2, "str1"), color=C_LABEL),
                  Circumscribe(colB.glyphs(4, "str2"), color=C_LABEL))
        self.say("另外两个常用指示这里没用到：.data 进入数据段，.word 依次存放 32 位的字。",
                 FadeOut(cur[0]), Create(sep), *[FadeIn(tbl[r], shift=LEFT * 0.2) for r in (6, 7)])
        self.hold()
        self.play(FadeOut(VGroup(colB, frame, faint, whole)))
        return colA, s_tab

    # ------------------------------------------------------------------ assembler: hello.s -> hello.o
    def assembler(self, colA, s_tab):
        words = VGroup(*[mono(f"{w:08x}", 26, C_TEXT) for _, w, _ in HELLO_O])
        words.arrange_in_grid(rows=3, cols=4, buff=(0.45, 0.35), flow_order="rd")
        words.move_to([1.9, 0.9, 0])
        o_tab = mono("hello.o", 26, TEAL_C).next_to(words, UP, buff=0.45).align_to(words, LEFT)
        self.say("第二步，汇编器生成目标文件 hello.o。它是二进制的，直接看只是一串十六进制数。",
                 FadeIn(o_tab), LaggedStart(*[FadeIn(w) for w in words], lag_ratio=0.08, run_time=1.6))
        self.hold()

        D = Disasm(HELLO_O)
        D.shift([-3.1 - D.get_left()[0], 2.45 - D.row_y(0), 0])
        heads = VGroup(*[zh(s, 18, GREY_B).next_to(col, UP, buff=0.22).align_to(col, LEFT).shift(RIGHT * 0.12)
                         for s, col in (("地址", D.addr), ("机器码", D.hex), ("指令", D.asm))])
        for h, col in zip(heads, (D.addr, D.hex, D.asm)):
            h.set_y(2.85)
            if h.width > col.width:   # English "Machine code" is wider than the hex column
                h.scale_to_fit_width(col.width, about_edge=LEFT)
        self.say("把 main 反汇编出来：左列是模块内的地址，中间是机器码，右列是指令。",
                 o_tab.animate.move_to([D.get_left()[0] + o_tab.width / 2 + 0.1, s_tab.get_y(), 0]),
                 *[ReplacementTransform(w, D.hex[i]) for i, w in enumerate(words)], run_time=1.4)
        self.add(D)
        self.play(FadeIn(D.addr), FadeIn(D.asm), FadeIn(heads))

        pairs = [(6, [2, 3]), (7, [4, 5]), (8, [6]), (11, [9]), (12, [10])]
        marks = VGroup()
        for src, dst in pairs:
            a = SurroundingRectangle(colA[src][1:], color=ORANGE, buff=0.05, stroke_width=2)
            b = SurroundingRectangle(VGroup(*[D.row(i) for i in dst]), color=ORANGE, buff=0.04, stroke_width=2)
            ln = Line(a.get_right(), b.get_left(), stroke_color=ORANGE, stroke_width=2)
            marks.add(VGroup(a, ln, b))
        foot = zh("注：la 也可能展开成 auipc + addi；call 通常是 auipc + jalr（第 12 集）", 18, GREY_B)
        foot.next_to(D, DOWN, buff=0.3).align_to(D, LEFT)
        self.say("伪指令都展开了。注意这份清单做了简化：call 只变成了一条 jalr。",
                 LaggedStart(*[Create(m) for m in marks], lag_ratio=0.25, run_time=2.2), FadeIn(foot))
        self.hold()
        dx = -6.55 - D.get_left()[0]
        self.play(FadeOut(VGroup(colA, s_tab, marks, foot)), VGroup(D, heads, o_tab).animate.shift(RIGHT * dx))

        holes = VGroup()
        boxes = VGroup()
        for i, (n, sub) in HOLES.items():
            holes.add(D.digits(i, 0, n), D.imm(i, sub))
            boxes.add(SurroundingRectangle(D.digits(i, 0, n), color=C_HOLE, buff=0.04, stroke_width=2))
        self.say("但这五条的立即数都是 0，只是占位符：数据和 printf 在哪，汇编器还不知道。",
                 holes.animate.set_color(C_HOLE), LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.15))
        fixed = [0, 1, 7, 8, 9, 10]
        self.say("其余指令不涉及地址，汇编完，机器码就定了。",
                 VGroup(*[D.hex[i][1:] for i in fixed]).animate.set_color(C_DONE),
                 Circumscribe(D.row(1), color=C_DONE))

        # symbol table, rows lined up with the listing
        X0 = -0.3
        sym_t = zh("符号表", 26, YELLOW_D).move_to([X0, D.row_y(0), 0], aligned_edge=LEFT)
        sym = grid_table(["标签", "段内地址", "类型"],
                         [["main", "0x00000000", "global text"], ["str1", "0x00000000", "local data"],
                          ["str2", "0x0000000c", "local data"]],
                         [X0, X0 + 1.2, X0 + 3.2], colors=[C_LABEL, C_NUM, C_TEXT])
        sym.shift(UP * D.row_y(1))
        self.say("符号表记下本文件的标签，以及它们在各自段内的地址；调试器 gdb 也要用它。",
                 FadeIn(sym_t), FadeIn(sym[0]), Create(sym[1]),
                 LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in sym[2]], lag_ratio=0.2))
        self.say("main 在代码段偏移 0 处，类型是 global，这正是 .global 的作用。",
                 Indicate(sym[2][0], color=YELLOW_D, scale_factor=1.1))
        self.hold()

        cells = VGroup()
        labels = [chr(b) if 32 < b < 127 else {32: "␣", 10: "\\n", 0: "\\0"}[b]
                  for b in STR1_BYTES + STR2_BYTES]
        for k, s in enumerate(labels):
            sq = Square(0.34, stroke_color=C_DATA_SEG, stroke_width=1.5, fill_color=C_DATA_SEG,
                        fill_opacity=0.12 if k < 12 else 0.28)
            sq.move_to([X0 + 0.17 + k * 0.34, -0.75, 0])
            t = mono(s, 18 if len(s) == 1 else 14, WHITE).move_to(sq)
            cells.add(VGroup(sq, t))
        br1 = Brace(cells[:12], UP, buff=0.06, color=GREY_B)
        br2 = Brace(cells[12:], UP, buff=0.06, color=GREY_B)
        l1 = mono("str1", 20, C_LABEL).next_to(br1, UP, buff=0.06)
        l2 = mono("str2", 20, C_LABEL).next_to(br2, UP, buff=0.06)
        o1 = mono("0x0", 18, GREY_B).next_to(cells[0], DOWN, buff=0.1)
        o2 = mono("0xc", 18, GREY_B).next_to(cells[12], DOWN, buff=0.1)
        strip_t = zh("数据段（.rodata）", 20, GREY_A).next_to(cells, DOWN, buff=0.5).align_to(cells, RIGHT)
        self.say("两个字符串是局部数据。第一个连同结尾的 0 共 12 字节，所以第二个从 0xc 开始。",
                 Indicate(VGroup(sym[2][1], sym[2][2]), color=YELLOW_D, scale_factor=1.05),
                 LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.04, run_time=1.4),
                 FadeIn(strip_t))
        self.play(GrowFromCenter(br1), FadeIn(l1), FadeIn(o1), GrowFromCenter(br2), FadeIn(l2), FadeIn(o2))
        self.play(Indicate(o2, color=YELLOW_D), Indicate(sym[2][2][1], color=YELLOW_D))
        self.hold()

        self.play(FadeOut(VGroup(sym_t, sym, cells, br1, br2, l1, l2, o1, o2, strip_t)))
        rel_t = zh("重定位表", 26, RED_B).move_to([X0, D.row_y(0), 0], aligned_edge=LEFT)
        rel = grid_table(["地址", "类型", "依赖"],
                         [["0x00000008", "lui", "%hi(str1)"], ["0x0000000c", "addi", "%lo(str1)"],
                          ["0x00000010", "lui", "%hi(str2)"], ["0x00000014", "addi", "%lo(str2)"],
                          ["0x00000018", "jalr", "printf"]],
                         [X0, X0 + 2.0, X0 + 3.1], colors=[C_NUM, C_MNEM, C_LABEL])
        rel.shift(UP * D.row_y(1))
        links = VGroup(*[DashedLine([D.get_right()[0] + 0.12, D.row_y(i), 0], [X0 - 0.15, D.row_y(i), 0],
                                    stroke_color=C_HOLE, stroke_width=2, dash_length=0.08)
                         for i in range(2, 7)])
        self.say("重定位表是留给链接器的“待办清单”，每一项对应一个占位符。",
                 FadeIn(rel_t), FadeIn(rel[0]), Create(rel[1]),
                 LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in rel[2]], lag_ratio=0.15))
        self.say("前两项：0x8 处的 lui 等着 str1 地址的高 20 位，0xc 处的 addi 等着低 12 位。",
                 Create(links[0]), Create(links[1]),
                 Indicate(rel[2][0], color=RED_B, scale_factor=1.05),
                 Indicate(rel[2][1], color=RED_B, scale_factor=1.05))
        self.say("str2 的两项同理；最后一项在 0x18，jalr 等着 printf 的地址。",
                 *[Create(links[k]) for k in (2, 3, 4)],
                 Indicate(rel[2][4], color=RED_B, scale_factor=1.05))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ three kinds of addresses
    def three_kinds(self):
        head = self.heading("哪些地址需要重定位？")

        def card(x, title, color, lines):
            box = RoundedRectangle(corner_radius=0.15, width=4.15, height=3.8, stroke_color=color,
                                   stroke_width=2.5, fill_color=color, fill_opacity=0.06).move_to([x, 0.1, 0])
            t = zh(title, 22, color).next_to(box.get_top(), DOWN, buff=0.28)
            if t.width > 3.9:
                t.scale_to_fit_width(3.9)
            code = CodeListing(lines, font_size=SZ, line_gap=GAP).next_to(t, DOWN, buff=0.4)
            return VGroup(box, t, code)

        c1 = card(-4.5, "① 文件内的 PC 相对跳转", BLUE_C,
                  ["    beq  t0 t1 L1", "    addi t0 t0 1", "L1: add  t2 t0 t1"])
        c2 = card(0, "② 静态数据的绝对地址", C_DATA_SEG,
                  ["la   a0 str1", "→ lui  a0 %hi(str1)", "  addi a0 a0 %lo(str1)"])
        c3 = card(4.5, "③ 外部函数", RED_C, ["call printf", "→ jal  ra printf"])
        code1 = c1[2]
        code1.shift(LEFT * 0.25)
        arc = CurvedArrow(code1.right_of(0, 0.15), code1.right_of(2, 0.15), angle=-TAU / 4, color=YELLOW_D)
        off = mono("+8", 22, YELLOW_D).next_to(arc, RIGHT, buff=0.08)
        v1 = zh("汇编器直接算好", 24, C_DONE).next_to(c1[0].get_bottom(), UP, buff=0.55)
        v1b = zh("B 型分支从不用改", 18, GREY_A).next_to(v1, DOWN, buff=0.15)
        v2 = zh("进重定位表", 24, C_HOLE).next_to(c2[0].get_bottom(), UP, buff=0.55)
        v3 = zh("进重定位表", 24, C_HOLE).next_to(c3[0].get_bottom(), UP, buff=0.55)
        self.say("为什么有的地址汇编器就能定，有的却要等链接器？因为地址分三种。", Write(head))
        self.say("一、文件内的 PC 相对跳转，比如 beq，或 jal 到本文件的标签：代码整体挪到哪儿，距离都不变。",
                 FadeIn(c1), Create(arc), FadeIn(off))
        self.play(VGroup(code1, arc, off).animate(rate_func=there_and_back, run_time=1.6).shift(DOWN * 0.45))
        self.play(FadeIn(v1, shift=UP * 0.1))
        self.say("二、静态数据的地址，比如 la 要装入的 str1、lw 要读的全局变量：要等所有文件拼好才知道。",
                 FadeIn(c2))
        self.say("三、外部函数，比如 printf：它在别的文件里，汇编器连它有多远都不知道。", FadeIn(c3))
        self.say("后两种要记进重定位表。所以 jal 有时要改，而 B 型分支只在模块内跳，从来不用改。",
                 FadeIn(v2, shift=UP * 0.1), FadeIn(v3, shift=UP * 0.1), FadeIn(v1b))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ linker: hello.o -> a.out
    def linker(self):
        head = self.heading("链接：hello.o → a.out")
        W = 2.4
        spec_data = [("…", 0.4), ("str2", 0.5), ("str1", 0.5)]
        spec_text = [("…", 0.4), ("printf", 0.55), ("…", 0.4), ("main", 0.55), ("启动例程", 0.55)]

        def column(spec, color):
            frames = VGroup(*[Rectangle(width=W, height=h, stroke_color=color, stroke_width=2) for _, h in spec])
            frames.arrange(DOWN, buff=0)
            return frames

        dframes, tframes = column(spec_data, C_DATA_SEG), column(spec_text, C_TEXT_SEG)
        dots = VGroup(*[Dot(radius=0.035, color=GREY_B) for _ in range(3)]).arrange(DOWN, buff=0.1)
        mem = VGroup(dframes, dots, tframes).arrange(DOWN, buff=0.14).move_to([-4.0, 0.1, 0])
        aout_t = mono("a.out", 24, GREEN_C).next_to(mem, UP, buff=0.12)
        fill_d = VGroup(*[seg_box(s, C_DATA_SEG, W, f.height) for (s, _), f in zip(spec_data, dframes)])
        fill_t = VGroup(*[seg_box(s, C_TEXT_SEG, W, f.height) for (s, _), f in zip(spec_text, tframes)])
        for g, fr in ((fill_d, dframes), (fill_t, tframes)):
            for s, f in zip(g, fr):
                s.move_to(f)
        br_t = Brace(tframes, RIGHT, buff=0.08, color=C_TEXT_SEG)
        br_d = Brace(dframes, RIGHT, buff=0.08, color=C_DATA_SEG)
        br_tl = zh("代码段", 20, C_TEXT_SEG).next_to(br_t, RIGHT, buff=0.08)
        br_dl = zh("数据段", 20, C_DATA_SEG).next_to(br_d, RIGHT, buff=0.08)

        def addr_label(i_frame, frames, a):
            return mono(f"0x{a:X}", 20, GREY_B).next_to(frames[i_frame], LEFT, buff=0.15)

        a_crt, a_main, a_pf = (addr_label(4, tframes, 0x10000), addr_label(3, tframes, MAIN),
                               addr_label(1, tframes, PRINTF))
        a_s1, a_s2 = addr_label(2, dframes, STR1), addr_label(1, dframes, STR2)

        def objfile(title, segs, x, y):
            boxes = VGroup(*[seg_box(s, c, 1.9, 0.5) for s, c in segs]).arrange(DOWN, buff=0)
            t = mono(title, 22, TEAL_C).next_to(boxes, UP, buff=0.1)
            return VGroup(boxes, t).move_to([x, y, 0])

        crt = objfile("crt0.o", [("启动例程", C_TEXT_SEG)], 0.6, 1.55)
        hello = objfile("hello.o", [("main", C_TEXT_SEG), ("str1 str2", C_DATA_SEG)], 3.3, 1.3)
        pf = objfile("printf.o", [("printf", C_TEXT_SEG)], 1.4, -1.0)
        others = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.08, width=1.5, height=0.8, stroke_color=GREY_B,
                                                  stroke_width=1.5), mono(s, 18, GREY_B))
                          for s in ("strlen.o", "…")])
        for o in others:
            o[1].move_to(o[0])
        others.arrange(RIGHT, buff=0.3).next_to(pf, RIGHT, buff=0.35).align_to(pf, DOWN)
        libc_in = VGroup(pf, others)
        libc_box = SurroundingRectangle(libc_in, buff=0.25, corner_radius=0.12, stroke_color=TEAL_C,
                                        stroke_width=2)
        libc_t = mono("libc.a", 22, TEAL_C).next_to(libc_box, UP, buff=0.1).align_to(libc_box, LEFT)
        libc = VGroup(libc_box, libc_t, libc_in)
        inputs = VGroup(crt, hello, libc)

        self.say("第三步，链接器把 hello.o、启动例程和库里的 printf 拼成可执行文件 a.out。",
                 Write(head), FadeIn(inputs, lag_ratio=0.1), Create(mem), FadeIn(aout_t))
        self.hold()
        q = Arrow(hello[0].get_bottom(), libc_box.get_top() + RIGHT * 0.3, buff=0.1, color=YELLOW_D,
                  stroke_width=3)
        q_l = mono("printf?", 20, YELLOW_D).next_to(q, RIGHT, buff=0.1)
        bundle = zh("一包 .o 文件", 20, GREY_A).next_to(libc_t, RIGHT, buff=0.3)
        self.say("printf 在哪？链接器先查用户的 .o 文件，找不到再查库。库文件 .a 其实就是一包 .o 文件。",
                 Circumscribe(crt, color=GREY_B), Circumscribe(hello, color=GREY_B))
        self.play(GrowArrow(q), FadeIn(q_l), FadeIn(bundle))
        self.play(Circumscribe(pf, color=YELLOW_D))
        re_c = zh("重新编译", 20, BLUE_B).next_to(hello, UP, buff=0.12)
        no_c = zh("不用重新编译", 20, GREY_A).next_to(libc_box, DOWN, buff=0.12).align_to(libc_box, RIGHT)
        self.say("链接也让分开编译成为可能：改了 hello.c 只需重新编译它自己，庞大的 C 库不用跟着重编。",
                 FadeIn(re_c, shift=DOWN * 0.1), Indicate(hello[0], color=BLUE_B), FadeIn(no_c))
        self.hold()

        self.say("先把各代码段从 0x10000 起首尾相接：启动例程在最前，接着是 main，再往后是 printf。",
                 FadeOut(VGroup(q, q_l, re_c, no_c)), GrowFromCenter(br_t), FadeIn(br_tl))
        self.play(TransformFromCopy(crt[0][0], fill_t[4]), FadeIn(a_crt), run_time=1.0)
        self.play(TransformFromCopy(hello[0][0], fill_t[3]), FadeIn(a_main), FadeIn(fill_t[2]), run_time=1.0)
        self.play(TransformFromCopy(pf[0][0], fill_t[1]), FadeIn(a_pf), FadeIn(fill_t[0]), run_time=1.0)
        self.say("数据段接在代码之后：str1 在 0x20A10，str2 比它晚 12 字节。",
                 GrowFromCenter(br_d), FadeIn(br_dl))
        self.play(TransformFromCopy(hello[0][1], VGroup(fill_d[1], fill_d[2])), FadeIn(a_s1), FadeIn(a_s2),
                  FadeIn(fill_d[0]), run_time=1.2)

        SX = 1.9
        st_t = zh("符号表（链接后）", 24, YELLOW_D).move_to([SX, 2.55, 0], aligned_edge=LEFT)
        st = grid_table(["符号", "地址"],
                        [["main", "0x000101b0"], ["printf", "0x00010450"], ["str1", "0x00020a10"],
                         ["str2", "0x00020a1c"]],
                        [SX, SX + 1.5], colors=[C_LABEL, C_NUM])
        st.shift(UP * 2.15)
        self.say("所有符号的最终地址都定了，链接器据此更新符号表。",
                 FadeOut(VGroup(inputs, bundle)), FadeIn(st_t), FadeIn(st[0]), Create(st[1]))
        self.play(*[TransformFromCopy(a, st[2][k][1]) for k, a in enumerate((a_main, a_pf, a_s1, a_s2))],
                  *[FadeIn(st[2][k][0]) for k in range(4)], run_time=1.2)
        self.hold()

        # --- fill the holes
        D = Disasm(HELLO_O)
        D.shift([-6.55 - D.get_left()[0], 2.45 - D.row_y(0), 0])
        for i in (0, 1, 7, 8, 9, 10):
            D.hex[i][1:].set_color(C_DONE)
        boxes = {}
        for i, (n, sub) in HOLES.items():
            D.digits(i, 0, n).set_color(C_HOLE)
            D.imm(i, sub).set_color(C_HOLE)
            boxes[i] = SurroundingRectangle(D.digits(i, 0, n), color=C_HOLE, buff=0.04, stroke_width=2)
        new_addr = plain_listing([addr_s(a) for a, _, _ in A_OUT], GREY_B)
        new_addr.shift(D.addr[0].get_left() - new_addr[0].get_left())
        self.say("然后按重定位表逐项补洞。先换上每条指令的最终地址。",
                 FadeOut(VGroup(mem, aout_t, fill_d, fill_t, br_t, br_d, br_tl, br_dl,
                                a_crt, a_main, a_pf, a_s1, a_s2)),
                 FadeIn(D), FadeIn(VGroup(*boxes.values())))
        self.play(ReplacementTransform(D.addr, new_addr), run_time=1.2)
        D.addr = new_addr

        CX = 1.9
        calc = VGroup(mono("str1 = 0x20A10", SZ, C_TEXT), mono("0xA10 → -0x5F0 = -1520", SZ, C_TEXT),
                      mono("0x21000 - 1520 = 0x20A10", SZ, C_TEXT))
        for k, m in enumerate(calc):
            m.move_to([CX, -0.05 - k * 0.4, 0], aligned_edge=LEFT)
        calc[2][:7].set_color(C_DONE)
        self.say("从 str1 = 0x20A10 开始：低 12 位 0xA10 的最高位是 1，addi 会把它当成负数 −1520。",
                 Indicate(st[2][2], color=YELLOW_D, scale_factor=1.05), FadeIn(calc[0]),
                 Circumscribe(D.row(2), color=C_HOLE), Circumscribe(D.row(3), color=C_HOLE))
        self.play(FadeIn(calc[1], shift=DOWN * 0.1))
        self.say("所以高 20 位要多加 1，写成 0x21。这正是第 12 集里 li 的拆法。",
                 FadeIn(calc[2], shift=DOWN * 0.1))
        self.hold()

        bf = BitField([("imm[31:12]", 20, YELLOW_D), ("rd", 5, FIELD_COLORS["rd"]),
                       ("opcode", 7, FIELD_COLORS["opcode"])],
                      box_w=0.15, box_h=0.34, font_size=14, label_size=16, show_ranges=False)
        bf.set_bits_now(format(HELLO_O[2][1], "032b"))
        bf.field_digits[0].set_color(C_HOLE)
        bf.move_to([6.6 - bf.width / 2, -1.9, 0])
        bf_t = mono("lui  a0 0x21", 18, GREY_A).next_to(bf.labels[0], UP, buff=0.08).align_to(bf, LEFT)
        self.say("把 0x21 填进 lui 的立即数字段：占位的 0 变成了真正的地址位。",
                 FadeIn(bf), FadeIn(bf_t))
        self.play(LaggedStart(*[Transform(d, mono(ch, bf.font_size, C_DONE).move_to(d))
                                for d, ch in zip(bf.field_digits[0], format(0x21, "020b"))],
                              lag_ratio=0.04, run_time=1.2))
        self.play(*D.refill(2, A_OUT[2][1], A_OUT[2][2], 5), FadeOut(boxes[2]), run_time=1.2)
        self.say("addi 填入 −1520，这两条指令就补全了。",
                 *D.refill(3, A_OUT[3][1], A_OUT[3][2], 3), FadeOut(boxes[3]), run_time=1.2)
        self.hold()

        calc2 = VGroup(mono("str2 = 0x20A1C", SZ, C_TEXT), mono("0xA1C → -0x5E4 = -1508", SZ, C_TEXT),
                       mono("0x21000 - 1508 = 0x20A1C", SZ, C_TEXT))
        for a, b in zip(calc2, calc):
            a.move_to(b, aligned_edge=LEFT)
        calc2[2][:7].set_color(C_DONE)
        self.say("str2 同理：lui 也填 0x21，addi 填 −1508。",
                 FadeOut(VGroup(bf, bf_t)), Transform(calc, calc2), Indicate(st[2][3], color=YELLOW_D,
                                                                            scale_factor=1.05))
        self.play(*D.refill(4, A_OUT[4][1], A_OUT[4][2], 5), *D.refill(5, A_OUT[5][1], A_OUT[5][2], 3),
                  FadeOut(boxes[4]), FadeOut(boxes[5]), run_time=1.4)

        calc3 = VGroup(mono("printf = 0x10450", SZ, C_TEXT), mono("PC     = 0x101C8", SZ, C_TEXT),
                       mono("0x10450 - 0x101C8 = 0x288", SZ, C_TEXT))
        for a, b in zip(calc3, calc):
            a.move_to(b, aligned_edge=LEFT)
        calc3[2][-5:].set_color(C_DONE)
        self.say("最后是 printf：它在 0x10450，离这条调用 0x288 字节。",
                 Transform(calc, calc3), Indicate(st[2][1], color=YELLOW_D, scale_factor=1.05),
                 Circumscribe(D.row(6), color=C_HOLE))
        editor = zh("链接器旧称“链接编辑器”，\n因为它改写的正是这些“链接”", 20, GREY_B)
        editor.move_to([CX, -1.6, 0], aligned_edge=LEFT)
        self.say("jal 能跳 ±1 MiB，足够了：链接器把这里直接改写成一条 jal。",
                 *D.refill(6, A_OUT[6][1], A_OUT[6][2], 8), FadeOut(boxes[6]), run_time=1.4)
        self.play(FadeIn(editor))
        self.hold()

        parts = VGroup(*[seg_box(s, c, 3.4, 0.5, size=20) for s, c in
                         (("文件头", GREY_B), ("代码段", C_TEXT_SEG), ("数据段", C_DATA_SEG), ("调试信息", GREY))])
        parts.arrange(DOWN, buff=0).move_to([CX + 1.9, -0.2, 0])
        parts_t = mono("a.out", 24, GREEN_C).next_to(parts, UP, buff=0.15)
        self.say("其余指令一位没动。再加上文件头和调试信息，a.out 就完成了：每一位都已确定。",
                 FadeOut(VGroup(calc, st_t, st, editor)), FadeIn(parts_t), LaggedStart(*[FadeIn(p) for p in parts],
                                                                                lag_ratio=0.15),
                 Indicate(D.hex, color=C_DONE, scale_factor=1.03))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ the quick check, answered
    def quiz_answer(self):
        quiz = self.quiz()
        self.say("回到小测验：add 不涉及任何地址，汇编之后就确定了。", FadeIn(quiz))
        a1 = VGroup(Arrow(LEFT * 0.4, RIGHT * 0.4, buff=0, color=C_DONE), zh("汇编之后", 26, C_DONE))
        a1[1].next_to(a1[0], RIGHT, buff=0.15)
        a1.next_to(quiz.code, RIGHT, buff=0.5).set_y(quiz.code[0].get_y())
        self.play(FadeIn(a1, shift=RIGHT * 0.2), quiz.opts[1][0].animate.set_stroke(C_DONE).set_fill(C_DONE, 0.3))
        a2 = VGroup(Arrow(LEFT * 0.4, RIGHT * 0.4, buff=0, color=C_DONE), zh("链接之后", 26, C_DONE))
        a2[1].next_to(a2[0], RIGHT, buff=0.15)
        a2.next_to(quiz.code, RIGHT, buff=0.5).set_y(quiz.code[1].get_y())
        self.say("而 jal 跳向 stdio 库里的外部函数 fprintf，要到链接之后才确定。",
                 FadeIn(a2, shift=RIGHT * 0.2), quiz.opts[2][0].animate.set_stroke(C_DONE).set_fill(C_DONE, 0.3))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ static vs dynamic linking
    def static_dynamic(self):
        div = DashedLine(UP * 2.9, DOWN * 2.3, stroke_color=GREY_D)
        st_t = zh("静态链接", 30, BLUE_C).move_to([-3.4, 2.7, 0])
        dy_t = zh("动态链接", 30, GREEN_C).move_to([3.4, 2.7, 0])

        def prog(name, x, lib):
            t = zh(name, 22, GREY_A)
            code = seg_box("代码", C_TEXT_SEG, 2.2, 0.6)
            parts = [code]
            if lib:
                parts.append(seg_box("libc 副本", TEAL_C, 2.2, 1.4))
            body = VGroup(*parts).arrange(DOWN, buff=0)
            frame = SurroundingRectangle(body, buff=0.08, stroke_color=GREY_B, stroke_width=1.5)
            t.next_to(frame, UP, buff=0.12)
            return VGroup(frame, body, t).move_to([x, 0.75 if lib else 1.4, 0])

        sa, sb = prog("程序 A", -5.0, True), prog("程序 B", -1.8, True)
        big = zh("每个程序都很大", 22, GREY_A).move_to([-3.4, -1.25, 0])
        self.say("刚才这种叫静态链接：库代码直接拷进 a.out，程序自给自足，但文件很大。",
                 Create(div), FadeIn(st_t), FadeIn(sa), FadeIn(sb))
        self.play(FadeIn(big))
        bugs = VGroup(*[zh("漏洞", 20, RED_B).move_to(p[1][1]).shift(DOWN * 0.35) for p in (sa, sb)])
        self.say("库一旦修了 bug 或安全漏洞，每个程序都得重新链接、重新发布。",
                 FadeIn(bugs), *[p[1][1][0].animate.set_fill(RED_C, 0.35) for p in (sa, sb)])
        relink = zh("逐个重新链接、重新发布", 22, RED_B).move_to(big)
        self.play(FadeOut(big), FadeIn(relink),
                  *[Indicate(p, color=RED_B, scale_factor=1.04) for p in (sa, sb)])
        self.hold()

        da, db = prog("程序 A", 1.9, False), prog("程序 B", 5.0, False)
        so = seg_box("libc.so", TEAL_C, 2.4, 0.8, size=24).move_to([3.45, -0.5, 0])
        arrows = VGroup(*[Arrow(p[0].get_bottom(), so.get_top() + RIGHT * dx, buff=0.1, color=GREY_B,
                                stroke_width=3) for p, dx in ((da, -0.5), (db, 0.5))])
        at_load = zh("加载时链接", 20, GREY_A).next_to(arrows, UP, buff=0.05).shift(DOWN * 0.35)
        self.say("动态链接则把库单独存成文件，比如 libc.so，等程序加载时才链接进来。",
                 FadeIn(dy_t), FadeIn(da), FadeIn(db), FadeIn(so))
        self.play(*[GrowArrow(a) for a in arrows], FadeIn(at_load))
        new_so = seg_box("libc.so（新）", C_DONE, 2.4, 0.8, size=24).move_to(so)
        share = zh("一份库，大家共享", 22, GREY_A).next_to(so, DOWN, buff=0.3)
        self.say("程序文件更小，多个程序还能共享内存里的同一份库；换掉 libc.so，大家一起升级。",
                 FadeIn(share))
        self.play(Transform(so, new_so), *[Indicate(p, color=C_DONE, scale_factor=1.04) for p in (da, db)])
        cons = VGroup(zh("运行时有链接开销", 22, RED_B), zh("光有 a.out 不够，还要库文件", 22, RED_B))
        cons.arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(share, DOWN, buff=0.3)
        self.say("代价是运行时的链接开销，而且光有 a.out 已经跑不起来。总体上仍是利大于弊。",
                 FadeIn(cons, shift=UP * 0.1))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ bonus: interpret vs translate
    def bonus(self):
        head = self.heading("番外：解释与翻译")
        tag = zh("（不考）", 24, GREY_B).next_to(head[0], RIGHT, buff=0.2)
        line = DoubleArrow(LEFT * 6.2, RIGHT * 6.2, buff=0, color=GREY_B, stroke_width=3,
                           max_tip_length_to_length_ratio=0.02).shift(UP * 0.8)
        xs = [-4.6, -1.55, 1.55, 4.6]
        names = ["Python", "Java", "C", "机器码"]
        descs = ["解释器逐句执行", "字节码 + 解释执行", "编译成机器码", "硬件直接执行"]
        stops = VGroup()
        for x, n, d in zip(xs, names, descs):
            dot = Dot([x, 0.8, 0], radius=0.09, color=YELLOW_D)
            nt = (zh if NEEDS_TR.search(n) else mono)(n, 28, WHITE).next_to(dot, UP, buff=0.25)
            dt = zh(d, 20, GREY_A).next_to(dot, DOWN, buff=0.25)
            stops.add(VGroup(dot, nt, dt))
        easy = zh("← 更好写", 22, BLUE_B).move_to([-5.0, -0.45, 0])
        fast = zh("更快 →", 22, GOLD_C).move_to([5.2, -0.45, 0])
        self.say("番外（不考）：程序也可以不翻译，而是交给解释器（另一个程序）直接执行。",
                 Write(head), FadeIn(tag), GrowFromCenter(line))
        self.say("Python 全靠解释，最好写也最慢；Java 先编译成字节码再解释，所以到处都能跑。",
                 FadeIn(stops[0], shift=UP * 0.1), FadeIn(stops[1], shift=UP * 0.1), FadeIn(easy))
        self.say("C 编译成机器码，快得多。机器码最难手写，却最好“解释”：硬件直接就能执行。",
                 FadeIn(stops[2], shift=UP * 0.1), FadeIn(stops[3], shift=UP * 0.1), FadeIn(fast))
        badges = VGroup(box_label("Venus：用软件逐条执行 RISC-V", TEAL_C, h=0.7, font_size=22),
                        box_label("Rosetta：让 Intel 程序跑在 Apple 芯片上", GREY_B, h=0.7, font_size=22))
        badges.arrange(RIGHT, buff=0.4).move_to(DOWN * 1.6)
        if badges.width > 13.2:
            badges.scale_to_fit_width(13.2)
        hist = mono("680x0 → PowerPC → x86 → ARM", 18, GREY_B).next_to(badges[1], DOWN, buff=0.15)
        self.say("机器码也能用软件来解释：Venus 逐条模拟 RISC-V，方便单步调试。",
                 FadeIn(badges[0], shift=UP * 0.1))
        self.say("Apple 几次更换 ISA，都靠软件来运行旧 ISA 的程序，最近的一次就是 Rosetta。",
                 FadeIn(badges[1], shift=UP * 0.1), FadeIn(hist))
        self.hold()

        def col(title, color, items, x):
            t = zh(title, 28, color)
            rows = VGroup(*[zh(s, 24, C_TEXT) for s in items]).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
            g = VGroup(t, rows).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            return g.move_to([x, 0.3, 0], aligned_edge=UP).shift(UP * 1.6)

        left = col("解释的长处", BLUE_B, ["更容易实现", "报错、调试更友好", "代码更小，不依赖具体 ISA"], -3.3)
        right = col("翻译的长处", GOLD_C, ["通常快 10 倍以上", "不必公开源代码"], 3.3)
        note = zh("程序自己分不清跑在解释器上还是硬件上", 22, GREY_B).move_to(DOWN * 1.35)
        self.say("解释器好写、好调试、可移植；翻译后的程序通常快 10 倍以上，还不必公开源代码。",
                 FadeOut(VGroup(line, stops, easy, fast, badges, hist)), FadeIn(left, shift=UP * 0.1),
                 FadeIn(right, shift=UP * 0.1), FadeIn(note))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ finale
    def finale(self):
        icons = [file_icon("hello.c", BLUE_C, w=1.1, h=1.35, font_size=20),
                 file_icon("hello.s", BLUE_C, w=1.1, h=1.35, font_size=20),
                 file_icon("hello.o", TEAL_C, w=1.1, h=1.35, font_size=20),
                 file_icon("a.out", GREEN_C, w=1.1, h=1.35, font_size=20)]
        term = VGroup(RoundedRectangle(corner_radius=0.1, width=2.5, height=1.35, stroke_color=GREY_B,
                                       stroke_width=2, fill_color=BLACK, fill_opacity=0.6))
        prompt = mono("$ ./a.out", 18, GREY_B)
        out = mono("Hello, world!", 18, C_DONE)
        VGroup(prompt, out).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(term[0])
        chain = VGroup(*icons, term).arrange(RIGHT, buff=1.4).move_to(UP * 1.9)
        VGroup(prompt, out).move_to(term[0])
        arrows = VGroup(*[Arrow(chain[k].get_right(), chain[k + 1].get_left(), buff=0.1, color=GREY_B,
                                stroke_width=3) for k in range(4)])
        steps = VGroup(*[zh(s, 20, YELLOW_D).next_to(a, UP, buff=0.08)
                         for s, a in zip(("编译", "汇编", "链接", "加载"), arrows)])
        for s, a in zip(steps, arrows):   # English labels are wider than the gap
            if s.width > a.width:
                s.scale_to_fit_width(a.width)
        self.say("串起来看：编译成汇编，汇编成带占位符的机器码，链接时补上地址，最后加载运行。",
                 LaggedStart(*[AnimationGroup(FadeIn(chain[k], shift=RIGHT * 0.15),
                                              *([GrowArrow(arrows[k - 1]), FadeIn(steps[k - 1])] if k else []))
                               for k in range(5)], lag_ratio=0.45, run_time=4))
        self.say("加载器把 a.out 读进内存，经启动例程调用 main，屏幕上就出现了 Hello, world!",
                 FadeIn(prompt), Indicate(chain[3], color=GREEN_C, scale_factor=1.08))
        self.play(AddTextLetterByLetter(out, run_time=1.0))

        entries = VGroup()
        for n, ep in enumerate(EPISODES, 1):
            e = VGroup(mono(f"{n:02d}", 20, GREY_B), zh(ep["title"][LANG], 20, GREY_A))
            e.arrange(RIGHT, buff=0.2)
            entries.add(e)
        grid = VGroup(VGroup(*entries[:7]).arrange(DOWN, buff=0.2, aligned_edge=LEFT),
                      VGroup(*entries[7:]).arrange(DOWN, buff=0.2, aligned_edge=LEFT))
        grid.arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to(DOWN * 0.95)
        self.say("这也是整个系列的缩影：从寄存器、内存、分支、函数，到指令编码和 CALL。",
                 LaggedStart(*[FadeIn(e, shift=UP * 0.1) for e in entries], lag_ratio=0.1, run_time=2.4))
        self.play(entries[-1][1].animate.set_color(YELLOW_D), entries[-1][0].animate.set_color(YELLOW_D))
        self.say("从一行 printf 到一串确定的比特，这就是程序运行前走过的路。",
                 Indicate(term, color=C_DONE, scale_factor=1.05))
        self.hold(0.5)
