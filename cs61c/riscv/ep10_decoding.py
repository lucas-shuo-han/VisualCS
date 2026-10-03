import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403


# ---------------------------------------------------------------- encodings
# Every word shown in this episode is assembled here and checked against a
# small independent decoder, so the pictures cannot drift from the real bits.

OP_R, OP_IMM, OP_LOAD, OP_STORE, OP_JALR, OP_SYSTEM = (
    0b0110011, 0b0010011, 0b0000011, 0b0100011, 0b1100111, 0b1110011)


def enc_r(f7, rs2, rs1, f3, rd, op=OP_R):
    return (f7 << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op


def enc_i(imm, rs1, f3, rd, op):
    return ((imm & 0xFFF) << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op


def enc_s(imm, rs2, rs1, f3, op=OP_STORE):
    return (((imm >> 5) & 0x7F) << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | ((imm & 0x1F) << 7) | op


def b32(w):
    return format(w, "032b")


def sext(v, bits):
    return v - (1 << bits) if (v >> (bits - 1)) & 1 else v


R_OPS = {(0, 0b000): "add", (0x20, 0b000): "sub", (0, 0b001): "sll", (0, 0b010): "slt",
         (0, 0b011): "sltu", (0, 0b100): "xor", (0, 0b101): "srl", (0x20, 0b101): "sra",
         (0, 0b110): "or", (0, 0b111): "and"}
I_OPS = {0b000: "addi", 0b010: "slti", 0b011: "sltiu", 0b100: "xori", 0b110: "ori", 0b111: "andi"}
LOADS = {0b000: "lb", 0b001: "lh", 0b010: "lw", 0b100: "lbu", 0b101: "lhu"}
STORES = {0b000: "sb", 0b001: "sh", 0b010: "sw"}


def disasm(w):
    """Independent RV32I decoder for the formats used here (ABI register names)."""
    op, rd, f3 = w & 0x7F, (w >> 7) & 31, (w >> 12) & 7
    rs1, rs2, f7 = (w >> 15) & 31, (w >> 20) & 31, w >> 25
    n = ABI_NAMES
    if op == OP_R:
        return f"{R_OPS[(f7, f3)]} {n[rd]}, {n[rs1]}, {n[rs2]}"
    if op == OP_IMM:
        if f3 == 0b001:
            return f"slli {n[rd]}, {n[rs1]}, {rs2}"
        if f3 == 0b101:
            return f"{'srai' if f7 == 0x20 else 'srli'} {n[rd]}, {n[rs1]}, {rs2}"
        return f"{I_OPS[f3]} {n[rd]}, {n[rs1]}, {sext(w >> 20, 12)}"
    if op == OP_LOAD:
        return f"{LOADS[f3]} {n[rd]}, {sext(w >> 20, 12)}({n[rs1]})"
    if op == OP_STORE:
        return f"{STORES[f3]} {n[rs2]}, {sext((f7 << 5) | rd, 12)}({n[rs1]})"
    if op == OP_JALR:
        return f"jalr {n[rd]}, {n[rs1]}, {sext(w >> 20, 12)}"
    if op == OP_SYSTEM:
        return {0: "ecall", 1: "ebreak"}[w >> 20]
    raise ValueError(hex(w))


X0, RA, SP, GP, T0, T1, A0, S11 = 0, 1, 2, 3, 5, 6, 10, 27

XOR = enc_r(0, S11, T1, 0b100, T0)                      # the word we disassemble
ADD = enc_r(0, S11, T1, 0b000, T0)
SUB = enc_r(0x20, S11, T1, 0b000, T0)
SRL = enc_r(0, S11, T1, 0b101, T0)
SRA = enc_r(0x20, S11, T1, 0b101, T0)
SRAI = enc_i(0b0100000_00101, T1, 0b101, T0, OP_IMM)     # srai t0, t1, 5
SRLI = enc_i(5, T1, 0b101, T0, OP_IMM)                   # srli t0, t1, 5
RET = enc_i(0, RA, 0b000, X0, OP_JALR)                   # jalr x0, ra, 0
ECALL = enc_i(0, 0, 0, 0, OP_SYSTEM)
EBREAK = enc_i(1, 0, 0, 0, OP_SYSTEM)
SW36 = enc_s(36, 14, 2, 0b010)                           # sw x14, 36(x2)
Q1 = enc_r(0, GP, SP, 0b000, RA)                         # add x1, x2, x3
Q2 = enc_i(-4, SP, 0b010, A0, OP_LOAD)                   # lw a0, -4(sp)

assert XOR == 0x01B342B3 and b32(XOR) == "0000" "0001" "1011" "0011" "0100" "0010" "1011" "0011"
assert disasm(XOR) == "xor t0, t1, s11"
assert (ADD, SUB, SRL, SRA) == (0x01B302B3, 0x41B302B3, 0x01B352B3, 0x41B352B3)
assert [disasm(w) for w in (ADD, SUB, SRL, SRA)] == [
    "add t0, t1, s11", "sub t0, t1, s11", "srl t0, t1, s11", "sra t0, t1, s11"]
assert (SRAI, SRLI) == (0x40535293, 0x00535293)
assert disasm(SRAI) == "srai t0, t1, 5" and disasm(SRLI) == "srli t0, t1, 5"
assert RET == 0x00008067 and disasm(RET) == "jalr zero, ra, 0"
assert (ECALL, EBREAK) == (0x00000073, 0x00100073)
assert (disasm(ECALL), disasm(EBREAK)) == ("ecall", "ebreak")
assert format(36, "012b") == "0000001" "00100"
assert SW36 == 0x02E12223 and disasm(SW36) == "sw a4, 36(sp)"
assert Q1 == 0x003100B3 and disasm(Q1) == "add ra, sp, gp"
assert b32(Q1) == "00000000001100010000000010110011"       # the add x1, x2, x3 of the notes
assert Q2 == 0xFFC12503 and disasm(Q2) == "lw a0, -4(sp)"

# one line of C, three ISAs (bytes as they sit in the file, little-endian)
RV_ADD = enc_r(0, 11, 10, 0b000, 10)                       # RISC-V  add a0, a0, a1
ARM_ADD = (0b0001011 << 24) | (1 << 16) | (0 << 5) | 0    # AArch64 add w0, w0, w1 (sf=0, shift=0)
X86_ADD = bytes([0x01, 0b11_011_000])                    # x86     add eax, ebx: 01 /r, ModRM reg=ebx rm=eax
assert RV_ADD == 0x00B50533 and disasm(RV_ADD) == "add a0, a0, a1"
assert ARM_ADD == 0x0B010000
RV_BYTES = list(RV_ADD.to_bytes(4, "little"))
ARM_BYTES = list(ARM_ADD.to_bytes(4, "little"))
assert RV_BYTES == [0x33, 0x05, 0xB5, 0x00] and ARM_BYTES == [0x00, 0x00, 0x01, 0x0B]
assert list(X86_ADD) == [0x01, 0xD8]

# the 8-bit right-shift picture
SHIFT_SRC = "10110100"
assert format(int(SHIFT_SRC, 2) >> 2, "08b") == "00101101"
assert format((sext(int(SHIFT_SRC, 2), 8) >> 2) & 0xFF, "08b") == "11101101"


# ---------------------------------------------------------------- helpers

R_TABLE = [("add", "0000000", "000"), ("sub", "0100000", "000"), ("and", "0000000", "111"),
           ("or", "0000000", "110"), ("xor", "0000000", "100"), ("sll", "0000000", "001"),
           ("srl", "0000000", "101"), ("sra", "0100000", "101"), ("slt", "0000000", "010"),
           ("sltu", "0000000", "011")]
for _m, _f7, _f3 in R_TABLE:
    assert R_OPS[(int(_f7, 2), int(_f3, 2))] == _m


def nibble_row(bits, box=0.36, gap=0.14, font_size=22):
    """A bit_row with a small gap after every 4 bits (one hex digit each)."""
    row = bit_row(bits, GREY_B, box=box, font_size=font_size)
    for k, cell in enumerate(row):
        cell.shift(RIGHT * gap * (k // 4))
    return row.center()


def r_table(size=22, row_gap=0.38, group_dx=5.0):
    """The ten R-type instructions: mnemonic | funct7 | funct3, in two columns."""
    tbl = VGroup()
    tbl.rows = []
    for g in range(2):
        x0 = g * group_dx
        for r in range(5):
            m, f7, f3 = R_TABLE[5 * g + r]
            y = -r * row_gap
            row = VGroup(
                mono(m, size, C_MNEM).move_to([x0, y, 0], aligned_edge=LEFT),
                mono(f7, size, FIELD_COLORS["funct7"]).move_to([x0 + 2.0, y, 0]),
                mono(f3, size, FIELD_COLORS["funct3"]).move_to([x0 + 3.4, y, 0]),
            )
            tbl.rows.append(row)
            tbl.add(row)
        tbl.add(mono("funct7", size - 4, GREY).move_to([x0 + 2.0, row_gap, 0]),
                mono("funct3", size - 4, GREY).move_to([x0 + 3.4, row_gap, 0]))
    return tbl.center()


def byte_cells(bs, color, w=0.7, h=0.5):
    g = VGroup()
    for k, b in enumerate(bs):
        r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2, fill_color=color,
                      fill_opacity=0.12).move_to(RIGHT * k * w)
        g.add(VGroup(r, mono(f"{b:02X}", 24, WHITE).move_to(r)))
    return g


def x_mark(size=0.3, color=RED_C):
    return VGroup(Line(UL * size, DR * size), Line(UR * size, DL * size)).set_stroke(color, 7)


def check_mark(size=0.32, color=GREEN_C):
    return VMobject(stroke_color=color, stroke_width=8).set_points_as_corners(
        [[-size, 0, 0], [-size * 0.25, -size * 0.7, 0], [size, size * 0.8, 0]])


def under(bf, i, s, color=None, size=22, buff=0.12):
    """A note under field i of a BitField (below its bit-range label)."""
    t = mono(s, size, color or bf.fields[i][2]).next_to(bf.ranges[i], DOWN, buff=buff)
    if t.width > bf.frames[i].width + 0.3:
        t.scale_to_fit_width(bf.frames[i].width + 0.3)
    return t


def asm_code(s, size):
    return CodeListing([s], font_size=size)


def arr(a, b, color=GREY_B, buff=0.1, width=3):
    return Arrow(a, b, buff=buff, color=color, stroke_width=width, max_tip_length_to_length_ratio=0.2,
                 max_stroke_width_to_length_ratio=10)


class Ep10Decoding(FormatScene):
    def construct(self):
        self.title_card()
        self.isa_binaries()
        self.disassemble()
        self.bit30()
        self.i_family()
        self.jalr_ret()
        self.s_example()
        self.quiz()
        self.end_card(
            [
                "反汇编：先看 opcode 定格式，再切字段、定操作、译寄存器",
                "第 30 位是开关：add/sub、srl/sra、srli/srai",
                "I 型有 4 个 opcode：立即数运算、load、jalr、ecall/ebreak",
                "funct3 成对复用：addi 与 add，lw 与 sw（没有 subi）",
                "ret = jalr x0, ra, 0 = 0x00008067",
            ],
        )

    # ------------------------------------------------------------------ binaries are ISA-bound
    def isa_binaries(self):
        src = CodeListing(["a = a + b;"], lang="c", font_size=34)
        box = SurroundingRectangle(src.lines, color=GREY_B, buff=0.25, corner_radius=0.1)
        top = VGroup(box, src).move_to(UP * 2.45)
        specs = [("RISC-V", "本课程", "add a0, a0, a1", RV_BYTES, YELLOW_D),
                 ("ARM", "多数手机", "add w0, w0, w1", ARM_BYTES, GREY_A),
                 ("x86", "多数电脑", "add eax, ebx", list(X86_ADD), GREY_A)]
        cols = VGroup()
        for k, (name, who, asm, bs, color) in enumerate(specs):
            tag = VGroup(mono(name, 30, color), zh(who, 22, GREY_A)).arrange(DOWN, buff=0.1)
            code = mono(asm, 26, C_REG, t2c={"add": C_MNEM})
            cells = byte_cells(bs, color)
            size = zh("4 字节" if len(bs) == 4 else "2 字节", 22, GREY_A)
            col = VGroup(tag, code, cells, size).arrange(DOWN, buff=0.35)
            col.move_to([(k - 1) * 4.4, -0.3, 0])
            cols.add(col)
        arrows = VGroup(*[arr(top.get_bottom(), c[0].get_top(), buff=0.12) for c in cols])
        self.say("第 2 集说过，x86、ARM、RISC-V 是三种不同的指令集。同一行 C 代码，交给三种编译器，"
                 "得到的机器码完全不同。手机里多是 ARM 芯片，电脑里多是 x86。",
                 FadeIn(top, shift=DOWN * 0.2),
                 LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25),
                 LaggedStart(*[FadeIn(c[0], shift=DOWN * 0.1) for c in cols], lag_ratio=0.25),
                 run_time=1.6)
        self.cue(tr("得到的机器码完全不同"),
                 LaggedStart(*[FadeIn(VGroup(c[1], c[2]), shift=DOWN * 0.1) for c in cols], lag_ratio=0.3),
                 run_time=1.6)
        self.say("连长度都不一样：x86 的指令有长有短，这一条只有 2 个字节。"
                 "RISC-V 的指令则一律 32 位，和数据字一样宽：取指令和读数据能共用同一套内存硬件。",
                 FadeIn(VGroup(*[c[3] for c in cols])),
                 Indicate(cols[2][2], color=GREY_A, scale_factor=1.15))
        word = SurroundingRectangle(cols[0][2], color=YELLOW_D, buff=0.1)
        self.cue(tr("RISC-V 的指令则一律 32 位"), Create(word))
        self.hold()
        self.clear_stage()

        exe = file_icon("a.out", YELLOW_D, w=1.2, h=1.45)
        exe = VGroup(exe, mono("RISC-V", 22, YELLOW_D).next_to(exe, DOWN, buff=0.12)).move_to([-3.4, 1.2, 0])
        old = file_icon("8088", GREY_B, w=1.2, h=1.45)
        old = VGroup(old, zh("1981 年", 22, GREY_A).next_to(old, DOWN, buff=0.12)).move_to([-3.4, -1.15, 0])
        pc = box_label("x86 电脑", GREY_B, w=3.0, h=1.1, font_size=30).move_to([2.9, 0.05, 0])
        a1 = arr(exe[0].get_right(), pc.get_left() + UP * 0.25, buff=0.2)
        a2 = arr(old[0].get_right(), pc.get_left() + DOWN * 0.25, buff=0.2)
        no = x_mark().move_to(a1.get_center() + UP * 0.05)
        yes = check_mark().move_to(a2.get_center() + UP * 0.05)
        self.say("所以程序的二进制文件和指令集是绑定的：RISC-V 的可执行文件，在 Intel 的 x86 电脑上根本跑不起来。"
                 "不过，同一个指令集常常向后兼容：今天的 x86 处理器，仍能运行 1981 年为 Intel 8088 写的程序。",
                 FadeIn(exe, shift=RIGHT * 0.2), FadeIn(pc))
        self.cue(tr("RISC-V 的可执行文件"), GrowArrow(a1))
        self.cue(tr("根本跑不起来"), Create(no))
        self.cue(tr("不过，同一个指令集常常向后兼容"), FadeIn(old, shift=RIGHT * 0.2))
        self.cue(tr("今天的 x86 处理器"), GrowArrow(a2))
        self.cue(tr("仍能运行"), Create(yes))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ disassembly
    def disassemble(self):
        head = self.heading("反汇编：从机器码到汇编")
        self.say("上一集把汇编翻译成机器码；这一集反过来：拿到机器码，怎么读回汇编？这叫反汇编（disassembly）。"
                 "拿这个字练手：0x01B342B3。", Write(head))
        word = mono(hex32(XOR), 48, YELLOW_D).move_to(UP * 2.2)
        self.cue(tr("拿这个字练手"), FadeIn(word, shift=DOWN * 0.2))

        row = nibble_row(b32(XOR)).move_to(UP * 0.85)
        xs = [VGroup(*row[4 * k:4 * k + 4]).get_center()[0] for k in range(8)]
        prefix, digits = VGroup(*word[:2]), VGroup(*word[2:])
        self.remove(word)
        self.add(prefix, digits)
        self.say("第一步：换成二进制。每个十六进制数字，正好展开成 4 位。"
                 "接着找 opcode：不管哪种格式，它永远占最低的 7 位。"
                 "每种格式都有自己专属的一组 opcode。查表：0110011，是 R 型。",
                 FadeOut(prefix), *[d.animate.move_to([x, 2.2, 0]) for d, x in zip(digits, xs)])
        self.cue(tr("每个十六进制数字，正好展开成"),
                 LaggedStart(*[
            AnimationGroup(FadeIn(VGroup(*[c[0] for c in row[4 * k:4 * k + 4]])),
                           *[TransformFromCopy(digits[k], row[4 * k + j][1]) for j in range(4)])
            for k in range(8)], lag_ratio=0.18),
                 run_time=2.6)

        op_cells = VGroup(*row[25:])
        op_box = SurroundingRectangle(op_cells, color=FIELD_COLORS["opcode"], buff=0.07)
        op_lab = mono("opcode", 22, FIELD_COLORS["opcode"]).next_to(op_box, DOWN, buff=0.12)
        self.cue(tr("接着找 opcode"), Create(op_box), FadeIn(op_lab))

        specs = [("0110011", "R 型", "寄存器之间运算"), ("0010011", "I 型", "立即数运算"),
                 ("0000011", "I 型", "load"), ("0100011", "S 型", "store")]
        table = VGroup()
        for k, (op, fmt, what) in enumerate(specs):
            y = -k * 0.5
            table.add(VGroup(mono(op, 26, FIELD_COLORS["opcode"]).move_to([0, y, 0], aligned_edge=LEFT),
                             zh(fmt, 26).move_to([1.8, y, 0], aligned_edge=LEFT),
                             zh(what, 22, GREY_A).move_to([3.2, y, 0], aligned_edge=LEFT)))
        table.move_to(DOWN * 1.35)
        probe = VGroup(*[c[1] for c in row[25:]]).copy()
        hl = SurroundingRectangle(table[0], color=FIELD_COLORS["opcode"], buff=0.1)
        self.cue(tr("每种格式都有自己专属的一组 opcode"),
                 LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in table], lag_ratio=0.15))
        self.cue(tr("查表"),
                 probe.animate.set_color(FIELD_COLORS["opcode"]).arrange(RIGHT, buff=0.04)
                  .match_height(table[0][0]).move_to(table[0][0]),
                 run_time=1.0)
        self.cue(tr("是 R 型"), FadeOut(probe), Create(hl))

        bf = BitField(fmt_fields("R")).move_to(DOWN * 0.85)
        self.say("第二步：知道了格式，才知道其余 25 位怎么切。按 R 型切开：funct7、rs2、rs1、funct3、rd。",
                 FadeOut(VGroup(table, hl, op_lab)),
                 FadeIn(bf.frames), FadeIn(bf.labels), FadeIn(bf.ranges))
        self.fly_bits(row, bf, [(0, range(0, 7)), (1, range(7, 12)), (2, range(12, 17)),
                                (3, range(17, 20)), (4, range(20, 25)), (5, range(25, 32))], run_time=2.2)
        corner = mono(hex32(XOR), 30, YELLOW_D).to_corner(UR, buff=0.5)
        self.play(FadeOut(row), FadeOut(op_box), FadeOut(digits), FadeIn(corner),
                  bf.animate.move_to(UP * 1.35), run_time=1.2)

        tbl = r_table().move_to(DOWN * 1.1)
        xor_row = tbl.rows[4]
        self.say("第三步：funct3 = 100，funct7 = 0000000。查 R 型的表：这是 xor。"
                 "注意：助记符（mnemonic）xor 不存放在任何一个字段里，而是由 opcode、funct3、funct7 共同决定。",
                 Indicate(bf.frames[3], scale_factor=1.08), Indicate(bf.frames[0], scale_factor=1.05),
                 FadeIn(tbl))
        hl = SurroundingRectangle(xor_row, color=YELLOW_D, buff=0.08)
        n_op = under(bf, 3, "xor", C_MNEM)
        self.cue(tr("查 R 型的表"), Create(hl))
        self.cue(tr("这是 xor"), TransformFromCopy(xor_row[0], n_op))
        self.cue(tr("注意：助记符"), *[Indicate(bf.frames[i], scale_factor=1.06) for i in (0, 3, 5)])
        self.hold()

        n_rd, n_rs1, n_rs2 = under(bf, 4, "x5"), under(bf, 2, "x6"), under(bf, 1, "x27")
        self.say("第四步：寄存器字段是 5 位无符号数：rd = 00101 = 5，rs1 = 00110 = 6，rs2 = 11011 = 27。"
                 "再换成寄存器名：x5 是 t0，x6 是 t1，x27 是 s11。"
                 "拼起来：xor t0, t1, s11。",
                 FadeOut(VGroup(tbl, hl)),
                 LaggedStart(*[FadeIn(n, shift=DOWN * 0.1) for n in (n_rd, n_rs1, n_rs2)], lag_ratio=0.3))
        abi = [mono(s, 28, abi_color(s)).next_to(n, DOWN, buff=0.14)
               for s, n in (("t0", n_rd), ("t1", n_rs1), ("s11", n_rs2))]
        self.cue(tr("再换成寄存器名"), LaggedStart(*[FadeIn(a, shift=DOWN * 0.1) for a in abi], lag_ratio=0.3))

        asm = asm_code("xor t0, t1, s11", 44).move_to(DOWN * 1.3)
        toks = [asm.glyphs(0, s) for s in ("xor", "t0", "t1", "s11")]
        commas = VGroup(asm.glyphs(0, ",", 0), asm.glyphs(0, ",", 1))
        self.cue(tr("拼起来"),
                 *[TransformFromCopy(s, t) for s, t in zip([n_op, *abi], toks)],
                 FadeIn(commas),
                 run_time=1.6)
        self.remove(*toks, commas)
        self.add(asm)
        roles = VGroup(*[mono(r, 20, FIELD_COLORS[r]).next_to(t, DOWN, buff=0.15)
                         for r, t in zip(("rd", "rs1", "rs2"), toks[1:])])
        links = VGroup(*[arr(a.get_bottom(), t.get_top(), color=FIELD_COLORS[r], buff=0.12, width=2.5)
                         for a, t, r in zip(abi, toks[1:], ("rd", "rs1", "rs2"))])
        self.say("小心顺序：汇编里写 rd, rs1, rs2，而字段从左到右是 rs2, rs1, rd，正好相反。",
                 LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=0.3), FadeIn(roles))
        self.hold()
        self.clear_stage()

        steps = ["转成二进制，看 opcode 定格式", "按格式切分字段", "由 funct3、funct7 定操作", "寄存器编号换成名字"]
        rows = VGroup(*[
            VGroup(mono(str(k + 1), 32, YELLOW_D), zh(s, 30)).arrange(RIGHT, buff=0.35)
            for k, s in enumerate(steps)
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(LEFT * 1.6 + UP * 0.3)
        b1 = Brace(VGroup(rows[0], rows[1]), RIGHT, color=GREEN_C)
        b2 = Brace(VGroup(rows[2], rows[3]), RIGHT, color=GOLD_C)
        t1 = zh("所有格式通用", 26, GREEN_C).next_to(b1, RIGHT, buff=0.2)
        t2 = zh("因格式而异", 26, GOLD_C).next_to(b2, RIGHT, buff=0.2)
        recap = VGroup(rows, b1, b2, t1, t2)
        if recap.width > 12.6:
            recap.scale_to_fit_width(12.6)
        recap.set_x(0)
        self.say("反汇编就这四步。前两步对任何格式都一样，后两步因格式而异。",
                 Write(self.heading("反汇编的四个步骤")),
                 LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.25), run_time=2.0)
        self.cue(tr("前两步对任何格式都一样"), GrowFromCenter(b1), FadeIn(t1), GrowFromCenter(b2), FadeIn(t2))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ bit 30
    def bit30(self):
        head = self.heading("第 30 位：一个开关")
        tbl = r_table(size=26, row_gap=0.5, group_dx=5.4).move_to(UP * 0.55)
        self.say("回头看完整的 R 型表：10 条指令共用一个 opcode，funct3 却只有 8 种。"
                 "funct3 相同的有两对：add 和 sub 都是 000，srl 和 sra 都是 101。"
                 "区分它们靠 funct7。funct7 也只有两种取值，而且只差一位：第 30 位。",
                 Write(head), FadeIn(tbl, lag_ratio=0.02))
        pairs = VGroup(SurroundingRectangle(VGroup(tbl.rows[0], tbl.rows[1]), color=YELLOW_D, buff=0.1),
                       SurroundingRectangle(VGroup(tbl.rows[6], tbl.rows[7]), color=YELLOW_D, buff=0.1))
        self.cue(tr("funct3 相同的有两对"), Create(pairs))
        ones = [tbl.rows[1][1][1], tbl.rows[7][1][1]]
        self.cue(tr("区分它们靠 funct7"),
                 *[Indicate(o, color=WHITE, scale_factor=1.8) for o in ones],
                 *[Circumscribe(o, color=RED_B, buff=0.06) for o in ones])
        tally = zh("opcode 7 位 + funct3 3 位 + funct7 7 位 = 17 位", 26, GREY_A).next_to(tbl, DOWN, buff=0.5)
        self.say("光为区分运算就动用了 17 位，明显有富余。但让字段位置对齐，比省下几位更重要。",
                 FadeIn(tally, shift=UP * 0.1))
        self.hold()

        bf = BitField(fmt_fields("R"), bits=b32(ADD)).move_to(UP * 1.6)
        tag = mono("R", 30, WHITE).next_to(bf.frames, LEFT, buff=0.3)
        asm = asm_code("add t0, t1, s11", 34).move_to([3.4, -0.25, 0])
        hx = mono(hex32(ADD), 34, YELLOW_D).move_to([3.4, -1.15, 0])
        b30 = bf.field_digits[0][1]
        mark = SurroundingRectangle(b30, color=RED_B, buff=0.05)
        m_lab = zh("第 30 位", 22, RED_B).move_to([b30.get_center()[0], bf.labels[0].get_top()[1] + 0.28, 0])
        self.say("以 add t0, t1, s11 为例：把第 30 位从 0 翻成 1，它就变成了 sub t0, t1, s11。"
                 "add 和 sub 共用一个加法器。第 30 位就是个开关（flag）：为 1 时先把 rs2 取负（按位取反再加 1），再相加。",
                 FadeOut(VGroup(tbl, pairs, tally)), FadeIn(VGroup(bf, tag)), FadeIn(asm), FadeIn(hx))
        self.cue(tr("把第 30 位从 0 翻成 1"), Create(mark), FadeIn(m_lab))
        self.cue(tr("它就变成了"),
                 bf.fill_field(0, "0100000"),
                 Transform(asm, asm_code("sub t0, t1, s11", 34).move_to(asm)),
                 Transform(hx, mono(hex32(SUB), 34, YELLOW_D).move_to(hx)))

        # add / sub share one adder; bit 30 switches the negation of rs2 on
        bx = b30.get_center()[0]
        neg_box = RoundedRectangle(corner_radius=0.08, width=0.9, height=0.5, stroke_width=3)
        neg_txt = mono("-x", 26)
        neg = VGroup(neg_box, neg_txt).move_to([-4.7, -0.2, 0])
        neg_txt.move_to(neg_box)
        ctrl = DashedLine([bx, bf.frames[0].get_bottom()[1], 0], neg.get_top(), stroke_width=3)
        s_in = mono("s11", 26, C_S).move_to([-6.25, -0.2, 0])
        t_in = mono("t1", 26, C_T).move_to([-6.25, -1.3, 0])
        adder = VGroup(Circle(radius=0.32, stroke_color=BLUE_C, stroke_width=3, fill_color=BLUE_C,
                              fill_opacity=0.12), mono("+", 30, BLUE_C)).move_to([-3.2, -0.75, 0])
        out = mono("t0", 26, C_T).move_to([-1.9, -0.75, 0])
        wires = VGroup(arr(s_in.get_right(), neg.get_left(), buff=0.12),
                       arr(neg.get_right(), adder.get_left() + UP * 0.12, buff=0.08),
                       arr(t_in.get_right(), adder.get_left() + DOWN * 0.12, buff=0.12),
                       arr(adder.get_right(), out.get_left(), buff=0.1))

        def neg_state(on):
            c = RED_C if on else GREY_D
            return [neg_box.animate.set_stroke(c).set_fill(c, 0.2 if on else 0.05),
                    neg_txt.animate.set_color(WHITE if on else GREY),
                    ctrl.animate.set_stroke(RED_B if on else GREY_D)]

        neg_box.set_stroke(RED_C).set_fill(RED_C, 0.2)
        ctrl.set_stroke(RED_B)
        self.cue(tr("add 和 sub 共用一个加法器"), FadeIn(VGroup(s_in, t_in, neg, adder, out, wires)), Create(ctrl))
        self.play(bf.fill_field(0, "0000000"), *neg_state(False),
                  Transform(asm, asm_code("add t0, t1, s11", 34).move_to(asm)),
                  Transform(hx, mono(hex32(ADD), 34, YELLOW_D).move_to(hx)))
        self.wait(0.4)
        self.cue(tr("为 1 时先把 rs2 取负"),
                 bf.fill_field(0, "0100000"),
                 *neg_state(True),
                 Transform(asm, asm_code("sub t0, t1, s11", 34).move_to(asm)),
                 Transform(hx, mono(hex32(SUB), 34, YELLOW_D).move_to(hx)))
        self.hold()
        diagram = VGroup(s_in, t_in, neg, adder, out, wires, ctrl)

        # srl / sra
        src = bit_row(SHIFT_SRC, GREY_B, box=0.42, font_size=24).move_to([-4.0, -0.2, 0])
        res = bit_row("00101101", GREY_B, box=0.42, font_size=24).move_to([-4.0, -1.35, 0])
        demo_l = zh("以 8 位为例，右移 2 位：", 22, GREY_A).next_to(src, UP, buff=0.22, aligned_edge=LEFT)
        res_l = mono("srl", 24, C_MNEM).next_to(res, LEFT, buff=0.3)
        for k in (0, 1):
            res[k][1].set_color(GREEN_B)
        self.say("funct3 换成 101 就是右移。第 30 位为 0 是 srl：逻辑右移，空出的高位补 0。"
                 "第 30 位为 1 就成了 sra：算术右移，高位补的是符号位。这回，这个开关管的是符号扩展。",
                 FadeOut(diagram), bf.fill_field(3, "101"), bf.fill_field(0, "0000000"),
                 Transform(asm, asm_code("srl t0, t1, s11", 34).move_to(asm)),
                 Transform(hx, mono(hex32(SRL), 34, YELLOW_D).move_to(hx)))
        self.cue(tr("逻辑右移"), FadeIn(src), FadeIn(demo_l))
        self.cue(tr("空出的高位补 0"),
                 FadeIn(VGroup(*[c[0] for c in res])),
                 FadeIn(res_l),
                 *[TransformFromCopy(src[k][1], res[k + 2][1]) for k in range(6)],
                 FadeIn(VGroup(res[0][1], res[1][1]), shift=RIGHT * 0.3),
                 run_time=1.4)
        ones = VGroup(*[mono("1", 24, RED_B).move_to(res[k][0]) for k in (0, 1)])
        self.cue(tr("第 30 位为 1 就成了 sra"),
                 bf.fill_field(0, "0100000"),
                 Transform(asm, asm_code("sra t0, t1, s11", 34).move_to(asm)),
                 Transform(hx, mono(hex32(SRA), 34, YELLOW_D).move_to(hx)),
                 Transform(res_l, mono("sra", 24, C_MNEM).move_to(res_l)))
        self.cue(tr("高位补的是符号位"), Indicate(src[0], color=RED_B, scale_factor=1.3))
        self.cue(tr("这回，这个开关管的是符号扩展"), Transform(VGroup(res[0][1], res[1][1]), ones))
        self.hold()

        # shift-immediates: the same bit, inside the I-type immediate
        lab0 = mono("imm[11:5]", 20, RED_C).move_to(bf.labels[0])
        lab1 = mono("imm[4:0]", 20, YELLOW_D).move_to(bf.labels[1])
        self.say("移位立即数用的是 I 型的一个变体，CS61C 叫它 I* 型：移位量最多 31，只占立即数的低 5 位。",
                 FadeOut(VGroup(src, res, demo_l, res_l)),
                 Transform(tag, mono("I*", 30, WHITE).move_to(tag)),
                 Transform(bf.labels[1], lab1),
                 bf.frames[1].animate.set_stroke(YELLOW_D).set_fill(YELLOW_D, 0.14))
        self.cue(tr("移位量最多 31"),
                 bf.fill_field(1, "00101"),
                 bf.fill_field(5, "0010011"),
                 Transform(asm, asm_code("srai t0, t1, 5", 34).move_to(asm)),
                 Transform(hx, mono(hex32(SRAI), 34, YELLOW_D).move_to(hx)))
        self.say("立即数的高 7 位不当数值用，而是像 funct7 一样当开关：srai 的这 7 位是 0100000，开关依旧是第 30 位。"
                 "关掉第 30 位就是 srli。左移只有逻辑移位一种，所以 slli 的这一位永远是 0。",
                 Transform(bf.labels[0], lab0), Indicate(mark, color=RED_B))
        self.cue(tr("关掉第 30 位就是 srli"),
                 bf.fill_field(0, "0000000"),
                 Transform(asm, asm_code("srli t0, t1, 5", 34).move_to(asm)),
                 Transform(hx, mono(hex32(SRLI), 34, YELLOW_D).move_to(hx)))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ the I-type family
    def i_family(self):
        head = self.heading("I 型全家")
        spec = [("000", ["add", "sub"], ["addi", "subi"]), ("111", ["and"], ["andi"]),
                ("110", ["or"], ["ori"]), ("100", ["xor"], ["xori"]), ("001", ["sll"], ["slli"]),
                ("101", ["srl", "sra"], ["srli", "srai"]), ("010", ["slt"], ["slti"]),
                ("011", ["sltu"], ["sltiu"])]
        rows = VGroup()
        for k, (f3, rs, is_) in enumerate(spec):
            y = 1.75 - k * 0.46
            r = VGroup(*[mono(m, 26, C_MNEM) for m in rs]).arrange(RIGHT, buff=0.35)
            i = VGroup(*[mono(m, 26, C_MNEM) for m in is_]).arrange(RIGHT, buff=0.35)
            rows.add(VGroup(mono(f3, 26, FIELD_COLORS["funct3"]).move_to([-5.3, y, 0]),
                            r.move_to([-4.0, y, 0], aligned_edge=LEFT),
                            i.move_to([-1.5, y, 0], aligned_edge=LEFT)))
        header = VGroup(mono("funct3", 22, GREY).move_to([-5.3, 2.3, 0]),
                        zh("R 型", 24, GREY_A).move_to([-4.0, 2.3, 0], aligned_edge=LEFT),
                        zh("I 型", 24, GREY_A).move_to([-1.5, 2.3, 0], aligned_edge=LEFT))
        subi = rows[0][2][1]
        subi.set_color(GREY_D)
        self.say("I 型不只有 addi。把立即数运算和 R 型并排：funct3 一一对应，addi 对 add，xori 对 xor，slti 对 slt，"
                 "唯独没有 subi：要减一个常数，addi 一个负数就行。",
                 Write(head), FadeIn(header),
                 LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.12), run_time=2.2)
        strike = Line(subi.get_left() + LEFT * 0.08, subi.get_right() + RIGHT * 0.08, color=RED_C, stroke_width=4)
        alt = CodeListing(["addi t0, t0, -5", "# t0 = t0 - 5"], font_size=28, line_gap=0.5).move_to([3.9, 1.1, 0])
        self.cue(tr("唯独没有 subi"), Create(strike), FadeIn(alt, shift=LEFT * 0.2))
        box101 = SurroundingRectangle(rows[5], color=RED_B, buff=0.08)
        self.say("3 位的 funct3 只有 8 种编码，这里已经全部用光，srli 和 srai 还得靠第 30 位来区分。",
                 LaggedStart(*[Indicate(r[0], scale_factor=1.3) for r in rows], lag_ratio=0.08),
                 Create(box101), run_time=1.8)
        self.hold()

        cats = [("0010011", "立即数运算", ["addi", "slti", "xori", "slli", "srai", "..."]),
                ("0000011", "load", ["lb", "lh", "lw", "lbu", "lhu"]),
                ("1100111", "间接跳转", ["jalr"]),
                ("1110011", "系统", ["ecall", "ebreak"])]
        table = VGroup()
        cat_labels = [zh(cat, 26) for _, cat, _ in cats]
        mx = max(-1.7, -4.2 + max(c.width for c in cat_labels) + 0.6)
        for k, ((op, _, ms), cat_l) in enumerate(zip(cats, cat_labels)):
            y = 1.9 - k * 0.8
            members = VGroup(*[mono(m, 24, C_MNEM) for m in ms]).arrange(RIGHT, buff=0.3)
            table.add(VGroup(mono(op, 26, FIELD_COLORS["opcode"]).move_to([-6.1, y, 0], aligned_edge=LEFT),
                             cat_l.move_to([-4.2, y, 0], aligned_edge=LEFT),
                             members.move_to([mx, y, 0], aligned_edge=LEFT)))
        self.say("5 种 load 也要靠 funct3 区分，只好另开一个 opcode。算下来，I 型一共有 4 个 opcode。",
                 FadeOut(VGroup(rows, header, strike, alt, box101)),
                 LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in table], lag_ratio=0.25), run_time=2.0)
        self.hold()
        sysrow = table[3]
        hl = SurroundingRectangle(sysrow, color=YELLOW_D, buff=0.1)
        ecall_m, ebreak_m = sysrow[2][0], sysrow[2][1]
        os_box = box_label("操作系统", BLUE_C, h=0.6, font_size=24).move_to([ecall_m.get_x() - 1.45, -1.65, 0])
        dbg_box = box_label("调试器", GREEN_C, h=0.6, font_size=24).move_to([ebreak_m.get_x() + 1.1, -1.65, 0])
        self.say("ecall（environment call，环境调用）向操作系统请求服务，比如输出文字、结束程序。"
                 "ebreak 则把控制权交给调试器：调试器里的断点，就是靠它实现的。",
                 table[:3].animate.set_opacity(0.35), Create(hl))
        self.cue(tr("向操作系统请求服务"),
                 GrowArrow(arr(ecall_m.get_bottom(), os_box.get_top(), color=BLUE_C, buff=0.1)),
                 FadeIn(os_box))
        self.cue(tr("把控制权交给调试器"),
                 GrowArrow(arr(ebreak_m.get_bottom(), dbg_box.get_top(), color=GREEN_C, buff=0.1)),
                 FadeIn(dbg_box))
        self.hold()
        self.clear_stage(head)

        bf = BitField(fmt_fields("I"), bits=b32(ECALL)).move_to(UP * 1.0)
        name = mono("ecall", 36, C_MNEM).move_to([-2.6, -0.85, 0])
        hx = mono(hex32(ECALL), 36, YELLOW_D).move_to([2.6, -0.85, 0])
        b20 = SurroundingRectangle(bf.field_digits[0][11], color=RED_B, buff=0.05)
        self.say("这两条都没有操作数：ecall 除了 opcode 全是 0；ebreak 只是在立即数的最低位多了一个 1。",
                 FadeIn(bf), FadeIn(name), FadeIn(hx))
        self.cue(tr("ecall 除了 opcode 全是 0"), Create(b20))
        self.cue(tr("ebreak 只是在立即数的最低位"),
                 bf.fill_field(0, "000000000001"),
                 Transform(name, mono("ebreak", 36, C_MNEM).move_to(name)),
                 Transform(hx, mono(hex32(EBREAK), 36, YELLOW_D).move_to(hx)))
        self.hold()
        self.clear_stage(head)

        ls = [("000", "lb", "sb", "字节"), ("001", "lh", "sh", "半字"), ("010", "lw", "sw", "字"),
              ("100", "lbu", "—", "字节，无符号"), ("101", "lhu", "—", "半字，无符号")]
        lrows = VGroup()
        for k, (f3, ld, st, w) in enumerate(ls):
            y = 1.7 - k * 0.52
            lrows.add(VGroup(mono(f3, 26, FIELD_COLORS["funct3"]).move_to([-4.6, y, 0]),
                             mono(ld, 26, C_MNEM).move_to([-2.8, y, 0]),
                             mono(st, 26, C_MNEM if st != "—" else GREY).move_to([-1.1, y, 0]),
                             zh(w, 24, GREY_A).move_to([0.4, y, 0], aligned_edge=LEFT)))
        lhead = VGroup(mono("funct3", 22, GREY).move_to([-4.6, 2.3, 0]),
                       mono("load", 22, GREY).move_to([-2.8, 2.3, 0]),
                       mono("store", 22, GREY).move_to([-1.1, 2.3, 0]))
        pair = SurroundingRectangle(VGroup(*[VGroup(r[1], r[2]) for r in lrows[:3]]), color=YELLOW_D, buff=0.12)
        self.say("load 和 store 的 funct3 也是配套的：lb 和 sb 是 000，lh 和 sh 是 001，lw 和 sw 是 010。"
                 "lbu、lhu 没有对应的 store：store 只写入指定的字节，不涉及扩展。同理，RV32 也没有 lwu。",
                 FadeIn(lhead), LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in lrows], lag_ratio=0.15),
                 run_time=1.8)
        self.cue(tr("lb 和 sb 是 000"), Create(pair))
        no_lwu = zh("RV32 也没有 lwu：一个字正好填满 32 位的寄存器", 24, GREY_A).move_to(DOWN * 1.4)
        self.cue(tr("lbu、lhu 没有对应的 store"),
                 *[Indicate(r[2], color=GREY_A) for r in lrows[3:]],
                 FadeIn(no_lwu, shift=UP * 0.1))
        self.hold()

        code = CodeListing([
            "addi t0, t1, 8     # t0 = t1 + 8",
            "lw   t0, 8(t1)     # 地址 = t1 + 8",
            "jalr ra, t1, 8     # 跳到 t1 + 8",
        ], font_size=30, line_gap=0.7).move_to(UP * 1.0)
        boxes = VGroup(*[SurroundingRectangle(code.glyphs(i, "t1 + 8"), color=YELLOW_D, buff=0.07)
                         for i in range(3)])
        shared = zh("都要算 rs1 + imm：复用同一个加法器", 28, YELLOW_D).move_to(DOWN * 1.1)
        self.say("load 和 jalr 为什么也用 I 型？它们都要先算 rs1 + 立即数：一个算地址，一个算跳转目标，正好复用同一个加法器。",
                 FadeOut(VGroup(lrows, lhead, pair, no_lwu)),
                 LaggedStart(*[FadeIn(line, shift=RIGHT * 0.2) for line in code.lines], lag_ratio=0.25))
        self.cue(tr("它们都要先算"),
                 LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.25),
                 FadeIn(shared, shift=UP * 0.1))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ jalr, ret
    def jalr_ret(self):
        head = self.heading("jalr 与函数返回")
        gen = mono("jalr rd, rs1, imm", 34, C_TEXT, t2c={"jalr": C_MNEM})
        alt = mono("= jalr rd, imm(rs1)", 26, GREY)
        g = VGroup(gen, alt).arrange(RIGHT, buff=0.5).move_to(UP * 2.25)
        eff = mono("rd = PC + 4;   PC = rs1 + imm", 28, GREY_A).next_to(g, DOWN, buff=0.35)
        self.say("jalr rd, rs1, imm（也写作 jalr rd, imm(rs1)）：先把 PC + 4 存进 rd，再跳到 rs1 + imm。",
                 Write(head), FadeIn(g, shift=DOWN * 0.2), FadeIn(eff))
        self.hold()

        eq = VGroup(asm_code("ret", 34), mono("=", 34, GREY_A), asm_code("jr ra", 34),
                    mono("=", 34, GREY_A), asm_code("jalr x0, ra, 0", 34)).arrange(RIGHT, buff=0.45)
        eq.move_to(UP * 2.25)
        self.say("第 7 集的 ret 和 jr ra 都是伪指令，没有自己的 opcode：汇编器把它们都翻译成 jalr x0, ra, 0。"
                 "rd 取 x0，是因为返回时不需要再留下返回地址：写进 x0 的值会被直接丢掉。",
                 FadeOut(VGroup(g, eff), shift=UP * 0.2), FadeIn(eq, shift=UP * 0.2))
        self.cue(tr("rd 取 x0"), Circumscribe(eq[4].glyphs(0, "x0"), color=YELLOW_D))
        self.hold()

        bf = BitField(fmt_fields("I")).move_to(UP * 0.4)
        self.say("编码：立即数 0，rs1 = ra = x1，rd = x0。jalr 只有一条，funct3 其实用不上，按格式填 000。"
                 "opcode 是 1100111。合起来就是 0x00008067：在反汇编结果里见到它，就知道函数要返回了。",
                 FadeIn(bf.frames), FadeIn(bf.labels), FadeIn(bf.ranges))
        notes = self.encode(bf, [(0, "000000000000", "0"), (1, "00001", "ra = x1"), (3, "00000", "x0"),
                                 (2, "000", "000")], rt=0.7)
        self.cue(tr("opcode 是 1100111"))
        notes.add(*self.encode(bf, [(4, "1100111", "jalr")], rt=0.7))
        self.hex_of(bf, -1.65)
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ S-type example
    def s_example(self):
        head = self.heading("S 型：拆开的立即数")
        asm = asm_code("sw x14, 36(x2)", 40).move_to(UP * 2.4)
        sbf = BitField(fmt_fields("S")).move_to(DOWN * 0.55)
        self.say("再来一个 S 型的例子：sw x14, 36(x2)。"
                 "36 的 12 位二进制是 0000 0010 0100。高 7 位 0000001 放进 imm[11:5]，低 5 位 00100 放进 imm[4:0]。",
                 Write(head), FadeIn(asm, shift=DOWN * 0.2), FadeIn(sbf.frames), FadeIn(sbf.labels),
                 FadeIn(sbf.ranges))
        bits = format(36, "012b")
        row = bit_row(bits, YELLOW_D, box=0.42, font_size=24).move_to(UP * 1.3)
        idx = VGroup(*[mono(str(11 - k), 16, GREY).next_to(row[k], UP, buff=0.08) for k in range(12)])
        lab = mono("36 =", 28, YELLOW_D).next_to(row, LEFT, buff=0.3)
        self.cue(tr("36 的 12 位二进制"), FadeIn(row), FadeIn(idx), FadeIn(lab))
        self.fly_bits(row, sbf, [(0, range(0, 7)), (4, range(7, 12))])
        self.say("为什么要拆？只用 funct7 的 7 位，只能表示 128 个值；store 没有 rd，正好借用 rd 的 5 位，凑满 12 位。"
                 "其余照旧：rs2 = x14，rs1 = x2，funct3 = 010 表示 sw，opcode 是 0100011。",
                 Indicate(sbf.frames[0], color=YELLOW_D, scale_factor=1.05),
                 Indicate(sbf.frames[4], color=YELLOW_D, scale_factor=1.1))
        self.cue(tr("其余照旧"))
        notes = self.encode(sbf, [(1, "01110", "x14"), (2, "00010", "x2"), (3, "010", "sw"),
                                  (5, "0100011", "store")], rt=0.7)
        self.say("结果是 0x02E12223。反汇编时就反过来：把两段拼回去，0000001 00100 就是 36。")
        self.hex_of(sbf, -2.05)
        self.cue(tr("反汇编时就反过来"), FadeOut(VGroup(*[c[1] for c in row])))
        back = VGroup(*[c[1].copy() for c in row])
        self.play(*[TransformFromCopy(d, b) for d, b in
                    zip([*sbf.field_digits[0], *sbf.field_digits[4]], back)], run_time=1.4)
        self.cue(tr("0000001 00100 就是 36"), Indicate(lab, color=YELLOW_D))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ quiz
    def quiz(self):
        head = self.heading("小测验")
        q1 = VGroup(mono("1.", 36, GREY_A), mono(hex32(Q1), 48, YELLOW_D)).arrange(RIGHT, buff=0.4)
        q2 = VGroup(mono("2.", 36, GREY_A), mono(hex32(Q2), 48, YELLOW_D)).arrange(RIGHT, buff=0.4)
        qs = VGroup(q1, q2).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to([-1.0, 0.5, 0])
        ring = Circle(radius=0.45, stroke_color=GREY_D, stroke_width=6).move_to([4.2, 0.5, 0])
        sweep = Arc(radius=0.45, start_angle=PI / 2, angle=-TAU, stroke_color=YELLOW_D, stroke_width=6)
        sweep.move_arc_center_to(ring.get_center())
        self.say("最后留两道题：把这两个字翻译成汇编。先暂停视频，自己试试。",
                 Write(head), LaggedStart(*[FadeIn(q, shift=RIGHT * 0.2) for q in qs], lag_ratio=0.3),
                 FadeIn(ring))
        self.play(Create(sweep), run_time=5, rate_func=linear)
        self.hold()

        self.play(FadeOut(VGroup(q2, ring, sweep)), q1.animate.scale(0.75).move_to([1.2, 2.4, 0]))
        bf = BitField(fmt_fields("R"), bits=b32(Q1)).move_to(UP * 0.9)
        bf.digits.set_opacity(0)
        self.say("第 1 题：opcode 是 0110011，R 型；funct3 和 funct7 全是 0，所以是 add。"
                 "rd = 1，rs1 = 2，rs2 = 3：答案是 add x1, x2, x3，也就是 add ra, sp, gp。",
                 FadeIn(bf.frames), FadeIn(bf.labels), FadeIn(bf.ranges))
        self.cue(tr("opcode 是 0110011"),
                 LaggedStart(*[d.animate.set_opacity(1) for d in bf.digits], lag_ratio=0.03),
                 run_time=1.4)
        n1 = VGroup(under(bf, 5, "R"), under(bf, 3, "add", C_MNEM), under(bf, 0, "0000000"))
        self.cue(tr("所以是 add"), LaggedStart(*[FadeIn(n, shift=DOWN * 0.1) for n in n1], lag_ratio=0.3))
        n2 = VGroup(under(bf, 4, "x1"), under(bf, 2, "x2"), under(bf, 1, "x3"))
        ans = VGroup(asm_code("add x1, x2, x3", 40), mono("= add ra, sp, gp", 30, GREY_A)).arrange(RIGHT, buff=0.5)
        ans.move_to(DOWN * 1.4)
        self.cue(tr("rd = 1，rs1 = 2，rs2 = 3"),
                 LaggedStart(*[FadeIn(n, shift=DOWN * 0.1) for n in n2], lag_ratio=0.3))
        self.play(FadeIn(ans, shift=UP * 0.2))
        self.hold()
        self.play(FadeOut(VGroup(q1, bf, n1, n2, ans)))

        q2.scale(0.75).move_to([1.2, 2.4, 0])
        ibf = BitField(fmt_fields("I"), bits=b32(Q2)).move_to(UP * 0.9)
        ibf.digits.set_opacity(0)
        self.say("第 2 题：opcode 0000011 是 load，funct3 = 010 是 lw；rd = 10 是 a0，rs1 = 2 是 sp。"
                 "立即数 1111 1111 1100 的最高位是 1，按补码是 −4。答案：lw a0, -4(sp)。",
                 FadeIn(q2), FadeIn(ibf.frames), FadeIn(ibf.labels), FadeIn(ibf.ranges))
        self.play(LaggedStart(*[d.animate.set_opacity(1) for d in ibf.digits], lag_ratio=0.03), run_time=1.4)
        m1 = VGroup(under(ibf, 4, "load"), under(ibf, 2, "lw", C_MNEM), under(ibf, 3, "a0"), under(ibf, 1, "sp"))
        self.play(LaggedStart(*[FadeIn(n, shift=DOWN * 0.1) for n in m1], lag_ratio=0.3))
        imm = under(ibf, 0, "1111 1111 1100 = -4")
        ans = asm_code("lw a0, -4(sp)", 44).move_to(DOWN * 1.4)
        self.cue(tr("立即数 1111 1111 1100"), FadeIn(imm, shift=DOWN * 0.1))
        self.play(FadeIn(ans, shift=UP * 0.2))
        self.hold(0.5)
