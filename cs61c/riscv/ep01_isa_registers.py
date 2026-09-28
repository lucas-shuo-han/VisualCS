import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F403


class Ep01ISARegisters(NarratedScene):
    def construct(self):
        self.title_card(1, "从 C 到汇编", "指令集架构 · 寄存器 · 算术指令")
        self.hook()
        self.isa()
        self.registers()
        self.arithmetic()
        self.compile_expr()
        self.immediates()
        self.end_card(
            [
                "ISA 是软件与硬件之间的契约",
                "RV32I 有 32 个 32 位寄存器，x0 恒为 0",
                "算术指令：add / sub rd, rs1, rs2",
                "addi 带 12 位立即数；mv、li、nop 是伪指令",
            ],
            next_title="内存：lw、sw 与字节寻址",
        )

    # ------------------------------------------------------------------ hook
    def hook(self):
        c = CodeListing(["a = b + c;"], lang="c", font_size=40).move_to(UP * 2.4)
        self.say("我们写下一行 C 代码：a = b + c;", FadeIn(c, shift=DOWN * 0.2))

        bits = "0000000 01100 01011 000 01010 0110011"
        cols = [FIELD_COLORS[k] for k in ("funct7", "rs2", "rs1", "funct3", "rd", "opcode")]
        markup = " ".join(span(b, col) for b, col in zip(bits.split(), cols))
        machine = MarkupText(markup, font=MONO, font_size=34).move_to(DOWN * 1.9)
        self.say("但 CPU 并不认识 C。它只会执行一串串的 0 和 1。",
                 FadeIn(machine, lag_ratio=0.05, run_time=1.5))

        asm = CodeListing(["add x10, x11, x12"], font_size=40).move_to(UP * 0.25)
        a1 = Arrow(c.get_bottom(), asm.get_top(), buff=0.2, color=GREY_B)
        a2 = Arrow(asm.get_bottom(), machine.get_top(), buff=0.2, color=GREY_B)
        l1 = zh("编译器 Compiler", 26, GREY_A).next_to(a1, RIGHT, buff=0.3)
        l2 = zh("汇编器 Assembler", 26, GREY_A).next_to(a2, RIGHT, buff=0.3)
        self.say("中间隔着两步翻译：编译器先把 C 变成汇编语言……",
                 GrowArrow(a1), FadeIn(l1), FadeIn(asm, shift=DOWN * 0.2))
        self.say("……汇编器再把每条汇编指令变成一个 32 位的机器码。",
                 GrowArrow(a2), FadeIn(l2))
        self.play(Circumscribe(machine, color=YELLOW_D, time_width=0.6, run_time=1.5))
        self.say("汇编和机器码几乎一一对应：汇编就是机器指令的“文字版”。",
                 Indicate(asm, color=YELLOW_D, scale_factor=1.05))
        self.hold(0.3)
        self.clear_stage()

    # ------------------------------------------------------------------ ISA
    def isa(self):
        sw = box_label("软件：C、Python、操作系统……", BLUE_C, w=9, h=1.1)
        isa = box_label("指令集架构  ISA", YELLOW_D, w=9, h=0.9, font_size=32)
        hw = box_label("硬件：CPU 电路", GREEN_C, w=9, h=1.1)
        stack = VGroup(sw, isa, hw).arrange(DOWN, buff=0.35).move_to(UP * 0.4)
        self.say("汇编指令组成的“词汇表”，叫做指令集架构（ISA）。",
                 LaggedStart(FadeIn(sw, shift=DOWN * 0.2), FadeIn(hw, shift=UP * 0.2),
                             lag_ratio=0.3))
        self.play(GrowFromCenter(isa))
        self.say("它是软件和硬件之间的契约：软件只使用这些指令，硬件保证正确执行它们。",
                 Indicate(isa, color=YELLOW_D, scale_factor=1.04))
        self.hold()

        self.play(stack.animate.scale(0.7).to_edge(UP, buff=0.4))
        names = VGroup(
            box_label("x86", GREY_B, w=2.4, font=MONO),
            box_label("ARM", GREY_B, w=2.4, font=MONO),
            box_label("RISC-V", YELLOW_D, w=2.4, font=MONO),
        ).arrange(RIGHT, buff=0.6).move_to(DOWN * 1.2)
        self.say("x86、ARM、RISC-V 都是 ISA。CS61C 用的是 RISC-V：开源、简洁、规整。",
                 LaggedStart(*[FadeIn(n, shift=UP * 0.2) for n in names], lag_ratio=0.3))
        self.play(names[2].animate.scale(1.15), names[0].animate.set_opacity(0.4),
                  names[1].animate.set_opacity(0.4))
        risc = zh("RISC = Reduced Instruction Set Computer  精简指令集", 26, GREY_A)
        risc.next_to(names, DOWN, buff=0.45)
        self.say("RISC 是“精简指令集”：指令少而规整，硬件就能做得简单、快速。",
                 FadeIn(risc, shift=UP * 0.2))
        self.say("RV32I 基础指令集只有大约 40 条指令，这个系列就能覆盖其中的大部分。")
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ registers
    def registers(self):
        head = self.heading("寄存器 Registers")
        self.say("RISC-V 的算术指令只能操作寄存器：CPU 内部极少量、极快的存储单元。",
                 Write(head))
        rf = RegisterFile().move_to(DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(VGroup(rf.cells[i], rf.names[i], rf.vals[i]), scale=0.8)
                                for i in range(32)], lag_ratio=0.04, run_time=2.2))
        self.say("RV32I 一共有 32 个整数寄存器：x0 到 x31。",
                 LaggedStart(*[Indicate(rf.names[i], color=YELLOW_D) for i in range(32)],
                             lag_ratio=0.03, run_time=1.8))
        one = rf.cells[8]
        brace = Brace(one, UP, buff=0.05, color=YELLOW_D)
        bl = zh("32 位 = 4 字节 = 1 个字（word）", 24, YELLOW_D).next_to(brace, UP, buff=0.1)
        self.say("每个寄存器 32 位宽。32 位，也就是 4 个字节，称为一个“字”。",
                 GrowFromCenter(brace), FadeIn(bl))
        self.hold()
        self.play(FadeOut(brace), FadeOut(bl))

        # registers vs memory
        self.play(rf.animate.scale(0.55).move_to(LEFT * 3.7 + DOWN * 0.1))
        rf_tag = zh("寄存器：32 × 4 B = 128 字节", 24, BLUE_B).next_to(rf, DOWN, buff=0.35)
        mem = Rectangle(width=5.0, height=4.0, stroke_color=GREEN_C, fill_color=GREEN_C,
                        fill_opacity=0.08).move_to(RIGHT * 3.5 + UP * 0.2)
        grid = VGroup(*[
            Line(mem.get_corner(UL) + RIGHT * 0.1 + DOWN * (k * 0.2 + 0.2),
                 mem.get_corner(UR) + LEFT * 0.1 + DOWN * (k * 0.2 + 0.2),
                 stroke_width=1, stroke_color=GREEN_C, stroke_opacity=0.35)
            for k in range(19)
        ])
        mem_tag = zh("内存：数十亿字节", 24, GREEN_B).next_to(mem, DOWN, buff=0.35)
        self.say("为什么只有 32 个？因为越小越快。",
                 FadeIn(rf_tag), FadeIn(mem), Create(grid, lag_ratio=0.05), FadeIn(mem_tag))
        self.say("寄存器在一个时钟周期内就能读写，而访问内存往往要慢上百倍。",
                 Indicate(rf, color=BLUE_B), Wiggle(mem_tag))
        self.hold()
        self.play(FadeOut(VGroup(mem, grid, mem_tag, rf_tag)))
        self.play(rf.animate.scale(1 / 0.55).move_to(DOWN * 0.3))

        # x0
        x0box = SurroundingRectangle(VGroup(rf.names[0], rf.cells[0]), color=YELLOW_D, buff=0.1)
        self.say("其中 x0 很特别：它的值永远是 0。", Create(x0box))
        five = mono("5", 30, RED_B).next_to(rf.cells[0], UP, buff=0.6)
        self.say("往 x0 里写任何值，都会被悄悄丢弃。", FadeIn(five, shift=DOWN * 0.2))
        self.play(five.animate.move_to(rf.cells[0]).scale(0.8), run_time=0.8)
        self.play(FadeOut(five, scale=0.2), Indicate(rf.vals[0], color=YELLOW_D, scale_factor=1.6))
        self.say("听起来有点浪费？稍后你就会看到它有多好用。")
        self.hold()
        self.play(FadeOut(x0box))

        # ABI names
        self.say("在汇编里，我们通常用寄存器的“别名”，也就是 ABI 名字。",
                 LaggedStart(*[Transform(rf.names[i], rf.abi_label(i)) for i in range(32)],
                             lag_ratio=0.03, run_time=2.4))

        t_grp = VGroup(*[VGroup(rf.names[i], rf.cells[i]) for i in range(32) if ABI_NAMES[i][0] == "t" and ABI_NAMES[i] != "tp"])
        s_grp = VGroup(*[VGroup(rf.names[i], rf.cells[i]) for i in range(32) if ABI_NAMES[i][0] == "s" and ABI_NAMES[i] != "sp"])
        a_grp = VGroup(*[VGroup(rf.names[i], rf.cells[i]) for i in range(32) if ABI_NAMES[i][0] == "a"])
        self.say("t 开头的是临时寄存器（temporary）……",
                 *[Indicate(g, color=C_T, scale_factor=1.1) for g in t_grp])
        self.say("s 开头的是保存寄存器（saved）……",
                 *[Indicate(g, color=C_S, scale_factor=1.1) for g in s_grp])
        self.say("a 开头的用来传递参数（argument）和返回值。",
                 *[Indicate(g, color=C_A, scale_factor=1.1) for g in a_grp])
        special = VGroup(*[VGroup(rf.names[i], rf.cells[i]) for i in (1, 2, 3, 4)])
        self.say("ra、sp 等有专门用途。它们的规则，第 4 集讲函数调用时再细说。",
                 *[Indicate(g, color=RED_B, scale_factor=1.1) for g in special])
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ add / sub
    def arithmetic(self):
        head = self.heading("算术指令")
        syntax = CodeListing(["add rd, rs1, rs2"], font_size=48).move_to(UP * 1.6)
        parts = [("add", "操作"), ("rd", "目标"), ("rs1", "源 1"), ("rs2", "源 2")]
        notes = VGroup()
        for tok, lab in parts:
            g = syntax.glyphs(0, tok)
            n = zh(lab, 24, GREY_A).next_to(g, DOWN, buff=0.35)
            notes.add(n)
        self.say("算术指令的格式是固定的：操作名、目标寄存器，然后是两个源寄存器。",
                 Write(head), FadeIn(syntax, shift=DOWN * 0.2))
        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.15) for n in notes], lag_ratio=0.25))
        meaning = mono("rd = rs1 + rs2", 40, YELLOW_D).next_to(notes, DOWN, buff=0.7)
        self.say("add rd, rs1, rs2 的意思就是：rd = rs1 + rs2。", Write(meaning))
        self.hold()
        self.play(FadeOut(VGroup(syntax, notes, meaning)))

        regs = reg_column([("s0", 0), ("s1", 7), ("s2", 5)], width=1.6)
        regs.move_to(LEFT * 4.2 + DOWN * 0.3)
        alu = alu_shape(label="+").move_to(RIGHT * 1.4 + DOWN * 0.1)
        code = CodeListing(["add s0, s1, s2"], font_size=40).move_to(UP * 2.2 + RIGHT * 0.9)
        self.say("举个例子：s1 里是 7，s2 里是 5。",
                 FadeIn(regs, shift=RIGHT * 0.2), FadeIn(alu))
        self.say("执行 add s0, s1, s2：两个值被送进加法器……", FadeIn(code, shift=DOWN * 0.2))
        v1 = regs[1].val.copy()
        v2 = regs[2].val.copy()
        self.play(v1.animate.move_to(alu.get_center() + [-0.4, 0.95, 0]),
                  v2.animate.move_to(alu.get_center() + [0.4, 0.95, 0]), run_time=1.2)
        res = mono("12", 30, YELLOW_D).move_to(alu.get_center() + DOWN * 1.0)
        self.play(ReplacementTransform(VGroup(v1, v2), res), Indicate(alu[0], color=BLUE_B))
        self.say("……得到 12，写回 s0。", res.animate.move_to(regs[0].box))
        self.play(regs[0].set(12), FadeOut(res))
        self.hold()

        code2 = CodeListing(["sub s0, s1, s2"], font_size=40).move_to(code)
        alu2 = alu_shape(label="−").move_to(alu)
        self.say("sub 也一样：rd = rs1 − rs2。注意顺序，被减数是 rs1，减数是 rs2。",
                 Transform(code, code2), Transform(alu, alu2))
        v1 = regs[1].val.copy()
        v2 = regs[2].val.copy()
        self.play(v1.animate.move_to(alu.get_center() + [-0.4, 0.95, 0]),
                  v2.animate.move_to(alu.get_center() + [0.4, 0.95, 0]), run_time=1.2)
        res = mono("2", 30, YELLOW_D).move_to(alu.get_center() + DOWN * 1.0)
        self.play(ReplacementTransform(VGroup(v1, v2), res))
        self.play(res.animate.move_to(regs[0].box))
        self.play(regs[0].set(2), FadeOut(res))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ a = b + c - d
    def compile_expr(self):
        c = CodeListing(["a = b + c - d;"], lang="c", font_size=40).move_to(UP * 2.7)
        self.say("来编译一个稍复杂的表达式：a = b + c - d。", FadeIn(c, shift=DOWN * 0.2))
        mapping = VGroup(*[
            VGroup(mono(v, 28, WHITE), mono("→", 28, GREY), mono(r, 28, C_S)).arrange(RIGHT, buff=0.2)
            for v, r in [("a", "s0"), ("b", "s1"), ("c", "s2"), ("d", "s3")]
        ]).arrange(RIGHT, buff=0.8).next_to(c, DOWN, buff=0.45)
        self.say("假设编译器已经把 a、b、c、d 分别放在 s0、s1、s2、s3 中。",
                 LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in mapping], lag_ratio=0.2))

        asm = CodeListing([
            "add t0, s1, s2    # t0 = b + c",
            "sub s0, t0, s3    # a = t0 - d",
        ], font_size=30).move_to(DOWN * 0.2 + RIGHT * 1.6)
        regs = reg_column([("s0", 0), ("s1", 10), ("s2", 20), ("s3", 5), ("t0", 0)],
                          width=1.4, buff=0.16)
        regs.scale(0.9).move_to(LEFT * 4.6 + DOWN * 0.7)
        self.say("每条指令只能做一次运算，所以要拆成两步，中间结果放在临时寄存器 t0。",
                 FadeIn(asm, shift=UP * 0.2), FadeIn(regs, shift=RIGHT * 0.2))
        self.hold()
        cur = asm.line_box(0)
        self.say("设 b = 10，c = 20，d = 5。第一步：t0 = 10 + 20 = 30。", FadeIn(cur))
        self.play(Indicate(regs[1]), Indicate(regs[2]))
        self.play(regs[4].set(30))
        self.say("第二步：s0 = t0 − d = 30 − 5 = 25。完成！", cur.animate.become(asm.line_box(1)))
        self.play(Indicate(regs[4]), Indicate(regs[3]))
        self.play(regs[0].set(25))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ immediates
    def immediates(self):
        head = self.heading("立即数 Immediate")
        c = CodeListing(["a = b + 5;"], lang="c", font_size=40).move_to(UP * 2.0)
        self.say("如果要加的是一个常数呢？比如 a = b + 5。", Write(head), FadeIn(c))
        addi = CodeListing(["addi s0, s1, 5"], font_size=44).move_to(UP * 0.6)
        five = addi.glyphs(0, "5")
        note = zh("立即数：直接写在指令里的常数", 26, C_NUM).next_to(addi, DOWN, buff=0.45)
        self.say("用 addi。i 表示 immediate，立即数：这个常数直接编码在指令里。",
                 FadeIn(addi, shift=DOWN * 0.2))
        self.play(Circumscribe(five, color=C_NUM), FadeIn(note, shift=UP * 0.15))
        self.hold()
        neg = CodeListing(["addi s0, s1, -5   # a = b - 5"], font_size=34).next_to(note, DOWN, buff=0.5)
        self.say("RISC-V 没有 subi：减一个常数，就是加一个负数。", FadeIn(neg, shift=UP * 0.2))
        rng = zh("立即数只有 12 位：范围 −2048 ~ 2047（原因见第 5 集）", 26, GREY_A)
        rng.next_to(neg, DOWN, buff=0.45)
        self.say("立即数只有 12 位，范围是 −2048 到 2047。为什么是 12 位？第 5 集揭晓。",
                 FadeIn(rng))
        self.hold()
        self.play(FadeOut(VGroup(c, addi, note, neg, rng)))

        rows = [
            ("mv   s0, s1", "addi s0, s1, 0", "复制：加 0"),
            ("li   s0, 42", "addi s0, x0, 42", "装入常数：从 x0 加"),
            ("nop", "addi x0, x0, 0", "什么也不做"),
        ]
        left = CodeListing([r[0] for r in rows], font_size=32, line_gap=1.0)
        right = CodeListing([r[1] for r in rows], font_size=32, line_gap=1.0)
        left.move_to(LEFT * 3.6 + UP * 0.4)
        right.move_to(RIGHT * 1.2 + UP * 0.4)
        right.align_to(left, UP)
        arrows = VGroup(*[
            Arrow(LEFT * 0.5, RIGHT * 0.5, color=GREY_B, buff=0).move_to(
                [(left.get_right()[0] + right.get_left()[0]) / 2, left[i].get_center()[1], 0])
            for i in range(3)
        ])
        notes = VGroup(*[
            zh(r[2], 24, GREY_A).next_to(right[i], DOWN, buff=0.12).align_to(right, LEFT)
            for i, r in enumerate(rows)
        ])
        VGroup(left, right, arrows, notes).move_to(UP * 0.2)
        self.say("现在看 x0 的妙用。汇编器提供了一些“伪指令”，它们会被替换成真实指令。",
                 FadeIn(left, shift=RIGHT * 0.2))
        self.say("mv 是加 0；li 是从 x0 出发加一个常数……",
                 LaggedStart(*[GrowArrow(a) for a in arrows[:2]], lag_ratio=0.3),
                 FadeIn(right[0]), FadeIn(right[1]), FadeIn(notes[0]), FadeIn(notes[1]))
        self.say("……nop 则把结果写进 x0：什么都不会改变。",
                 GrowArrow(arrows[2]), FadeIn(right[2]), FadeIn(notes[2]))
        self.play(Circumscribe(right.glyphs(2, "x0"), color=YELLOW_D))
        self.say("只用一个恒为 0 的寄存器，就省掉了好几条专用指令。这就是 RISC 的思路。")
        self.hold(0.5)
