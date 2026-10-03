import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---------------------------------------------------------------- the numbers, checked
M32 = 0xFFFFFFFF
OP_BRANCH, OP_JAL, OP_LUI, OP_AUIPC, OP_ARITH_I, OP_STORE = (
    0b1100011, 0b1101111, 0b0110111, 0b0010111, 0b0010011, 0b0100011)


def sext(v, bits):
    v &= (1 << bits) - 1
    return v - (1 << bits) if v >> (bits - 1) else v


def _b(v, hi, lo):
    return (v >> lo) & ((1 << (hi - lo + 1)) - 1)


def enc_b(imm, rs2, rs1, f3):
    i = imm & 0x1FFF
    return (_b(i, 12, 12) << 31 | _b(i, 10, 5) << 25 | rs2 << 20 | rs1 << 15 | f3 << 12
            | _b(i, 4, 1) << 8 | _b(i, 11, 11) << 7 | OP_BRANCH)


def enc_j(imm, rd):
    i = imm & 0x1FFFFF
    return _b(i, 20, 20) << 31 | _b(i, 10, 1) << 21 | _b(i, 11, 11) << 20 | _b(i, 19, 12) << 12 | rd << 7 | OP_JAL


def dec_j(w):
    imm = _b(w, 31, 31) << 20 | _b(w, 30, 21) << 1 | _b(w, 20, 20) << 11 | _b(w, 19, 12) << 12
    return _b(w, 6, 0), _b(w, 11, 7), sext(imm, 21)


def enc_u(imm20, rd, op):
    return imm20 << 12 | rd << 7 | op


def enc_i(imm, rs1, f3, rd, op=OP_ARITH_I):
    return (imm & 0xFFF) << 20 | rs1 << 15 | f3 << 12 | rd << 7 | op


def enc_s(imm, rs2, rs1, f3):
    return _b(imm, 11, 5) << 25 | rs2 << 20 | rs1 << 15 | f3 << 12 | _b(imm, 4, 0) << 7 | OP_STORE


def hi_lo(x):
    """Split a 32-bit constant for lui/auipc + addi/jalr."""
    hi, lo = ((x + 0x800) >> 12) & 0xFFFFF, sext(x & 0xFFF, 12)
    assert ((hi << 12) + lo) & M32 == x
    return hi, lo


# the notes' loop with toy addresses: beq at 0x0C, End at 0x1C
ADDRS = [0x0C, 0x10, 0x14, 0x18, 0x1C]
MOVED = [a + 0x1000 for a in ADDRS]
assert ADDRS[1] - ADDRS[0] == 4                     # beq not taken
assert ADDRS[4] - ADDRS[0] == 16 == 0x10            # beq taken -> End
assert ADDRS[0] - ADDRS[3] == -12                   # j Loop
assert MOVED[4] - MOVED[0] == 16 and MOVED[0] - MOVED[3] == -12
assert (MOVED[0], MOVED[3], MOVED[4]) == (0x100C, 0x1018, 0x101C)

# beq x19, x10, End (+16) and j Loop = jal x0, -12
B13 = format(16, "013b")                            # offset bits 12..0
J21 = format(-12 & 0x1FFFFF, "021b")                # offset bits 20..0
assert B13 == "0000000010000" and J21 == "111111111111111110100"
BEQ = enc_b(16, 10, 19, 0b000)
JLOOP = enc_j(-12, 0)
assert BEQ == 0x00A98863 and JLOOP == 0xFF5FF06F
assert dec_j(JLOOP) == (OP_JAL, 0, -12)
B_ROUTES = [(0, [0]), (1, list(range(2, 8))), (5, list(range(8, 12))), (6, [1])]
J_ROUTES = [(0, [0]), (1, list(range(10, 20))), (2, [9]), (3, list(range(1, 9)))]
assert ("".join("".join(B13[k] for k in ks) for _, ks in B_ROUTES[:2]) + "01010" + "10011" + "000"
        + "".join("".join(B13[k] for k in ks) for _, ks in B_ROUTES[2:]) + "1100011") == format(BEQ, "032b")
assert "".join("".join(J21[k] for k in ks) for _, ks in J_ROUTES) + "00000" + "1101111" == format(JLOOP, "032b")

# S vs B: which instruction bits hold which immediate bits
S_MEAN = {31: 11, **{25 + k: 5 + k for k in range(6)}, **{7 + k: k for k in range(5)}}
B_MEAN = {31: 12, **{25 + k: 5 + k for k in range(6)}, **{8 + k: 1 + k for k in range(4)}, 7: 11}
for ib, mb in B_MEAN.items():
    assert enc_b(1 << mb, 0, 0, 0) >> ib & 1
for ib, mb in S_MEAN.items():
    assert enc_s(1 << mb, 0, 0, 0) >> ib & 1
assert {b for b in S_MEAN if S_MEAN[b] != B_MEAN.get(b)} == {31, 7}
assert B_MEAN[8] == 1                               # inst[8] is imm[1]: 0 when offsets are multiples of 4

# ranges
assert (-(1 << 12), (1 << 12) - 2) == (-4096, 4094) and 4096 // 4 == 2 ** 10
assert (1 << 20) == 1024 * 1024 and (1 << 20) // 4 == 2 ** 18
assert (1 << 20) // (1 << 12) == 256 == 2 ** (20 - 12)

# li
assert hi_lo(0x87654321) == (0x87654, 0x321)
assert enc_u(0x87654, 10, OP_LUI) == 0x87654537 and enc_i(0x321, 10, 0, 10) == 0x32150513
assert sext(0xAFE, 12) & M32 == 0xFFFFFAFE == (0xAFE - 0x1000) & M32
assert (0xB0BAC000 + 0xFFFFFAFE) & M32 == 0xB0BABAFE
assert (0xB0BAD000 + 0xFFFFFAFE) & M32 == 0xB0BACAFE
assert hi_lo(0xB0BACAFE) == (0xB0BAD, sext(0xAFE, 12))
assert hi_lo(0x44331416) == (0x44331, 0x416)
assert format(0xAFE, "012b") == "101011111110" and format(0x321, "012b") == "001100100001"

# registers -> binary (the notes' exercise)
assert [format(ABI_NAMES.index(r), "05b") for r in ("s0", "sp", "t4")] == ["01000", "00010", "11101"]
assert format(9, "05b") == "01001" and ABI_NAMES.index("t4") == 29

# the notes' example.S / example.bin
TABLE = [
    ("addi sp, sp, -4", enc_i(-4, 2, 0, 2), "11111111110000010000000100010011"),
    ("sw   ra, 0(sp)", enc_s(0, 1, 2, 0b010), "00000000000100010010000000100011"),
    ("addi s0, sp, 4", enc_i(4, 2, 0, 8), "00000000010000010000010000010011"),
    ("mv   a0, a5", enc_i(0, 15, 0, 10), "00000000000001111000010100010011"),
    ("call printf", enc_j(0x40004, 1), "00000000010001000000000011101111"),
]
for _, w, s in TABLE:
    assert format(w, "032b") == s


def bracket(x0, x1, y, color, up=True, tick=0.15):
    d = -tick if up else tick
    return VGroup(
        Line([x0, y, 0], [x1, y, 0], stroke_color=color, stroke_width=3),
        Line([x0, y, 0], [x0, y + d, 0], stroke_color=color, stroke_width=3),
        Line([x1, y, 0], [x1, y + d, 0], stroke_color=color, stroke_width=3),
    )




def left_at(listing, x, y):
    """Put a CodeListing's text left edge at x and its first line at y."""
    listing.shift(RIGHT * (x - listing.lines.get_left()[0]) + UP * (y - listing[0].get_center()[1]))
    return listing


class Ep12Addressing(FormatScene):
    def construct(self):
        self.title_card()
        self.modes()
        self.offsets()
        self.encode_loop()
        self.s_vs_b()
        self.far_branch()
        self.anywhere()
        self.big_constants()
        self.recipe()
        self.end_card(
            [
                "寻址方式：基址 + 偏移、PC 相对、绝对",
                "偏移 = 目标地址 − 当前指令地址，搬家不变",
                "分支太远：条件取反，跳过一条 j（±1 MiB）",
                "任意地址：lui 或 auipc 配合 jalr",
                "拆常数：低 12 位的最高位是 1，高 20 位先加 1",
            ],
        )

    # ------------------------------------------------------------------ addressing modes
    def _card(self, x, title, color, formula, code_lines):
        box = RoundedRectangle(corner_radius=0.15, width=4.2, height=3.3, stroke_color=color, stroke_width=3,
                               fill_color=color, fill_opacity=0.06).move_to([x, 0.75, 0])
        t = zh(title, 30, color)
        f = (zh if NEEDS_TR.search(formula) else mono)(formula, 26, WHITE)
        for m in (t, f):
            if m.width > 3.8:
                m.scale_to_fit_width(3.8)
        t.move_to(box.get_top() + DOWN * 0.42)
        f.next_to(t, DOWN, buff=0.25)
        rule = Line(LEFT * 1.8, RIGHT * 1.8, stroke_color=color, stroke_width=1.5,
                    stroke_opacity=0.6).next_to(f, DOWN, buff=0.22).set_x(x)
        code = CodeListing(code_lines, font_size=24, line_gap=0.46)
        code.next_to(rule, DOWN, buff=0.28).set_x(x)
        return box, t, f, rule, code

    def modes(self):
        head = self.heading("三种寻址方式")
        self.say("6 种指令格式已经凑齐。这一集换个角度：指令要访问的地址、要跳去的目标，是怎么算出来的？"
                 "这些计算规则叫寻址方式（addressing mode）。RISC-V 主要用到三种。",
                 Write(head))
        c1 = self._card(-4.5, "基址 + 偏移", C_T, "R[rs1] + imm",
                        ["lw   x10, 8(x2)", "sw   x10, 8(x2)", "jalr x0, 0(ra)"])
        c2 = self._card(0, "PC 相对", YELLOW_D, "PC + imm",
                        ["beq  x19, x10, End", "jal  ra, func", "auipc t0, 0x12345"])
        c3 = self._card(4.5, "绝对", RED_B, "直接给出完整地址",
                        ["lui  ra, hi", "jalr ra, lo(ra)"])
        self.cue(tr("这些计算规则叫寻址方式"),
                 LaggedStart(*[FadeIn(VGroup(c[0], c[1]), shift=UP * 0.15) for c in (c1, c2, c3)],
                             lag_ratio=0.25))
        self.say("第一种：基址 + 偏移（base/displacement），地址 = 寄存器 + 立即数。lw 和 sw 就是这样找到数据的。"
                 "jalr 也属于这一类：跳到 rs1 + 立即数。新 PC 只取决于寄存器，与 jalr 自己在哪儿无关。",
                 FadeIn(c1[2]), Create(c1[3]), FadeIn(c1[4][0]), FadeIn(c1[4][1]))
        self.cue(tr("jalr 也属于这一类"), FadeIn(c1[4][2], shift=UP * 0.1))
        self.say("第二种：PC 相对寻址，以 PC 为基准加上偏移。条件分支、jal 和 auipc 都用它。"
                 "第三种：绝对寻址，直接给出完整地址。比如 lui 装入地址的高 20 位，jalr 补上低 12 位并跳过去。",
                 FadeIn(c2[2]), Create(c2[3]), LaggedStart(*[FadeIn(l) for l in c2[4]], lag_ratio=0.3))
        self.cue(tr("第三种：绝对寻址"),
                 FadeIn(c3[2]),
                 Create(c3[3]),
                 LaggedStart(*[FadeIn(l) for l in c3[4]], lag_ratio=0.3))
        rest = zh("其余指令：PC + 4", 24, YELLOW_D).next_to(c2[0], DOWN, buff=0.18)
        jbox = SurroundingRectangle(c1[4][2], color=RED_B, buff=0.08)
        self.say("其实几乎每条指令都以 PC 相对的方式更新 PC：普通指令 PC + 4，分支和 jal 是 PC + 偏移。只有 jalr 例外。"
                 "伪指令也各有归属：j 是 jal x0 的简写，属于 PC 相对；jr 和 ret 则是 jalr 的简写。",
                 FadeIn(rest, shift=UP * 0.1), Indicate(c2[0], color=YELLOW_D, scale_factor=1.03))
        self.cue(tr("只有 jalr 例外"), Create(jbox))
        pseudo = mono("j L = jal x0, L     jr rs = jalr x0, 0(rs)     ret = jalr x0, 0(ra)", 22, GREY_A)
        pseudo.move_to(DOWN * 1.95)
        self.cue(tr("伪指令也各有归属"), FadeIn(pseudo, shift=UP * 0.1))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ labels -> offsets
    def offsets(self):
        head = self.heading("从标签到偏移")
        code = left_at(CodeListing([
            "Loop: beq  x19, x10, End",
            "      add  x18, x18, x10",
            "      addi x19, x19, -1",
            "      j    Loop",
            "End:  ...",
        ], font_size=30, line_gap=0.62), -2.6, 2.2)

        def addr_texts(vals):
            return VGroup(*[mono(f"0x{a:02X}", 26, GREY).next_to(code.left_of(i, 0.45), LEFT, buff=0)
                            for i, a in enumerate(vals)])

        addrs = addr_texts(ADDRS)
        moved = addr_texts(MOVED)
        self.say("来算几个具体的偏移。这是课程笔记里的循环，每条指令都标了示例地址：beq 在 0x0C。"
                 "标签不是指令，机器码里根本没有 Loop 和 End。汇编器得把它们换算成相对 PC 的偏移。",
                 Write(head), FadeIn(code, shift=UP * 0.2), FadeIn(addrs))
        self.cue(tr("标签不是指令"),
                 Circumscribe(code.glyphs(0, "Loop:"), color=C_LABEL),
                 Circumscribe(code.glyphs(4, "End:"), color=C_LABEL))
        calc_y = -1.25
        p4 = CurvedArrow(code.right_of(0, 0.25), code.right_of(1, 0.25), angle=-TAU / 3, color=GREEN_B)
        p4_l = mono("+4", 28, GREEN_B).next_to(p4, RIGHT, buff=0.12)
        calc = mono("0x10 − 0x0C = +4", 30, GREEN_B).move_to([0.3, calc_y, 0])
        self.say("情况一：beq 不跳。PC 走到下一条，偏移是 +4。"
                 "情况二：beq 跳到 End。0x1C − 0x0C = 0x10，偏移 +16，也就是往后 4 条指令。"
                 "情况三：j Loop 从 0x18 跳回 0x0C。0x0C − 0x18 = −12，往回 3 条指令：偏移可以是负数。", Create(p4), FadeIn(p4_l), FadeIn(calc))
        p16 = CurvedArrow(code.right_of(0, 0.25), code.right_of(4, 0.25), angle=-TAU / 4, color=YELLOW_D)
        p16_l = mono("+16", 30, YELLOW_D).next_to(p16, RIGHT, buff=0.15)
        calc2 = mono("0x1C − 0x0C = 0x10 = +16", 30, YELLOW_D).move_to(calc)
        self.cue(tr("情况二"), Create(p16), FadeIn(p16_l), Transform(calc, calc2))
        xl = moved.get_left()[0] - 0.2
        m12 = CurvedArrow([xl, code[3].get_center()[1], 0], [xl, code[0].get_center()[1], 0],
                          angle=-TAU / 4, color=RED_B)
        m12_l = mono("−12", 30, RED_B).next_to(m12, LEFT, buff=0.15)
        calc3 = mono("0x0C − 0x18 = −12", 30, RED_B).move_to(calc)
        self.cue(tr("情况三"), Create(m12), FadeIn(m12_l), Transform(calc, calc3))
        self.hold()
        calc4 = mono("0x101C − 0x100C = +16     0x100C − 0x1018 = −12", 26, WHITE).move_to(calc)
        self.say("上一集提过位置无关代码。把整个循环搬到 0x100C：地址全变了，+16 和 −12 却一个都不用改。"
                 "反过来，要是指令里写死“跳到 0x1C”，一搬家就跳错了：绝对地址经不起代码搬家。",
                 *[Transform(a, b) for a, b in zip(addrs, moved)], Transform(calc, calc4), run_time=1.5)
        self.cue(tr("一个都不用改"), Indicate(p16_l, color=YELLOW_D), Indicate(m12_l, color=RED_B))
        bad = zh("写死“跳到 0x1C”？搬家后 End 在 0x101C，跳错了！", 28, RED_B).move_to(calc)
        if bad.width > 11.5:
            bad.scale_to_fit_width(11.5)
        self.cue(tr("反过来"), FadeOut(calc, shift=UP * 0.15), FadeIn(bad, shift=UP * 0.15))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ encode beq and j
    def encode_loop(self):
        head = self.heading("手工汇编：beq 与 j")
        asm = CodeListing(["beq x19, x10, End     # End = PC + 16"], font_size=32).move_to(UP * 2.45)
        bbf = BitField(fmt_fields("B")).move_to(DOWN * 0.35)
        row = bit_row(B13, YELLOW_D, box=0.42, font_size=24).move_to(UP * 1.45)
        idx = VGroup(*[mono(str(12 - k), 16, GREY).next_to(row[k], UP, buff=0.08) for k in range(13)])
        lab = mono("+16 =", 28, YELLOW_D).next_to(row, LEFT, buff=0.3)
        self.say("现在编成机器码。先是 beq x19, x10, End，偏移 +16：上一集算过，快速过一遍。"
                 "接着填上 rs2 = x10、rs1 = x19、funct3 = 000、opcode = 1100011，得到 0x00A98863。",
                 Write(head), FadeIn(asm, shift=DOWN * 0.2), FadeIn(VGroup(bbf.frames, bbf.labels, bbf.ranges)),
                 FadeIn(row), FadeIn(idx), FadeIn(lab))
        cross = Cross(row[12], stroke_color=RED_C, stroke_width=4)
        self.play(Create(cross), run_time=0.5)
        self.fly_bits(row, bbf, B_ROUTES, run_time=1.3)
        self.cue(tr("接着填上"))
        notes = self.encode(bbf, [(2, "01010", "x10"), (3, "10011", "x19"), (4, "000", "beq"),
                                  (7, "1100011", "branch")], rt=0.45)
        hx = self.hex_of(bbf, -2.0)
        assert hx.text == f"0x{BEQ:08X}"
        self.hold()
        self.play(FadeOut(VGroup(bbf, notes, hx, row, idx, lab, cross)))

        asm2 = CodeListing(["jal x0, Loop     # Loop = PC - 12"], font_size=32).move_to(asm)
        jbf = BitField(fmt_fields("J")).move_to(DOWN * 0.35)
        self.say("再编码 j Loop。j 是伪指令，实际是 jal x0, Loop：返回地址写进 x0，也就是直接丢掉。"
                 "J 型的偏移有 21 位。−12 是负数，写成 21 位补码：高 17 位全是 1，最后 4 位是 0100。",
                 Transform(asm, asm2), FadeIn(VGroup(jbf.frames, jbf.labels, jbf.ranges)))
        row = bit_row(J21, YELLOW_D, box=0.4, font_size=22).move_to(UP * 1.45 + RIGHT * 0.55)
        idx = VGroup(*[mono(str(20 - k), 14, GREY).next_to(row[k], UP, buff=0.08) for k in range(21)])
        lab = mono("−12 =", 28, YELLOW_D).next_to(row, LEFT, buff=0.3)
        self.cue(tr("J 型的偏移有 21 位"), FadeIn(row), FadeIn(idx), FadeIn(lab))
        cross = Cross(row[20], stroke_color=RED_C, stroke_width=4)
        self.say("最低位照例不存，其余各位按 imm[20|10:1|11|19:12] 的顺序对号入座。"
                 "rd = x0，写成 00000；jal 的 opcode 是 1101111。"
                 "结果是 0xFF5FF06F。开头的 FF 和中间的 FF，都来自负偏移高位的那一串 1。", Create(cross))
        self.fly_bits(row, jbf, J_ROUTES, run_time=2.0)
        self.cue(tr("rd = x0，写成"))
        notes = self.encode(jbf, [(4, "00000", "x0"), (5, "1101111", "jal")], rt=0.6)
        self.cue(tr("结果是 0xFF5FF06F"))
        hx = self.hex_of(jbf, -2.0)
        assert hx.text == f"0x{JLOOP:08X}"
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ S vs B
    def s_vs_b(self):
        head = self.heading("S 型与 B 型：只差两位")
        F = FIELD_COLORS
        s_fine = [("imm[11]", 1, F["imm"], "11"), ("imm[10:5]", 6, F["imm"]), ("rs2", 5, F["rs2"]),
                  ("rs1", 5, F["rs1"]), ("funct3", 3, F["funct3"]), ("imm[4:1]", 4, F["imm"]),
                  ("imm[0]", 1, F["imm"], "0"), ("opcode", 7, F["opcode"])]
        sbf = BitField(s_fine)
        bbf = BitField(fmt_fields("B"))
        stack = VGroup(sbf, bbf).arrange(DOWN, buff=0.55).move_to(UP * 0.6)
        tags = VGroup(mono("S", 32, WHITE).next_to(sbf.frames, LEFT, buff=0.35),
                      mono("B", 32, WHITE).next_to(bbf.frames, LEFT, buff=0.35))
        self.say("把 S 型和 B 型上下对齐：两者的立即数都分成两段，占着同样的位置。"
                 "inst[30:25] 在两者中都是 imm[10:5]，inst[11:8] 都是 imm[4:1]：含义完全相同。",
                 Write(head), FadeIn(stack, shift=UP * 0.1), FadeIn(tags))
        left = sbf.frames.get_left()[0]
        bw = sbf.box_w

        def band(hi, lo, color):
            xl = left + (31 - hi) * bw
            xr = left + (32 - lo) * bw
            top = stack.get_top()[1] + 0.08
            bot = stack.get_bottom()[1] - 0.08
            return Rectangle(width=xr - xl, height=top - bot, stroke_color=color, stroke_width=3,
                             fill_color=color, fill_opacity=0.08).move_to([(xl + xr) / 2, (top + bot) / 2, 0])

        same = VGroup(band(30, 25, GREEN_B), band(11, 8, GREEN_B))
        self.cue(tr("inst[30:25] 在两者中"), *[Create(b) for b in same])
        diff31 = band(31, 31, RED_B)
        leg1 = mono("inst[31]:  S imm[11] → B imm[12]", 22, RED_B)
        leg2 = mono("inst[7]:  S imm[0] → B imm[11]", 22, RED_B)
        legs = VGroup(leg1, leg2).arrange(RIGHT, buff=0.9).move_to(DOWN * 1.65)
        self.say("真正换了含义的只有两位。inst[31] 在 S 型是 imm[11]，在 B 型是 imm[12]，但始终是符号位；"
                 "inst[7] 在 S 型是 imm[0]，在 B 型是 imm[11]。硬件拼立即数时，只有这两位要分情况处理。",
                 Create(diff31), FadeIn(leg1, shift=UP * 0.1))
        diff7 = band(7, 7, RED_B)
        self.cue(tr("inst[7] 在 S 型"), Create(diff7), FadeIn(leg2, shift=UP * 0.1))
        self.hold()
        slot = bbf.field_digits[5][3]
        q_box = Rectangle(width=bw, height=bbf.box_h, stroke_color=YELLOW_D, stroke_width=4).move_to(slot)
        q = mono("?", 24, YELLOW_D).move_to(slot)
        self.say("小测验：如果程序里只有 32 位指令，B 型指令的 inst[8] 是不是一定为 0？"
                 "是的。这时偏移都是 4 的倍数，imm[1] 恒为 0，而它正好存在 inst[8]。"
                 "偏移以 2 字节为单位，分支不可能只挪 1 个字节；而只有 32 位指令时，能编码的目标里还有一半用不上。",
                 FadeOut(same), FadeOut(diff31), FadeOut(diff7), FadeOut(legs), Create(q_box), FadeIn(q))
        zero = mono("0", 24, GREEN_B).move_to(slot)
        ans = mono("inst[8] = imm[1] = 0", 24, GREEN_B).move_to(DOWN * 1.65)
        self.cue(tr("是的"), Transform(q, zero), q_box.animate.set_stroke(GREEN_B), FadeIn(ans, shift=UP * 0.1))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ branching far
    @staticmethod
    def _range_label(pre, power, color):
        # the CJK font has no superscript digits, so the power goes in the mono font
        a = zh(pre, 22, color)
        b = mono(power, 22, color).next_to(a, RIGHT, buff=0.04)
        c = zh("条指令）", 22, color).next_to(b, RIGHT, buff=0.12)
        return VGroup(a, b, c)

    def far_branch(self):
        head = self.heading("分支够不着怎么办？")
        y = 2.0
        nl = Line([-6.3, y, 0], [6.3, y, 0], stroke_color=GREY_B, stroke_width=2)
        tick = Line([0, y - 0.12, 0], [0, y + 0.12, 0], stroke_color=YELLOW_D, stroke_width=3)
        pc = mono("PC", 22, YELLOW_D).next_to(tick, DOWN, buff=0.1)
        scale = zh("示意图，未按比例", 20, GREY).to_corner(UR, buff=0.45)
        b_br = bracket(-1.6, 1.6, y + 0.35, YELLOW_D, up=True)
        b_lab = self._range_label("B 型：±4 KiB（", "±2¹⁰", YELLOW_D).next_to(b_br, UP, buff=0.12)
        self.say("上一集算过：B 型偏移的范围是 −4096 到 +4094 字节，约 ±4 KiB，也就是前后各 2 的 10 次方条指令。"
                 "if 和循环通常很短，这个范围绰绰有余。可要是目标 far 远在 4 KiB 之外，beq x10, x0, far 就够不着了。",
                 Write(head), Create(nl), Create(tick), FadeIn(pc), FadeIn(scale),
                 Create(b_br), FadeIn(b_lab, shift=DOWN * 0.1))
        far = Dot([4.8, y, 0], radius=0.09, color=RED_B)
        far_l = mono("far", 24, C_LABEL).next_to(far, UP, buff=0.12)
        orig = left_at(CodeListing(["      beq x10, x0, far"], font_size=28), -5.6, 0.25)
        nope = zh("够不着！", 26, RED_B).next_to(orig, RIGHT, buff=0.5)
        self.cue(tr("if 和循环通常很短"), FadeIn(far), FadeIn(far_l), FadeIn(orig, shift=UP * 0.1))
        self.cue(tr("beq x10, x0, far 就够不着了"),
                 FadeIn(nope, shift=LEFT * 0.1),
                 Indicate(far, color=RED_B, scale_factor=1.6))
        new = left_at(CodeListing(["      bne x10, x0, next", "      j   far", "next: ..."],
                                  font_size=28, line_gap=0.55), -5.6, 0.25)
        self.say("办法：把条件取反，让分支只负责跳过一条 j。"
                 "x10 等于 0 时，bne 不跳，执行 j far，跳到远处。"
                 "x10 不等于 0 时，bne 跳过 j，直接到 next 继续。效果和原来的 beq 完全一样。",
                 FadeOut(nope), ReplacementTransform(orig, new[0]), FadeIn(new[1:], shift=DOWN * 0.1))

        box = new.line_box(0)
        case1 = mono("x10 = 0", 26, YELLOW_D).move_to([-3.2, -1.55, 0])
        self.cue(tr("x10 等于 0 时"), FadeIn(box), FadeIn(case1))
        self.cue(tr("执行 j far"), box.animate.become(new.line_box(1)))
        p0 = new.glyphs(1, "far").get_right() + RIGHT * 0.15
        p1 = np.array([far.get_center()[0], p0[1], 0])
        path = VGroup(Line(p0, p1, stroke_color=YELLOW_D, stroke_width=4),
                      Arrow(p1, far.get_center() + DOWN * 0.12, buff=0, color=YELLOW_D, stroke_width=4))
        self.cue(tr("跳到远处"), Create(path[0]), run_time=0.6)
        self.play(GrowArrow(path[1]), run_time=0.6)
        case2 = mono("x10 ≠ 0", 26, TEAL_C).move_to(case1)
        box2 = new.line_box(0, color=TEAL_C)
        skip = CurvedArrow(new.right_of(0, 0.3), new.right_of(2, 0.3), angle=-TAU / 4, color=TEAL_C)
        self.cue(tr("x10 不等于 0 时"), FadeOut(path), Transform(case1, case2), Transform(box, box2))
        self.cue(tr("直接到 next 继续"), Create(skip), box.animate.become(new.line_box(2, color=TEAL_C)))
        self.hold()
        j_br = bracket(-6.2, 6.2, y - 0.6, BLUE_B, up=False)
        j_lab = self._range_label("J 型：±1 MiB（", "±2¹⁸", BLUE_B).next_to(j_br, DOWN, buff=0.12)
        self.say("j 是 J 型，偏移有 21 位，能到约 ±1 MiB，即前后各 2 的 18 次方条指令。"
                 "这也是无条件跳转用 j、不用 beq x0, x0 的原因：J 型没有 rs1、rs2 和 funct3，省下的位让偏移多出 8 位，范围大 256 倍。",
                 FadeOut(box), FadeOut(case1), FadeOut(skip), Create(j_br), FadeIn(j_lab, shift=UP * 0.1))
        self.cue(tr("这也是无条件跳转"), Indicate(j_lab, color=BLUE_B), Indicate(b_lab, color=YELLOW_D))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ jumping anywhere
    def anywhere(self):
        head = self.heading("跳到任意地址")
        a_t = zh("绝对：lui + jalr", 28, RED_B)
        a_c = CodeListing([
            "lui   ra, hi         # ra = hi << 12",
            "jalr  ra, lo(ra)     # PC = ra + lo; ra = PC + 4",
        ], font_size=26, line_gap=0.52)
        b_t = zh("PC 相对：auipc + jalr", 28, YELLOW_D)
        b_c = CodeListing([
            "auipc ra, hi         # ra = PC + (hi << 12)",
            "jalr  ra, lo(ra)     # PC = ra + lo; ra = PC + 4",
        ], font_size=26, line_gap=0.52)
        x0 = -5.8
        for t, c, yt in ((a_t, a_c, 1.9), (b_t, b_c, -0.3)):
            t.move_to([0, yt, 0]).align_to([x0, 0, 0], LEFT)
            left_at(c, x0 + 0.3, yt - 0.62)
        self.say("上一集说过，auipc 配 jalr 能跳到 32 位地址空间的任何位置。其实还有一种组合：lui 配 jalr。"
                 "先看绝对版本：lui 装入目标地址的高 20 位，jalr 加上低 12 位并跳过去。目标是一个固定的地址。",
                 Write(head), FadeIn(b_t, shift=RIGHT * 0.1), FadeIn(b_c, shift=RIGHT * 0.1))
        self.cue(tr("先看绝对版本"), FadeIn(a_t, shift=RIGHT * 0.1), FadeIn(a_c, shift=RIGHT * 0.1))
        self.say("jalr 用旧的 ra 算目标，同时把 PC + 4 写进 ra：同一个 ra 既当基址，又存返回地址。"
                 "auipc 版本则是 PC 相对的：ra = PC + (hi << 12)。目标跟着代码一起走，整段搬家也照样正确。",
                 Circumscribe(a_c.glyphs(1, "lo(ra)"), color=C_RA),
                 Circumscribe(a_c.glyphs(1, "ra = PC + 4"), color=C_RA))
        self.cue(tr("auipc 版本则是 PC 相对的"),
                 Indicate(b_t, color=YELLOW_D),
                 Circumscribe(b_c.glyphs(0, "PC + (hi << 12)"), color=YELLOW_D))
        b2 = CodeListing([
            "auipc t1, hi         # t1 = PC + (hi << 12)",
            "jalr  x0, lo(t1)     # PC = t1 + lo，不保存返回地址",
        ], font_size=26, line_gap=0.52)
        b2.shift(b_c[0].get_left() - b2[0].get_left())
        self.say("伪指令 call 展开的正是这一对。"
                 "只想跳走、不必返回时，jalr 的 rd 改成 x0；中转寄存器也换成 t1，免得冲掉 ra 里的返回地址。"
                 "注意：jalr 的 12 位立即数也会符号扩展。hi 和 lo 该怎么拆？这和 li 是同一个问题。", Circumscribe(VGroup(b_t, b_c), color=YELLOW_D))
        self.cue(tr("只想跳走"), Transform(b_c[0], b2[0]), Transform(b_c[1], b2[1]))
        lo_boxes = VGroup(SurroundingRectangle(a_c.glyphs(1, "lo"), color=YELLOW_D, buff=0.06),
                          SurroundingRectangle(b2.glyphs(1, "lo"), color=YELLOW_D, buff=0.06))
        self.cue(tr("注意：jalr"), *[Create(b) for b in lo_boxes])
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ li
    def _split(self, hi, lo, y=1.3):
        big = VGroup(mono("0x", 50, GREY_A), mono(hi, 50, YELLOW_D), mono(lo, 50, TEAL_C))
        big.arrange(RIGHT, buff=0.06, aligned_edge=DOWN).move_to([0, y, 0])
        div = DashedLine(UP * 0.4, DOWN * 0.4, stroke_color=GREY_B).move_to(
            [(big[1].get_right()[0] + big[2].get_left()[0]) / 2, y, 0])
        l_hi = zh("高 20 位 → lui", 22, YELLOW_D).next_to(big, DOWN, buff=0.25)
        l_hi.align_to(div, RIGHT).shift(LEFT * 0.12)
        l_lo = zh("低 12 位 → addi", 22, TEAL_C).next_to(big, DOWN, buff=0.25)
        l_lo.align_to(div, LEFT).shift(RIGHT * 0.12)
        return VGroup(big, div, l_hi, l_lo)

    def _code2(self, lines, y=-0.2):
        return left_at(CodeListing(lines, font_size=28, line_gap=0.55), -5.6, y)

    def _imm12(self, v, color, y=-1.8):
        row = bit_row(format(v, "012b"), GREY_B, box=0.4, font_size=24)
        lab = mono(f"0x{v:03X} =", 26, WHITE).next_to(row, LEFT, buff=0.3)
        g = VGroup(lab, row).move_to([0.6, y, 0])
        hl = SurroundingRectangle(row[0], color=color, buff=0.03, stroke_width=4)
        tag = mono("bit 11", 20, color).next_to(hl, UP, buff=0.08)
        return g, row, VGroup(hl, tag)

    def big_constants(self):
        head = self.heading("练习：li 与大常数")
        li = CodeListing(["li x10, 0x87654321"], font_size=34).move_to(UP * 2.4)
        self.say("用笔记里的两道题，练练上一集的 lui + addi。先交代一句：常数在 −2048 到 2047 之间时，li 只需一条 addi。"
                 "练习一：li x10, 0x87654321。高 20 位 0x87654 交给 lui，低 12 位 0x321 交给 addi。",
                 Write(head), FadeIn(li, shift=DOWN * 0.15))
        sp = self._split("87654", "321")
        self.cue(tr("练习一"), FadeIn(sp[0]), Create(sp[1]), FadeIn(sp[2:], shift=UP * 0.1))
        code = self._code2(["lui  x10, 0x87654        # x10 = 0x87654000",
                            "addi x10, x10, 0x321     # x10 = 0x87654321"])
        g, row, hl = self._imm12(0x321, GREEN_B)
        self.play(FadeIn(code[0], shift=RIGHT * 0.1))
        self.say("lui 先得到 0x87654000。0x321 的最高位是 0，符号扩展后不变，一加正好是 0x87654321。"
                 "顺手汇编成机器码：lui 是 U 型，opcode 为 0110111（auipc 是 0010111），得到 0x87654537；addi 则是 0x32150513。",
                 FadeIn(g), Create(hl[0]), FadeIn(hl[1]), FadeIn(code[1], shift=RIGHT * 0.1))
        mc = VGroup(mono("→ 0x87654537", 28, C_NUM), mono("→ 0x32150513", 28, C_NUM))
        for k in range(2):
            mc[k].move_to(code.glyphs(k, "#").get_left(), aligned_edge=LEFT).set_y(code[k].get_center()[1])
        ops = mono("opcode:  lui 0110111   auipc 0010111", 22, GREY_A).move_to(DOWN * 1.8)
        self.cue(tr("顺手汇编成机器码"),
                 FadeOut(g),
                 FadeOut(hl),
                 *[FadeOut(code.glyphs(k, c)) for k, c in ((0, "# x10 = 0x87654000"), (1, "# x10 = 0x87654321"))],
                 FadeIn(mc, shift=LEFT * 0.1),
                 FadeIn(ops))
        self.hold()

        li2 = CodeListing(["li x10, 0xB0BACAFE"], font_size=34).move_to(li)
        sp2 = self._split("B0BAC", "AFE")
        code2 = self._code2(["lui  x10, 0xB0BAC", "addi x10, x10, 0xAFE"])
        self.say("练习二：li x10, 0xB0BACAFE。照葫芦画瓢，写成 lui x10, 0xB0BAC 和 addi x10, x10, 0xAFE？"
                 "问题出在 0xAFE：它的最高位是 1，作为 12 位补码是负数，会被符号扩展成 0xFFFFFAFE。"
                 "0xB0BAC000 + 0xFFFFFAFE = 0xB0BABAFE：高 20 位少了 1！",
                 FadeOut(VGroup(code, mc, ops)), Transform(li, li2), ReplacementTransform(sp, sp2),
                 FadeIn(code2, shift=RIGHT * 0.1))
        g, row, hl = self._imm12(0xAFE, RED_B)
        self.cue(tr("问题出在 0xAFE"), FadeIn(g), Create(hl[0]), FadeIn(hl[1]))
        calc = VGroup(
            mono("  0xB0BAC000", 30, WHITE),
            mono("+ 0xFFFFFAFE", 30, WHITE),
            mono("= 0xB0BABAFE", 30, RED_B),
        ).arrange(DOWN, buff=0.16, aligned_edge=RIGHT).move_to([3.4, -0.75, 0])
        bar = Line(LEFT, RIGHT, stroke_color=GREY_B).match_width(calc).next_to(calc[1], DOWN, buff=0.08)
        wrong = zh("高 20 位少了 1！", 24, RED_B).next_to(calc, UP, buff=0.2)
        self.cue(tr("0xB0BAC000 + 0xFFFFFAFE"), FadeIn(calc[:2]), Create(bar), FadeIn(calc[2]), FadeIn(wrong))
        why = mono("0xFFFFFAFE = 0xAFE − 0x1000", 28, GREY_A).move_to([0, -1.8, 0])
        self.say("因为 0xFFFFFAFE 等于 0xAFE − 0x1000：加上它，就是加 0xAFE 再减 0x1000，正好从高 20 位扣掉 1。"
                 "所以要预先给高 20 位加 1：lui x10, 0xB0BAD。0xB0BAD000 + 0xFFFFFAFE = 0xB0BACAFE，对了。",
                 FadeOut(g), FadeOut(hl), FadeIn(why, shift=UP * 0.1))
        fix = self._code2(["lui  x10, 0xB0BAD", "addi x10, x10, 0xAFE"])
        calc2 = VGroup(
            mono("  0xB0BAD000", 30, WHITE),
            mono("+ 0xFFFFFAFE", 30, WHITE),
            mono("= 0xB0BACAFE", 30, GREEN_B),
        ).arrange(DOWN, buff=0.16, aligned_edge=RIGHT).move_to(calc)
        ok = zh("正确！", 24, GREEN_B).move_to(wrong)
        self.cue(tr("所以要预先给高 20 位加 1"),
                 FadeOut(why),
                 Transform(code2[0], fix[0]),
                 Transform(calc, calc2),
                 Transform(wrong, ok))
        self.cue(tr("对了"), Circumscribe(fix.glyphs(0, "0xB0BAD"), color=GREEN_B))
        self.hold()
        rule = VGroup(
            zh("低 12 位的最高位（第 11 位）是 1 → 高 20 位加 1", 28, YELLOW_D),
            mono("hi = (x + 0x800) >> 12", 30, WHITE),
        ).arrange(DOWN, buff=0.22)
        frame = SurroundingRectangle(rule, color=YELLOW_D, buff=0.22, corner_radius=0.1)
        rule_g = VGroup(frame, rule).move_to([0, 1.25, 0])
        self.say("规则：低 12 位的最高位（第 11 位）是 1，高 20 位就先加 1。写成公式：hi = (x + 0x800) >> 12。"
                 "上一节 lui 或 auipc 配 jalr，也照这条规则拆 hi 和 lo；用 auipc 时，x 是目标地址与 PC 之差。",
                 FadeOut(sp2), FadeIn(rule_g, shift=UP * 0.1))
        self.cue(tr("上一节 lui 或 auipc 配 jalr"), Indicate(rule[1], color=YELLOW_D))
        self.hold()
        self.play(FadeOut(VGroup(code2, calc, bar, wrong, rule_g)), FadeOut(li))
        q = CodeListing(["li   x5, 0x44331416"], font_size=34).move_to(UP * 1.6)
        ans = CodeListing(["lui  x5, 0x44331", "addi x5, x5, 0x416"], font_size=30, line_gap=0.55)
        ans.next_to(q, DOWN, buff=0.6).align_to(q, LEFT)
        bits = zh("2 × 32 = 64 位", 32, YELLOW_D).next_to(ans, DOWN, buff=0.55)
        self.say("小测验：li x5, 0x44331416 编码后占多少位？"
                 "答案是 64 位：li 是伪指令，这里要展开成 lui 和 addi 两条指令。", FadeIn(q, shift=UP * 0.1))
        self.cue(tr("答案是 64 位"), FadeIn(ans, shift=DOWN * 0.1), FadeIn(bits))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ recipe
    def recipe(self):
        def column(title, steps, color, left_x):
            t = zh(title, 30, color)
            rows = VGroup(*[zh(s, 22, WHITE) for s in steps]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            g = VGroup(t, rows).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            g.shift(RIGHT * (left_x - g.get_left()[0]) + UP * (3.55 - g.get_top()[1]))
            return g

        left = column("汇编 → 二进制", [
            "① 确定指令类型：R、I、I*、S、B、U、J",
            "② 找到对应的指令格式",
            "③ 把寄存器和立即数转成二进制",
            "④ 按格式摆放，填上 opcode 和 funct",
        ], YELLOW_D, -6.6)
        right = column("二进制 → 汇编", [
            "① 看 opcode（和 funct3/7）认出指令",
            "② 按格式把 32 位切成字段",
            "③ 翻译寄存器和立即数",
            "④ 拼出完整的汇编指令",
        ], TEAL_C, 0.35)
        self.say("最后把汇编与机器码的互译整理成两份清单。先看汇编 → 二进制；其中的 I* 就是第 10 集讲的移位格式。"
                 "第 ③ 步转寄存器时，先把 ABI 名换成编号：s0 是 x8，写作 01000；t4 是 x29，写作 11101。",
                 FadeIn(left[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in left[1]], lag_ratio=0.25))
        regs = VGroup(*[mono(t, 24, C_REG) for t in (
            "s0 = x8  → 01000", "sp = x2  → 00010", "x9       → 01001", "t4 = x29 → 11101")])
        regs.arrange_in_grid(2, 2, buff=(1.2, 0.25), col_alignments="ll").move_to(DOWN * 0.35)
        self.cue(tr("第 ③ 步转寄存器时"), Indicate(left[1][2], color=YELLOW_D), FadeIn(regs, shift=UP * 0.1))
        self.say("反方向就是第 10 集的反汇编，四步列在右边。手边备一张 61C 参考卡最方便。",
                 FadeIn(right[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in right[1]], lag_ratio=0.25))
        self.hold()

        jbf = BitField(fmt_fields("J"), bits=format(JLOOP, "032b")).move_to(DOWN * 1.05)
        word = mono(f"0x{JLOOP:08X}", 30, YELLOW_D).next_to(jbf.labels, UP, buff=0.12)
        word.align_to(jbf.frames, LEFT)
        mark = SurroundingRectangle(right[1][0], color=TEAL_C, buff=0.07)
        self.say("拿 J 型练一次：把 0xFF5FF06F 翻译回来。opcode 是 1101111，这是 jal。"
                 "按 J 型切开：rd 是 00000，即 x0；立即数按 imm[20|10:1|11|19:12] 拼回去，补上最低位的 0，得 −12。"
                 "拼起来就是 jal x0, −12：正是前面编码的 j Loop。",
                 FadeOut(regs), FadeIn(word), FadeIn(jbf), Create(mark))
        self.cue(tr("opcode 是 1101111"),
                 Indicate(jbf.frames[5], color=FIELD_COLORS["opcode"], scale_factor=1.08))
        imm = mono("imm = −12", 28, YELLOW_D)
        rd = mono("rd = x0", 28, FIELD_COLORS["rd"])
        res = VGroup(rd, imm).arrange(RIGHT, buff=1.2).next_to(jbf, DOWN, buff=0.2)
        self.cue(tr("按 J 型切开"),
                 mark.animate.become(SurroundingRectangle(VGroup(right[1][1], right[1][2]), color=TEAL_C, buff=0.07)),
                 Indicate(jbf.frames[4], color=FIELD_COLORS["rd"], scale_factor=1.08))
        self.cue(tr("rd 是 00000"), FadeIn(rd, shift=UP * 0.1))
        self.cue(tr("立即数按"), *[Indicate(jbf.frames[k], color=YELLOW_D, scale_factor=1.06) for k in range(4)])
        self.cue(tr("得 −12"), FadeIn(imm, shift=UP * 0.1))
        final = CodeListing(["jal x0, -12     # = j Loop"], font_size=30).move_to(res)
        self.cue(tr("拼起来就是"),
                 mark.animate.become(SurroundingRectangle(right[1][3], color=TEAL_C, buff=0.07)),
                 ReplacementTransform(res, final))
        self.hold()

        self.play(FadeOut(VGroup(jbf, word, final, mark, left, right)))
        entries = [("main:", None)] + [(a, s) for a, _, s in TABLE]
        asm_col = CodeListing([a for a, _ in entries], font_size=26, line_gap=0.5)
        bin_col = VGroup(*[mono(s if s else "（无）", 26, WHITE if s else GREY) for _, s in entries])
        for k, b in enumerate(bin_col):
            b.move_to([0, asm_col[k].get_center()[1], 0], aligned_edge=LEFT)
        asm_col.shift(LEFT * (asm_col.lines.get_left()[0] + 6.0))
        bin_col.shift(RIGHT * (-1.3 - bin_col.get_left()[0]))
        head_l = mono("example.S", 26, GREY_A).next_to(asm_col, UP, buff=0.35).align_to(asm_col.lines, LEFT)
        head_r = mono("example.bin", 26, GREY_A).move_to([0, head_l.get_center()[1], 0]).align_to(bin_col, LEFT)
        rule = Line([-6.1, 0, 0], [6.1, 0, 0], stroke_color=GREY_D, stroke_width=1.5)
        rule.set_y((head_l.get_bottom()[1] + asm_col.get_top()[1]) / 2)
        table = VGroup(head_l, head_r, rule, asm_col, bin_col)
        table.shift(UP * (0.55 - table.get_center()[1]))
        self.say("笔记里还有一份整文件的对照。标签 main 没有对应的机器码；伪指令 mv a0, a5 其实是 addi a0, a5, 0。"
                 "最后一行 call printf 只编成了一条 jal：目标够近时，工具链会把 auipc + jalr 缩成一条 jal。",
                 FadeIn(table, shift=UP * 0.1))
        self.cue(tr("标签 main 没有对应的机器码"), Circumscribe(VGroup(asm_col[0], bin_col[0]), color=C_LABEL))
        mv = CodeListing(["addi a0, a5, 0"], font_size=26)
        mv.shift(asm_col[4].get_left() - mv[0].get_left())
        self.cue(tr("伪指令 mv a0, a5"), Transform(asm_col[4], mv[0]), Circumscribe(bin_col[4], color=C_NUM))
        call_a = CodeListing(["jal  ra, printf"], font_size=26)
        call_a.shift(asm_col[5].get_left() - call_a[0].get_left())
        self.cue(tr("最后一行 call printf"), Circumscribe(VGroup(asm_col[5], bin_col[5]), color=YELLOW_D))
        self.play(Transform(asm_col[5], call_a[0]), Circumscribe(bin_col[5][-12:], color=C_NUM))
        self.hold(0.5)
