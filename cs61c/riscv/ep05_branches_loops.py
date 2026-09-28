import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F403


def small(s, size, color=C_TEXT):
    """Small label text. Built at twice the size and scaled down: at small sizes Pango
    rounds glyph positions and squeezes the spaces between English words."""
    return zh(s, size * 2, color).scale(0.5)


class Ep05BranchesLoops(NarratedScene):
    def construct(self):
        self.title_card()
        self.program_counter()
        self.branches()
        self.if_else()
        self.logic_ops()
        self.loop()
        self.end_card(
            [
                "PC 指向当前指令；顺序执行时每次加 4",
                "条件分支：beq bne blt bge bltu bgeu",
                "if-else：条件取反，再用 j 跳过 else",
                "位运算：and or xor，移位 sll srl sra",
                "循环：开头判断并跳出，末尾跳回开头",
            ],
        )

    # ------------------------------------------------------------------ PC
    def program_counter(self):
        code = CodeListing([
            "addi t0, x0, 3",
            "addi t1, x0, 4",
            "add  t2, t0, t1",
            "sub  t3, t2, t0",
        ], font_size=34, line_gap=0.72).move_to(LEFT * 0.6 + UP * 0.3)
        addrs = VGroup(*[mono(f"0x{4 * i:02X}", 28, GREY).next_to(code.left_of(i, 0.5), LEFT, buff=0)
                         for i in range(4)])
        pc = RegBox("PC", "0x00", color=YELLOW_D, width=1.6, font_size=30).move_to(RIGHT * 4.6 + UP * 2.3)
        self.say("程序就是内存里的一串指令。CPU 用一个特殊的寄存器——程序计数器（PC）——记住当前指令的地址。",
                 FadeIn(code, shift=UP * 0.2), FadeIn(addrs), FadeIn(pc))
        arrow = pc_arrow().next_to(addrs[0], LEFT, buff=0.2)
        box = code.line_box(0)
        self.play(FadeIn(arrow), FadeIn(box))
        self.say("每条指令占 4 个字节。执行完一条，PC 就加 4，指向下一条。")
        for i in range(1, 4):
            self.play(arrow.animate.next_to(addrs[i], LEFT, buff=0.2), box.animate.become(code.line_box(i)),
                      pc.set(f"0x{4 * i:02X}"), run_time=0.8)
            self.wait(0.3)
        self.say("可如果只能一条接一条地执行，就写不出 if，也写不出循环。我们需要能“跳”的指令。")
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ branches
    def branches(self):
        head = self.heading("条件分支")
        syn = CodeListing(["beq rs1, rs2, Label"], font_size=46).move_to(UP * 2.0)
        mean = zh("如果 rs1 == rs2，跳到 Label；否则执行下一条", 30, GREY_A).next_to(syn, DOWN, buff=0.4)
        self.say("条件分支 beq（branch if equal）：如果 rs1 等于 rs2，就跳到 Label；否则照常执行下一条。",
                 Write(head), FadeIn(syn, shift=DOWN * 0.2))
        self.play(FadeIn(mean, shift=UP * 0.15))
        self.hold()

        rows = [("beq", "=="), ("bne", "!="), ("blt", "<"), ("bge", ">="),
                ("bltu", "< 无符号"), ("bgeu", ">= 无符号")]
        cells = VGroup()
        for m, cond in rows:
            cells.add(VGroup(mono(m, 32, C_MNEM), Text(cond, font=CJK, font_size=28, color=WHITE)).arrange(RIGHT, buff=0.4))
        grid = VGroup(VGroup(*cells[0::2]).arrange(DOWN, buff=0.35, aligned_edge=LEFT),
                      VGroup(*cells[1::2]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)).arrange(RIGHT, buff=2.2)
        grid.next_to(mean, DOWN, buff=0.6)
        self.say("RISC-V 一共 6 条条件分支：相等、不等、小于、大于等于，以及小于和大于等于的无符号版本。",
                 LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cells], lag_ratio=0.15))
        bgt = CodeListing(["bgt a, b, L   =   blt b, a, L"], font_size=30).next_to(grid, DOWN, buff=0.5)
        self.say("没有 bgt 和 ble？交换两个操作数就行：a > b 就是 b < a。汇编器也提供了这类伪指令。",
                 FadeIn(bgt, shift=UP * 0.15))
        self.hold()
        self.play(FadeOut(VGroup(grid, bgt, mean)), syn.animate.move_to(UP * 2.4))
        j = CodeListing(["j Label      # = jal x0, Label"], font_size=36).next_to(syn, DOWN, buff=0.6)
        self.say("还有无条件跳转 j Label：直接跳过去。它是 jal x0, Label 的简写，第 7 集会讲 jal。",
                 FadeIn(j, shift=UP * 0.15))
        lab = zh("Label  =  某条指令的地址", 30, C_LABEL).next_to(j, DOWN, buff=0.6)
        self.say("Label 只是给代码中某个位置起的名字，汇编器会把它换算成地址。", FadeIn(lab))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ if / else
    def if_else(self):
        c = CodeListing([
            "if (i == j)",
            "    f = g + h;",
            "else",
            "    f = g - h;",
        ], lang="c", font_size=26, line_gap=0.5).to_corner(UL, buff=0.5).shift(DOWN * 0.4)
        mapping = VGroup(
            mono("f  g  h  i  j", 24, WHITE),
            mono("s0 s1 s2 s3 s4", 24, C_REG),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(c, DOWN, buff=0.45).align_to(c, LEFT)
        self.say("来翻译一个 if-else。f、g、h、i、j 分别放在 s0 到 s4。",
                 FadeIn(c, shift=RIGHT * 0.2), FadeIn(mapping))
        asm = CodeListing([
            "    bne s3, s4, Else  # i != j 就跳",
            "    add s0, s1, s2    # f = g + h",
            "    j   Exit",
            "Else:",
            "    sub s0, s1, s2    # f = g - h",
            "Exit:",
        ], font_size=28, line_gap=0.56)
        asm.to_edge(RIGHT, buff=0.35).set_y(0.9)
        self.say("关键技巧是“条件取反”：C 里 i == j 时执行 then 部分，所以汇编里反过来用 bne——不相等就跳过它，直接去 Else。",
                 FadeIn(asm, shift=LEFT * 0.2))
        self.play(Circumscribe(asm.glyphs(0, "bne"), color=RED_B), Circumscribe(c.glyphs(0, "=="), color=RED_B))
        self.hold()

        vals = mono("i = 5, j = 5", 28, YELLOW_D).next_to(mapping, DOWN, buff=0.5).align_to(c, LEFT)
        arrow = pc_arrow().move_to(asm.left_of(0, 0.5))
        self.say("情况一：i 等于 j。bne 不跳，执行 add……", FadeIn(vals), FadeIn(arrow))
        self.play(arrow.animate.move_to(asm.left_of(1, 0.5)))
        self.play(Indicate(asm[1], color=YELLOW_D))
        self.play(arrow.animate.move_to(asm.left_of(2, 0.5)))
        jump = CurvedArrow(asm.left_of(2, 0.6), asm.left_of(5, 0.6), angle=TAU / 5, color=YELLOW_D)
        self.say("……然后 j Exit 跳过 else 部分。", Create(jump))
        self.play(arrow.animate.move_to(asm.left_of(5, 0.5)))
        self.hold()

        vals2 = mono("i = 5, j = 7", 28, TEAL_C).move_to(vals, aligned_edge=LEFT)
        self.play(FadeOut(jump), arrow.animate.move_to(asm.left_of(0, 0.5)))
        jump2 = CurvedArrow(asm.left_of(0, 0.6), asm.left_of(3, 0.6), angle=TAU / 5, color=TEAL_C)
        self.say("情况二：i 不等于 j。bne 直接跳到 Else，执行 sub，然后自然走到 Exit。",
                 Transform(vals, vals2), Create(jump2))
        self.play(arrow.animate.move_to(asm.left_of(3, 0.5)))
        self.play(arrow.animate.move_to(asm.left_of(4, 0.5)))
        self.play(Indicate(asm[4], color=TEAL_C))
        self.play(arrow.animate.move_to(asm.left_of(5, 0.5)))
        self.say("注意 j Exit 不能省：否则执行完 then 部分，程序会一路“掉进” else 部分。",
                 Circumscribe(asm[2], color=RED_B))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ logic
    def logic_ops(self):
        head = self.heading("位运算与移位")
        self.say("在写循环之前，先认识几条位运算指令。它们对 32 位数据逐位操作。", Write(head))
        a_bits, b_bits = "10110110", "00001111"
        ra = bit_row(a_bits, BLUE_B)
        rb = bit_row(b_bits, GOLD_C)
        rr = bit_row("00000110", GREEN_C)
        rows = VGroup(ra, rb, rr).arrange(DOWN, buff=0.35).move_to(UP * 0.4 + RIGHT * 0.6)
        line = Line(rr.get_left() + LEFT * 0.2, rr.get_right() + RIGHT * 0.2, stroke_color=GREY_B)
        line.next_to(rr, UP, buff=0.17)
        la = mono("t1", 30, C_REG).next_to(ra, LEFT, buff=0.5)
        lb = mono("t2", 30, C_REG).next_to(rb, LEFT, buff=0.5)
        op = mono("and", 30, C_MNEM).next_to(rr, LEFT, buff=0.5)
        note = small("（只画出最低 8 位）", 22, GREY).next_to(rows, DOWN, buff=0.35)
        self.play(FadeIn(ra), FadeIn(rb), FadeIn(la), FadeIn(lb), FadeIn(note))
        self.say("and：两位都是 1，结果才是 1。它常用来做“掩码”：只保留想要的那些位。",
                 Create(line), FadeIn(op),
                 LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in rr], lag_ratio=0.1))
        self.hold()
        op_or = mono("or", 30, C_MNEM).move_to(op, aligned_edge=RIGHT)
        self.say("or：只要有一位是 1，结果就是 1……",
                 Transform(op, op_or), set_bit_row(rr, "10111111"))
        self.hold()
        op_x = mono("xor", 30, C_MNEM).move_to(op, aligned_edge=RIGHT)
        self.say("……xor：两位不同，结果才是 1。", Transform(op, op_x), set_bit_row(rr, "10111001"))
        self.hold()
        imm = CodeListing([
            "andi t0, t1, 0xFF    # 取出最低字节",
            "xori t0, t1, -1      # 按位取反 (not)",
        ], font_size=28, line_gap=0.55).next_to(note, DOWN, buff=0.35)
        self.say("它们都有立即数版本：andi、ori、xori。比如 andi t0, t1, 0xFF 取出最低的一个字节。",
                 FadeIn(imm[0], shift=UP * 0.15))
        self.say("RISC-V 没有真正的 not 指令：-1 的每一位都是 1，与它异或就是按位取反。伪指令 not 就是这么实现的。",
                 FadeIn(imm[1], shift=UP * 0.15))
        self.hold()
        self.play(FadeOut(VGroup(ra, rb, rr, line, la, lb, op, note, imm)))

        # shifts
        src = bit_row("00010110", BLUE_B).move_to(UP * 1.2)
        lbl = mono("t1 = 22", 30, WHITE).next_to(src, LEFT, buff=0.5)
        self.say("移位指令把所有位整体挪动。sll 是逻辑左移：往左挪，右边补 0。",
                 FadeIn(src), FadeIn(lbl))
        res = bit_row("00010110", GREEN_C).move_to(DOWN * 0.4)
        code = CodeListing(["slli t0, t1, 2"], font_size=30).next_to(res, LEFT, buff=0.5)
        self.play(FadeIn(code), TransformFromCopy(src, res))
        box = res[0][0].width
        gone = VGroup(*[c[1] for c in res[:2]])
        keep = VGroup(*[c[1] for c in res[2:]])
        self.play(FadeOut(gone, shift=UP * 0.4), run_time=0.6)
        for cell in res[:2]:
            cell.remove(cell[1])
        self.play(keep.animate.shift(LEFT * 2 * box), run_time=1.0)
        zeros = VGroup(*[mono("0", 30, GREY_B).move_to(res[k][0]) for k in (6, 7)])
        self.play(FadeIn(zeros, shift=LEFT * 0.3))
        eq = mono("= 88 = 22 × 4", 30, GREEN_C).next_to(res, RIGHT, buff=0.5)
        self.say("左移 k 位，相当于乘以 2 的 k 次方：22 左移 2 位，变成 88。", Write(eq))
        self.hold()
        self.play(FadeOut(VGroup(src, lbl, res, zeros, code, eq)))

        neg = bit_row("11110000", BLUE_B).move_to(UP * 1.6)
        nl = mono("-16", 30, WHITE).next_to(neg, LEFT, buff=0.5)
        srl = bit_row("00111100", TEAL_C).move_to(UP * 0.2)
        sra = bit_row("11111100", GREEN_C).move_to(DOWN * 1.1)
        srl_l = mono("srli 2", 28, C_MNEM).next_to(srl, LEFT, buff=0.5)
        sra_l = mono("srai 2", 28, C_MNEM).next_to(sra, LEFT, buff=0.5)
        srl_n = zh("左边补 0：不再是负数", 26, TEAL_C).next_to(srl, RIGHT, buff=0.4)
        sra_n = zh("左边补符号位：−16 ÷ 4 = −4", 26, GREEN_C).next_to(sra, RIGHT, buff=0.4)
        VGroup(neg, nl, srl, sra, srl_l, sra_l, srl_n, sra_n).move_to(UP * 0.2)
        # a real srli fills bit 31, not bit 7: say that this row is a toy 8-bit register
        toy = small("（示意：假设寄存器只有 8 位）", 22, GREY).next_to(VGroup(sra_l, sra), DOWN, buff=0.4)
        self.say("右移有两种。srl 是逻辑右移：左边补 0。",
                 FadeIn(neg), FadeIn(nl), FadeIn(toy), FadeIn(srl_l), TransformFromCopy(neg, srl))
        self.play(FadeIn(srl_n))
        self.say("sra 是算术右移：左边补符号位。这样负数除以 2 的幂之后，依然是负数。",
                 FadeIn(sra_l), TransformFromCopy(neg, sra))
        self.play(FadeIn(sra_n), Indicate(VGroup(*sra[:2]), color=GREEN_C))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ loop
    def loop(self):
        c = CodeListing([
            "int sum = 0;",
            "for (int i = 0; i < n; i++)",
            "    sum += A[i];",
        ], lang="c", font_size=26, line_gap=0.44).to_corner(UL, buff=0.45)
        self.say("现在把这些组合起来：对数组 A 的 n 个元素求和。", FadeIn(c, shift=RIGHT * 0.2))
        asm_src = [
            "    addi t0, x0, 0      # i = 0",
            "    addi s1, x0, 0      # sum = 0",
            "Loop:",
            "    bge  t0, a1, Done   # i >= n 就结束",
            "    slli t1, t0, 2      # t1 = i * 4",
            "    add  t1, a0, t1     # t1 = &A[i]",
            "    lw   t2, 0(t1)      # t2 = A[i]",
            "    add  s1, s1, t2     # sum += A[i]",
            "    addi t0, t0, 1      # i++",
            "    j    Loop",
            "Done:",
        ]
        asm = CodeListing(asm_src, font_size=23, line_gap=0.4)
        asm.next_to(c, DOWN, buff=0.35).align_to(c, LEFT).shift(RIGHT * 0.9)
        regs = reg_column([("a0", "0x100"), ("a1", 4), ("t0", 0), ("t1", 0), ("t2", 0), ("s1", 0)],
                          width=1.5, buff=0.14, font_size=22)
        regs.move_to(RIGHT * 3.9 + UP * 0.9)
        names = VGroup(*[small(s, 20, GREY_B).next_to(r, RIGHT, buff=0.15) for s, r in
                         zip(["A 的地址", "n", "i", "", "", "sum"], regs)])
        arr_vals = [3, 1, 4, 1]
        arr = VGroup()
        for k, v in enumerate(arr_vals):
            sq = Rectangle(width=0.9, height=0.6, stroke_color=GREEN_C, fill_color=GREEN_C, fill_opacity=0.1)
            t = mono(str(v), 26).move_to(sq)
            ad = mono(f"0x{0x100 + 4 * k:X}", 16, GREY).next_to(sq, DOWN, buff=0.1)
            arr.add(VGroup(sq, t, ad))
        arr.arrange(RIGHT, buff=0).next_to(regs, DOWN, buff=0.6).align_to(regs, LEFT).shift(RIGHT * 0.45)
        arr_l = mono("A", 28, GREEN_B).next_to(arr, LEFT, buff=0.25)
        self.say("A 的地址在 a0，n 在 a1；i 用 t0，sum 用 s1。",
                 FadeIn(asm, shift=UP * 0.2), FadeIn(regs), FadeIn(names), FadeIn(arr), FadeIn(arr_l))
        self.hold()

        back = CurvedArrow(asm.left_of(9, 0.2), asm.left_of(2, 0.2), angle=-TAU / 5, color=BLUE_B)
        out = CurvedArrow(asm.right_of(3, 0.15), asm.right_of(10, 0.15), angle=-TAU / 5, color=RED_B)
        self.say("循环的骨架：开头检查条件，不满足就跳出；循环体末尾，无条件跳回开头。",
                 Create(back), Create(out))
        self.say("条件又取反了：C 里 i < n 时继续，汇编里 i >= n 时跳出。",
                 Circumscribe(asm.glyphs(3, "bge"), color=RED_B), Circumscribe(c.glyphs(1, "i < n"), color=RED_B))
        self.say("A[i] 的地址是 A + 4i：用 slli 左移 2 位算出 4i，再加上基地址。",
                 Indicate(VGroup(asm[4], asm[5]), color=YELLOW_D, scale_factor=1.03))
        self.hold()

        box = asm.line_box(0)
        ptr = Triangle(color=YELLOW_D, fill_opacity=1).scale(0.12).rotate(PI)
        ptr.next_to(arr[0], UP, buff=0.08)

        def go(i, *anims, rt=0.55):
            self.play(box.animate.become(asm.line_box(i)), *anims, run_time=rt)

        R = {n: regs[k] for k, n in enumerate(["a0", "a1", "t0", "t1", "t2", "s1"])}
        self.say("第一轮：i = 0。bge 不成立，算出地址 0x100，读到 A[0] = 3，sum 变成 3。", FadeIn(box))
        go(1)
        go(3)
        go(4, R["t1"].set(0))
        go(5, R["t1"].set("0x100"))
        go(6, R["t2"].set(3), FadeIn(ptr))
        go(7, R["s1"].set(3))
        go(8, R["t0"].set(1))
        go(9)
        go(3)
        self.hold()

        total = 3
        self.say("之后每一轮都一样：算出 A + 4i，取出 A[i] 累加进 sum，再让 i 加 1……")
        for i in range(1, 4):
            total += arr_vals[i]
            rt = 0.3
            go(4, R["t1"].set(4 * i), rt=rt)
            go(5, R["t1"].set(f"0x{0x100 + 4 * i:X}"), rt=rt)
            go(6, R["t2"].set(arr_vals[i]), ptr.animate.next_to(arr[i], UP, buff=0.08), rt=rt)
            go(7, R["s1"].set(total), rt=rt)
            go(8, R["t0"].set(i + 1), rt=rt)
            go(9, rt=rt)
            go(3, rt=rt)
        self.say("当 i 增加到 4，bge 条件成立，跳到 Done。sum = 3 + 1 + 4 + 1 = 9。",
                 Indicate(R["t0"]), Indicate(R["a1"]))
        go(10, rt=0.8)
        self.play(Circumscribe(R["s1"], color=YELLOW_D))
        self.hold(0.5)
