import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F403

# beq x19, x10, End   with End 16 bytes ahead
BEQ = "0" + "000000" + "01010" + "10011" + "000" + "1000" + "0" + "1100011"
assert bits_to_hex(BEQ) == "0x00A98863"
assert (0xDEADB000 + 0xFFFFFEEF) & 0xFFFFFFFF == 0xDEADAEEF
assert (0xDEADC000 - 273) & 0xFFFFFFFF == 0xDEADBEEF


class Ep11FormatsBUJ(FormatScene):
    def construct(self):
        self.title_card()
        self.pc_relative()
        self.b_format()
        self.u_format()
        self.j_format()
        self.overview()
        self.end_card(
            [
                "分支用 PC 相对寻址：目标 = PC + 偏移",
                "B 型偏移以 2 字节为单位，范围约 ±4 KiB",
                "打乱的位序让各格式尽量共用同一组连线",
                "U 型：lui / auipc 提供高 20 位",
                "J 型：jal，范围约 ±1 MiB；jalr 是 I 型",
            ],
        )

    # ------------------------------------------------------------------ PC-relative
    def pc_relative(self):
        head = self.heading("分支的目标地址怎么编码？")
        code = CodeListing([
            "Loop: beq  x19, x10, End",
            "      add  x18, x18, x10",
            "      addi x19, x19, -1",
            "      j    Loop",
            "End:  ...",
        ], font_size=32, line_gap=0.62).move_to(UP * 0.5 + RIGHT * 0.6)
        addrs = VGroup(*[mono(f"0x{0x1000 + 4 * i:X}", 26, GREY).next_to(code.left_of(i, 0.45), LEFT, buff=0)
                         for i in range(5)])
        self.say("条件分支要比较两个寄存器 rs1、rs2，还要一个跳转目标；它不写寄存器，所以没有 rd。",
                 Write(head), FadeIn(code, shift=UP * 0.2), FadeIn(addrs))
        self.say("可目标地址本身就有 32 位，根本塞不进一条 32 位的指令。怎么办？",
                 Circumscribe(code.glyphs(0, "End"), color=C_LABEL))
        arrow = CurvedArrow(code.right_of(0, 0.3), code.right_of(4, 0.3), angle=-TAU / 4, color=YELLOW_D)
        off = mono("+16", 32, YELLOW_D).next_to(arrow, RIGHT, buff=0.15)
        self.say("观察：分支通常跳得很近——if 和循环体一般只有几条到几十条指令。",
                 Create(arrow), FadeIn(off))
        eq = zh("目标地址 = PC + 偏移量", 34, YELLOW_D).next_to(code, DOWN, buff=0.6)
        self.say("所以只编码“相对当前 PC 的偏移量”。这叫 PC 相对寻址（PC-relative addressing）。", Write(eq))
        self.hold()
        note = zh("偏移总是 2 的倍数 → 最低位恒为 0，不必存储", 28, GREY_A).move_to(eq)
        self.say("RISC-V 为 16 位的压缩指令留了余地，指令地址总是 2 的倍数，所以偏移的最低位恒为 0，不用存。",
                 FadeOut(eq, shift=UP * 0.2), FadeIn(note, shift=UP * 0.2))
        self.say("于是 12 个比特能表示 13 位的偏移：范围约 ±4 KiB，也就是前后各约 1024 条指令。")
        self.say("还有个好处：整段代码搬到内存别处，分支的偏移完全不用改。这叫位置无关代码（position-independent code）。",
                 VGroup(code, addrs, arrow, off).animate(rate_func=there_and_back, run_time=2).shift(RIGHT * 1.2))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ B
    def b_format(self):
        head = self.heading("B 型：条件分支")
        sbf = BitField(fmt_fields("S")).move_to(DOWN * 0.1)
        self.say("B 型的布局和 S 型几乎一样：rs1、rs2、funct3、opcode 都在老位置，立即数也分成两段。",
                 Write(head), FadeIn(sbf.frames), FadeIn(sbf.labels), FadeIn(sbf.ranges))
        bbf = BitField(fmt_fields("B")).move_to(sbf)
        self.play(
            ReplacementTransform(sbf.frames[0], VGroup(bbf.frames[0], bbf.frames[1])),
            ReplacementTransform(sbf.labels[0], VGroup(bbf.labels[0], bbf.labels[1])),
            ReplacementTransform(sbf.ranges[0], VGroup(bbf.ranges[0], bbf.ranges[1])),
            *[ReplacementTransform(getattr(sbf, a)[k], getattr(bbf, a)[k + 1])
              for a in ("frames", "labels", "ranges") for k in (1, 2, 3)],
            ReplacementTransform(sbf.frames[4], VGroup(bbf.frames[5], bbf.frames[6])),
            ReplacementTransform(sbf.labels[4], VGroup(bbf.labels[5], bbf.labels[6])),
            ReplacementTransform(sbf.ranges[4], VGroup(bbf.ranges[5], bbf.ranges[6])),
            *[ReplacementTransform(getattr(sbf, a)[5], getattr(bbf, a)[7]) for a in ("frames", "labels", "ranges")],
            run_time=1.6,
        )
        imm_legend = zh("黄色都是立即数；上方标注它存的是偏移量的哪几位", 25 if EN else 24, YELLOW_D)
        imm_legend.next_to(bbf, DOWN, buff=0.5)
        self.say("但立即数的位序被“打乱”了：第 12 位放在指令最高位，第 11 位挪到了右边那段的末尾。",
                 FadeIn(imm_legend),
                 Indicate(bbf.frames[0], color=YELLOW_D, scale_factor=1.3),
                 Indicate(bbf.frames[6], color=YELLOW_D, scale_factor=1.3))
        self.say("这是为了复用 S 型的连线：第 10:5 位和第 4:1 位与 S 型完全同位，符号位也永远在第 31 位。",
                 Indicate(bbf.frames[1], color=YELLOW_D), Indicate(bbf.frames[5], color=YELLOW_D))
        self.hold()
        self.play(FadeOut(imm_legend), bbf.animate.move_to(DOWN * 0.35))

        asm = CodeListing(["beq x19, x10, End     # End = PC + 16"], font_size=34).move_to(UP * 2.65)
        self.say("编码 beq x19, x10, End。End 在 4 条指令之后，偏移是 16 字节。",
                 FadeIn(asm, shift=DOWN * 0.2))
        row = bit_row("0000000010000", YELLOW_D, box=0.42, font_size=24).move_to(UP * 1.45)
        idx = VGroup(*[mono(str(12 - k), 16, GREY).next_to(row[k], UP, buff=0.08) for k in range(13)])
        lab = mono("16 =", 28, YELLOW_D).next_to(row, LEFT, buff=0.3)
        self.say("16 的 13 位二进制是 0 0000 0001 0000。最低位不存，其余各位按规定的位置“对号入座”。",
                 FadeIn(row), FadeIn(idx), FadeIn(lab))
        cross = Cross(row[12], stroke_color=RED_C, stroke_width=4)
        self.play(Create(cross))
        self.fly_bits(row, bbf, [(0, [0]), (1, [2, 3, 4, 5, 6, 7]), (5, [8, 9, 10, 11]), (6, [1])])
        self.say("寄存器照旧：rs2 = x10，rs1 = x19；beq 的 funct3 是 000，分支的 opcode 是 1100011。")
        notes = self.encode(bbf, [(2, "01010", "x10"), (3, "10011", "x19"), (4, "000", "beq"),
                                  (7, "1100011", "branch")], rt=0.7)
        self.say("最终的机器码是 0x00A98863。")
        hx = self.hex_of(bbf, -2.0)
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ U
    def u_format(self):
        head = self.heading("U 型：长立即数")
        self.say("12 位立即数只装得下小常数。想把 0xDEADBEEF 这样的 32 位常数放进寄存器，怎么办？",
                 Write(head))
        ubf = BitField(fmt_fields("U")).move_to(UP * 1.6)
        self.say("U 型只有 rd 和一个 20 位的立即数。lui（load upper immediate）就用这个格式。",
                 FadeIn(ubf.frames), FadeIn(ubf.labels), FadeIn(ubf.ranges))
        reg = BitField([("来自立即数的高 20 位", 20, YELLOW_D), ("低 12 位清零", 12, GREY_B)],
                       show_ranges=False, label_size=25 if EN else 20).move_to(DOWN * 0.6)
        t0 = mono("t0", 28, C_T).next_to(reg.frames, LEFT, buff=0.3)
        code = CodeListing(["lui t0, 0xDEADB"], font_size=32).next_to(reg, UP, buff=0.35)
        self.say("lui t0, 0xDEADB：把 20 位立即数放进 t0 的高 20 位，低 12 位全部清零。",
                 FadeIn(code), FadeIn(reg.frames), FadeIn(reg.labels), FadeIn(t0))
        self.play(reg.fill_field(0, format(0xDEADB, "020b")), reg.fill_field(1, "0" * 12))
        val = mono("t0 = 0xDEADB000", 32, YELLOW_D).next_to(reg, DOWN, buff=0.4)
        self.play(Write(val))
        self.hold()
        self.play(FadeOut(VGroup(ubf.frames, ubf.labels, ubf.ranges, reg.frames, reg.labels, reg.digits,
                                 t0, code, val)))

        lines = CodeListing([
            "lui  t0, 0xDEADB     # t0 = 0xDEADB000",
            "addi t0, t0, -273    # 低 12 位 0xEEF = -273",
        ], font_size=28, line_gap=0.55).move_to(UP * 1.8)
        self.say("再用 addi 补上低 12 位 0xEEF 就行？小心：addi 的立即数是有符号的。",
                 FadeIn(lines[0]))
        self.say("0xEEF 的最高位是 1，按 12 位补码它表示 −273，会被符号扩展成 0xFFFFFEEF。",
                 FadeIn(lines[1]))
        calc = VGroup(
            mono("  0xDEADB000", 32, WHITE),
            mono("+ 0xFFFFFEEF", 32, WHITE),
            mono("= 0xDEADAEEF", 32, RED_B),
        ).arrange(DOWN, buff=0.18, aligned_edge=RIGHT).move_to(DOWN * 0.7)
        bar = Line(LEFT, RIGHT, stroke_color=GREY_B).match_width(calc).next_to(calc[1], DOWN, buff=0.09)
        wrong = zh("高位被借走了 1！", 26, RED_B).next_to(calc, RIGHT, buff=0.5)
        self.say("相加的结果是 0xDEADAEEF：高 20 位被“借”走了 1。",
                 FadeIn(calc[:2]), Create(bar), FadeIn(calc[2]), FadeIn(wrong))
        self.hold()
        fixed = CodeListing(["lui  t0, 0xDEADC     # 先给高位加 1"], font_size=28).move_to(lines[0], aligned_edge=LEFT)
        calc2 = VGroup(
            mono("  0xDEADC000", 32, WHITE),
            mono("+ 0xFFFFFEEF", 32, WHITE),
            mono("= 0xDEADBEEF", 32, GREEN_B),
        ).arrange(DOWN, buff=0.18, aligned_edge=RIGHT).move_to(calc)
        ok = zh("正确！", 26, GREEN_B).move_to(wrong, aligned_edge=LEFT)
        self.say("解决办法：低 12 位的最高位是 1 时，先把高 20 位加 1，写成 lui t0, 0xDEADC。",
                 Transform(lines[0], fixed), Transform(calc, calc2), Transform(wrong, ok))
        li = CodeListing(["li t0, 0xDEADBEEF   # 伪指令，汇编器自动展开"], font_size=28).next_to(calc, DOWN, buff=0.55)
        self.say("好在不用手算：伪指令 li t0, 0xDEADBEEF 会由汇编器自动展开成这两条。",
                 FadeIn(li, shift=UP * 0.15))
        self.hold()
        self.play(FadeOut(VGroup(lines, calc, bar, wrong, li)))
        au = CodeListing(["auipc rd, imm      # rd = PC + (imm << 12)"], font_size=30).move_to(UP * 0.8)
        self.say("另一条 U 型指令 auipc：把立即数左移 12 位后加到 PC 上，用来算出离当前位置很远的地址。",
                 FadeIn(au, shift=UP * 0.15))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ J
    def j_format(self):
        head = self.heading("J 型：jal")
        jbf = BitField(fmt_fields("J")).move_to(UP * 1.3)
        self.say("jal 只需要 rd 和一个偏移量。于是 J 型把剩下的 20 位全都给了立即数。",
                 Write(head), FadeIn(jbf.frames), FadeIn(jbf.labels), FadeIn(jbf.ranges))
        rng = zh("偏移以 2 字节为单位：范围约 ±1 MiB", 28, YELLOW_D).next_to(jbf, DOWN, buff=0.45)
        self.say("同样以 2 字节为单位、最低位不存：21 位的偏移，范围约 ±1 MiB，足够覆盖绝大多数函数调用。",
                 FadeIn(rng))
        self.say("位序同样是打乱的：让尽量多的位和 I 型、U 型同位，符号位依旧待在第 31 位。",
                 Indicate(jbf.frames[1], color=YELLOW_D), Indicate(jbf.frames[3], color=YELLOW_D))
        self.hold()
        far = CodeListing([
            "auipc ra, 0x12345       # ra = PC + 0x12345000",
            "jalr  ra, 0x678(ra)     # 跳到 ra + 0x678，返回地址存进 ra",
        ], font_size=26, line_gap=0.52).next_to(rng, DOWN, buff=0.6)
        self.say("更远怎么办？jalr 是 I 型：跳到 rs1 + 立即数，并把 PC + 4 存进 rd。",
                 FadeIn(far[1], shift=UP * 0.1))
        self.say("配合 auipc 先算出高 20 位，就能跳到 32 位地址空间的任何位置。伪指令 call 就是这么展开的。",
                 FadeIn(far[0], shift=UP * 0.1))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ overview
    def overview(self):
        kinds = "RISBUJ"
        fields = [BitField(fmt_fields(k), box_h=0.38, box_w=0.34, show_ranges=False, label_size=16,
                           font_size=18) for k in kinds]
        stack = VGroup(*fields).arrange(DOWN, buff=0.26).move_to(UP * 0.55)
        tags = VGroup(*[mono(k, 28, WHITE).next_to(f.frames, LEFT, buff=0.35) for k, f in zip(kinds, fields)])
        self.say("把 RV32I 的全部 6 种格式放在一起看。",
                 LaggedStart(*[FadeIn(VGroup(t, f), shift=UP * 0.1) for t, f in zip(tags, fields)],
                             lag_ratio=0.2, run_time=2.4))
        left = fields[0].frames.get_left()[0]
        bw = fields[0].box_w

        def band(hi, lo, color):
            xl = left + (31 - hi) * bw
            xr = left + (32 - lo) * bw
            top = stack.get_top()[1] + 0.08
            bot = stack.get_bottom()[1] - 0.08
            return Rectangle(width=xr - xl, height=top - bot, stroke_color=color, stroke_width=3,
                             fill_color=color, fill_opacity=0.07).move_to([(xl + xr) / 2, (top + bot) / 2, 0])

        bands = [band(19, 15, FIELD_COLORS["rs1"]), band(24, 20, FIELD_COLORS["rs2"]),
                 band(11, 7, FIELD_COLORS["rd"]), band(6, 0, FIELD_COLORS["opcode"])]
        self.say("rs1、rs2、rd 和 opcode 的位置始终固定；变化的只是立即数的摆法。",
                 *[Create(b) for b in bands])
        sign = band(31, 31, RED_C)
        self.say("而立即数的符号位，永远是第 31 位：硬件可以在知道指令类型之前就开始做符号扩展。",
                 Create(sign))
        self.hold(0.8)
