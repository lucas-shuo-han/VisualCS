import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403


# machine code for the worked examples, assembled field by field
ADD = "0000000" + "01010" + "10011" + "000" + "10010" + "0110011"       # add  x18, x19, x10
ADDI = "111111001110" + "00001" + "000" + "01111" + "0010011"          # addi x15, x1, -50
LW = "000000001000" + "00010" + "010" + "01110" + "0000011"            # lw   x14, 8(x2)
SW = "0000000" + "01110" + "00010" + "010" + "01000" + "0100011"       # sw   x14, 8(x2)
assert bits_to_hex(ADD) == "0x00A98933"
assert bits_to_hex(ADDI) == "0xFCE08793"
assert bits_to_hex(LW) == "0x00812703"
assert bits_to_hex(SW) == "0x00E12423"


class Ep09FormatsRIS(FormatScene):
    def construct(self):
        self.title_card()
        self.stored_program()
        self.r_format()
        self.i_format()
        self.s_format()
        self.end_card(
            [
                "存储程序：指令就是存放在内存里的 32 位数",
                "R 型：funct7 | rs2 | rs1 | funct3 | rd | opcode",
                "I 型：12 位立即数取代 funct7 和 rs2",
                "S 型：立即数拆成两段，rs1、rs2 位置不变",
                "字段位置固定，硬件译码更简单",
            ],
        )

    # ------------------------------------------------------------------ stored program
    def stored_program(self):
        prog = [("add  x18, x19, x10", ADD), ("addi x15, x1, -50", ADDI),
                ("lw   x14, 8(x2)", LW), ("sw   x14, 8(x2)", SW)]
        cells = VGroup()
        texts = VGroup()
        addrs = VGroup()
        for k, (asm, bits) in enumerate(prog):
            r = Rectangle(width=5.2, height=0.7, stroke_color=GREY_B, fill_color=GREY_E, fill_opacity=0.3)
            r.move_to(DOWN * k * 0.7)
            t = CodeListing([asm], font_size=28).move_to(r)
            a = mono(f"0x{0x1000 + 4 * k:X}", 26, GREY_B).next_to(r, LEFT, buff=0.3)
            cells.add(r)
            texts.add(t)
            addrs.add(a)
        mem = VGroup(cells, texts, addrs).move_to(DOWN * 0.1 + LEFT * 0.5)
        mem_l = zh("内存", 28, GREY_A).next_to(cells, UP, buff=0.3)
        self.say("前几集我们一直在写汇编。可硬件真正执行的，是一个个 32 位的二进制数。"
                 "指令本身也是数据，和普通数据一样存在内存里：这就是“存储程序”（stored program）的思想。",
                 FadeIn(mem, shift=UP * 0.2), FadeIn(mem_l))
        hexes = VGroup(*[
            mono(bits_to_hex(b), 30, YELLOW_D).move_to(cells[k])
            for k, (_, b) in enumerate(prog)
        ])
        self.cue(tr("指令本身也是数据"),
                 LaggedStart(*[ReplacementTransform(t, h) for t, h in zip(texts, hexes)], lag_ratio=0.25,
                             run_time=2.2))
        pc = RegBox("PC", "0x1000", color=YELLOW_D, width=1.7, font_size=28).next_to(cells, RIGHT, buff=1.0)
        pc.shift(UP * 0.9)
        arrow = Arrow(pc.get_left(), cells[0].get_right(), buff=0.1, color=YELLOW_D)
        self.say("PC 里存的，是当前指令在内存中的地址。"
                 "那么，一条汇编指令究竟是怎样变成 32 个比特的？", FadeIn(pc), GrowArrow(arrow))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ R
    def r_format(self):
        head = self.heading("R 型：寄存器之间的运算")
        bf = BitField(fmt_fields("R")).move_to(UP * 0.6)
        self.say("32 位被切成几段，每段叫一个字段（field）。add、sub 这类操作数全是寄存器的指令，用 R 型格式。"
                 "rd、rs1、rs2 各占 5 位：2 的 5 次方是 32，刚好够给 32 个寄存器编号。"
                 "opcode 占最低 7 位，说明这是哪一类指令；funct3 和 funct7 再进一步区分具体的运算。",
                 Write(head), FadeIn(bf.frames, lag_ratio=0.2), FadeIn(bf.labels), FadeIn(bf.ranges))
        regs = VGroup(bf.frames[1], bf.frames[2], bf.frames[4])
        self.cue(tr("rd、rs1、rs2 各占 5 位"), *[Indicate(f, scale_factor=1.08) for f in regs])
        self.cue(tr("opcode 占最低 7 位"),
                 Indicate(bf.frames[5], scale_factor=1.08),
                 Indicate(bf.frames[3], scale_factor=1.08),
                 Indicate(bf.frames[0], scale_factor=1.08))
        self.hold()

        asm = CodeListing(["add x18, x19, x10"], font_size=40).move_to(UP * 2.4)
        self.say("来编码 add x18, x19, x10。"
                 "rd = 18，写成 5 位二进制是 10010；rs1 = 19 是 10011；rs2 = 10 是 01010。", FadeIn(asm, shift=DOWN * 0.2))
        self.cue(tr("rd = 18"))
        n1 = self.encode(bf, [(4, "10010", "x18"), (2, "10011", "x19"), (1, "01010", "x10")])
        self.say("add 的 funct3 和 funct7 都是 0，R 型算术指令的 opcode 是 0110011。"
                 "每 4 位合成一个十六进制数字：整条指令就是 0x00A98933。")
        n2 = self.encode(bf, [(3, "000", "add"), (0, "0000000", "add"), (5, "0110011", "R 型")])
        self.cue(tr("每 4 位合成一个十六进制数字"))
        hx = self.hex_of(bf, -1.9)
        self.hold()

        sub = CodeListing(["sub x18, x19, x10"], font_size=40).move_to(asm)
        self.say("换成 sub 呢？只有 funct7 变了：0100000。硬件看到第 30 位的这个 1，就让加法器改做减法。",
                 Transform(asm, sub))
        self.cue(tr("只有 funct7 变了"),
                 bf.fill_field(0, "0100000"),
                 Transform(n2[1], mono("sub", 20, FIELD_COLORS["funct7"]).move_to(n2[1])))
        self.cue(tr("硬件看到第 30 位的这个 1"), Circumscribe(bf.field_digits[0][1], color=RED_B))
        hx2 = mono("0x40A98933", 40, YELLOW_D).move_to(hx)
        self.play(Transform(hx, hx2))
        self.hold()
        self.play(FadeOut(VGroup(asm, n1, n2, hx)), FadeOut(bf.digits))

        rows = [("add", "000", "0000000"), ("sub", "000", "0100000"), ("sll", "001", "0000000"),
                ("xor", "100", "0000000"), ("srl", "101", "0000000"), ("sra", "101", "0100000"),
                ("or", "110", "0000000"), ("and", "111", "0000000")]
        tbl = VGroup(*[
            VGroup(mono(m, 24, C_MNEM), mono(f3, 24, FIELD_COLORS["funct3"]),
                   mono(f7, 24, FIELD_COLORS["funct7"])).arrange(RIGHT, buff=0.5)
            for m, f3, f7 in rows
        ])
        tbl.arrange_in_grid(4, 2, buff=(1.2, 0.22), flow_order="dr")
        tbl.next_to(bf, DOWN, buff=0.5)
        self.say("所有 R 型运算共用一个 opcode，靠 funct3 和 funct7 的组合来区分。",
                 LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in tbl], lag_ratio=0.1))
        self.hold()
        self.play(FadeOut(tbl), FadeOut(head))
        self.bf = bf

    # ------------------------------------------------------------------ I
    def i_format(self):
        bf = self.bf
        head = self.heading("I 型：带立即数的指令")
        self.say("addi 只有两个寄存器，外加一个常数。常数放在哪儿？"
                 "I 型把 R 型里 funct7 和 rs2 的位置合并成一个 12 位的立即数，其余字段纹丝不动。", Write(head))
        ibf = BitField(fmt_fields("I")).move_to(bf)
        self.cue(tr("I 型把 R 型里"),
                 ReplacementTransform(VGroup(bf.frames[0], bf.frames[1]), ibf.frames[0]),
                 ReplacementTransform(VGroup(bf.labels[0], bf.labels[1]), ibf.labels[0]),
                 ReplacementTransform(VGroup(bf.ranges[0], bf.ranges[1]), ibf.ranges[0]),
                 *[ReplacementTransform(bf.frames[k], ibf.frames[k - 1]) for k in range(2, 6)],
                 *[ReplacementTransform(bf.labels[k], ibf.labels[k - 1]) for k in range(2, 6)],
                 *[ReplacementTransform(bf.ranges[k], ibf.ranges[k - 1]) for k in range(2, 6)],
                 run_time=1.6)
        rng = zh("12 位补码：−2048 ~ 2047", 28, YELLOW_D).next_to(ibf, DOWN, buff=0.5)
        self.say("第 2 集的问题有了答案：立即数只分到这 12 位，而 12 位补码的范围正是 −2048 到 2047。",
                 Indicate(ibf.frames[0], color=YELLOW_D, scale_factor=1.05), FadeIn(rng))
        self.hold()
        self.play(FadeOut(rng))

        asm = CodeListing(["addi x15, x1, -50"], font_size=40).move_to(UP * 2.4)
        self.say("编码 addi x15, x1, -50：-50 的 12 位补码是 1111 1100 1110。"
                 "执行时，硬件把这 12 位符号扩展成 32 位，再和 rs1 相加。编码结果是 0xFCE08793。", FadeIn(asm, shift=DOWN * 0.2))
        notes = self.encode(ibf, [(0, "111111001110", "-50"), (1, "00001", "x1"), (2, "000", "addi"),
                                  (3, "01111", "x15"), (4, "0010011", "I 型算术")])
        self.cue(tr("编码结果是"))
        hx = self.hex_of(ibf, -1.9)
        self.hold()
        self.play(FadeOut(VGroup(asm, notes, hx)), FadeOut(ibf.digits))
        ibf.digits.set_opacity(0)

        asm = CodeListing(["lw x14, 8(x2)"], font_size=40).move_to(UP * 2.4)
        self.say("load 指令也是 I 型。lw x14, 8(x2) 里，偏移量 8 就是立即数，基址寄存器 x2 放在 rs1。",
                 FadeIn(asm, shift=DOWN * 0.2))
        notes = self.encode(ibf, [(0, "000000001000", "8"), (1, "00010", "x2"), (2, "010", "lw"),
                                  (3, "01110", "x14"), (4, "0000011", "load")], rt=0.7)
        widths = mono("funct3:  lb 000   lh 001   lw 010   lbu 100   lhu 101", 24,
                      FIELD_COLORS["funct3"]).next_to(ibf, DOWN, buff=1.0)
        self.say("所有 load 共用一个 opcode，由 funct3 区分宽度和有无符号：lb、lh、lw、lbu、lhu。"
                 "移位 slli、srli、srai 也用 I 型，但移位量最多 31，只用到立即数的低 5 位。",
                 FadeIn(widths, shift=UP * 0.1))
        shift_note = zh("slli / srli / srai 也是 I 型：移位量只用立即数的低 5 位", 25 if EN else 24, GREY_A)
        shift_note.next_to(widths, DOWN, buff=0.35)
        self.cue(tr("移位 slli"), FadeIn(shift_note))
        self.hold()
        self.play(FadeOut(VGroup(asm, notes, widths, shift_note, head)), FadeOut(ibf.digits))
        ibf.digits.set_opacity(0)
        self.ibf = ibf

    # ------------------------------------------------------------------ S
    def s_format(self):
        ibf = self.ibf
        head = self.heading("S 型：store")
        self.say("store 有两个源寄存器——数据和基址——没有目标寄存器，但还需要一个 12 位偏移。"
                 "S 型的做法：把立即数拆成两段。高 7 位放在 funct7 的老位置，低 5 位放在原来 rd 的位置。",
                 Write(head))
        sbf = BitField(fmt_fields("S")).move_to(ibf)
        self.cue(tr("S 型的做法"),
                 ReplacementTransform(ibf.frames[0], VGroup(sbf.frames[0], sbf.frames[1])),
                 ReplacementTransform(ibf.labels[0], VGroup(sbf.labels[0], sbf.labels[1])),
                 ReplacementTransform(ibf.ranges[0], VGroup(sbf.ranges[0], sbf.ranges[1])),
                 ReplacementTransform(ibf.frames[1], sbf.frames[2]),
                 ReplacementTransform(ibf.labels[1], sbf.labels[2]),
                 ReplacementTransform(ibf.ranges[1], sbf.ranges[2]),
                 ReplacementTransform(ibf.frames[2], sbf.frames[3]),
                 ReplacementTransform(ibf.labels[2], sbf.labels[3]),
                 ReplacementTransform(ibf.ranges[2], sbf.ranges[3]),
                 ReplacementTransform(ibf.frames[3], sbf.frames[4]),
                 ReplacementTransform(ibf.labels[3], sbf.labels[4]),
                 ReplacementTransform(ibf.ranges[3], sbf.ranges[4]),
                 ReplacementTransform(ibf.frames[4], sbf.frames[5]),
                 ReplacementTransform(ibf.labels[4], sbf.labels[5]),
                 ReplacementTransform(ibf.ranges[4], sbf.ranges[5]),
                 run_time=1.6)
        self.hold()

        asm = CodeListing(["sw x14, 8(x2)"], font_size=40).move_to(UP * 2.4)
        self.say("编码 sw x14, 8(x2)。偏移 8 的 12 位二进制是 0000000 01000：高 7 位全 0，低 5 位是 01000。",
                 FadeIn(asm, shift=DOWN * 0.2))
        notes = self.encode(sbf, [(0, "0000000", "8 高位"), (4, "01000", "8 低位")])
        self.say("要写入的数据 x14 放在 rs2，基址 x2 放在 rs1；funct3 = 010 表示整字，opcode 是 0100011。"
                 "拼起来，这条 sw 就是 0x00E12423。")
        notes2 = self.encode(sbf, [(1, "01110", "x14"), (2, "00010", "x2"), (3, "010", "sw"),
                                   (5, "0100011", "store")], rt=0.7)
        self.cue(tr("拼起来"))
        hx = self.hex_of(sbf, -1.9)
        self.hold()
        self.play(FadeOut(VGroup(asm, notes, notes2, hx, sbf.digits, head)))

        # alignment of R / I / S
        self.play(FadeOut(VGroup(sbf.frames, sbf.labels, sbf.ranges)))
        fields = [BitField(fmt_fields(k), box_h=0.5, show_ranges=False, label_size=18) for k in "RIS"]
        stack = VGroup(*fields).arrange(DOWN, buff=0.55).move_to(UP * 0.35)
        tags = VGroup(*[mono(k, 30, WHITE).next_to(f.frames, LEFT, buff=0.35) for k, f in zip("RIS", fields)])
        self.say("把三种格式叠起来看：为什么 S 型要拆得这么别扭？"
                 "答案：不管哪种格式，只要用到 rs1、rs2，它们就待在同一个位置。",
                 LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in fields], lag_ratio=0.3), FadeIn(tags))
        box_w = fields[0].box_w
        left = fields[0].frames.get_left()[0]

        def band(hi, lo, color):
            xl = left + (31 - hi) * box_w
            xr = left + (32 - lo) * box_w
            top = stack.get_top()[1] + 0.1
            bot = stack.get_bottom()[1] - 0.1
            return Rectangle(width=xr - xl, height=top - bot, stroke_color=color, stroke_width=3,
                             fill_color=color, fill_opacity=0.08).move_to([(xl + xr) / 2, (top + bot) / 2, 0])

        b_rs1 = band(19, 15, FIELD_COLORS["rs1"])
        b_rs2 = band(24, 20, FIELD_COLORS["rs2"])
        self.cue(tr("答案"), Create(b_rs1), Create(b_rs2))
        b_f3 = band(14, 12, FIELD_COLORS["funct3"])
        b_op = band(6, 0, FIELD_COLORS["opcode"])
        self.say("funct3 和 opcode 也一样。硬件不必先判断指令类型，就能按固定位置直接去读寄存器。"
                 "读寄存器和译码可以同时进行，电路更简单，也更快。这是 RISC-V 设计中很漂亮的一笔。",
                 Create(b_f3), Create(b_op))
        self.hold(0.5)
