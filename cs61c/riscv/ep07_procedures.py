import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F403


def addr_labels(listing, addrs, size=22):
    """addrs: list aligned with listing lines; None for lines without an address."""
    g = VGroup()
    for i, a in enumerate(addrs):
        if a is None:
            continue
        t = mono(f"0x{a:X}", size, GREY).next_to(listing.left_of(i, 0.35), LEFT, buff=0)
        g.add(t)
    return g


class Ep07Procedures(NarratedScene):
    def construct(self):
        self.title_card()
        self.six_steps()
        self.jal_ret()
        self.convention()
        self.stack()
        self.sum_square()
        self.end_card(
            [
                "参数放在 a0–a7，返回值放在 a0（和 a1）",
                "jal 把返回地址存进 ra 再跳转；jr ra 返回",
                "t、a、ra 由调用者保存；s、sp 由被调用者保存",
                "栈向低地址增长：减 sp 压栈，加 sp 出栈",
                "会调用别的函数的函数，必须先保存 ra",
            ],
        )

    # ------------------------------------------------------------------ six steps
    def six_steps(self):
        head = self.heading("调用一个函数，要做哪些事？")
        steps = [
            ("把参数放到函数拿得到的地方", "a0–a7"),
            ("跳转到函数", "jal"),
            ("为函数准备局部存储", "栈"),
            ("执行函数体", ""),
            ("把返回值放到调用者拿得到的地方", "a0"),
            ("跳回调用的位置", "jr ra"),
        ]
        rows = VGroup()
        for k, (s, tag) in enumerate(steps):
            num = mono(f"{k + 1}", 30, YELLOW_D)
            txt = zh(s, 30)
            row = VGroup(num, txt).arrange(RIGHT, buff=0.35)
            if tag:
                t = (zh if any(ord(c) > 0x2E7F for c in tag) else mono)(tag, 28, C_REG)
                t.next_to(txt, RIGHT, buff=0.5)
                row.add(t)
            rows.add(row)
        rows.arrange(DOWN, buff=0.34, aligned_edge=LEFT).move_to(DOWN * 0.1)
        self.say("调用一个函数，要经过六个基本步骤。", Write(head))
        self.say("先把参数放到函数拿得到的地方，然后跳过去……",
                 LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows[:2]], lag_ratio=0.4))
        self.say("……函数给自己准备局部存储，执行函数体……",
                 LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows[2:4]], lag_ratio=0.4))
        self.say("……把返回值放好，最后跳回调用它的地方。",
                 LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows[4:]], lag_ratio=0.4))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ jal / jr
    def jal_ret(self):
        c = CodeListing([
            "int sum(int x, int y) { return x + y; }",
            "a = sum(a, b);        // a→s0, b→s1",
        ], lang="c", font_size=26, line_gap=0.46).to_corner(UL, buff=0.45)
        main = CodeListing([
            "mv   a0, s0     # x = a",
            "mv   a1, s1     # y = b",
            "jal  ra, sum    # 调用",
            "mv   s0, a0     # a = 返回值",
        ], font_size=28, line_gap=0.52)
        fn = CodeListing([
            "sum:",
            "    add  a0, a0, a1",
            "    jr   ra",
        ], font_size=28, line_gap=0.52)
        main.move_to(LEFT * 1.6 + UP * 0.7)
        fn.next_to(main, DOWN, buff=0.7).align_to(main, LEFT)
        ma = addr_labels(main, [0x1000, 0x1004, 0x1008, 0x100C])
        fa = addr_labels(fn, [None, 0x2000, 0x2004])
        regs = reg_column([("PC", "0x1000"), ("ra", 0), ("a0", 0), ("a1", 0), ("s0", 3), ("s1", 4)],
                          width=1.7, buff=0.16, font_size=24)
        regs[0].box.set_stroke(YELLOW_D)
        regs[0].label.set_color(YELLOW_D)
        regs.move_to(RIGHT * 5.3 + DOWN * 0.1)
        self.say("看一个最简单的例子：a = sum(a, b)。a 在 s0，b 在 s1。",
                 FadeIn(c, shift=RIGHT * 0.2), FadeIn(main), FadeIn(fn), FadeIn(ma), FadeIn(fa),
                 FadeIn(regs))
        R = dict(zip(["PC", "ra", "a0", "a1", "s0", "s1"], regs))
        arrow = pc_arrow().next_to(ma[0], LEFT, buff=0.15)
        self.play(FadeIn(arrow))
        self.say("第一步：把参数放进 a0、a1。返回值将来也通过 a0 带回来。")
        self.play(R["a0"].set(3))
        self.play(arrow.animate.next_to(ma[1], LEFT, buff=0.15), R["PC"].set("0x1004"), R["a1"].set(4))
        self.play(arrow.animate.next_to(ma[2], LEFT, buff=0.15), R["PC"].set("0x1008"))
        self.say("jal 是 jump and link：先把下一条指令的地址 PC + 4 存进 ra，再跳到 sum。",
                 Circumscribe(main[2], color=YELLOW_D))
        self.play(R["ra"].set("0x100C"))
        link = SurroundingRectangle(ma[3], color=RED_B, buff=0.06)
        self.play(Create(link))
        jump = CurvedArrow(main.right_of(2, 0.2), fn.right_of(1, 0.2), angle=-TAU / 4, color=YELLOW_D)
        self.play(Create(jump), arrow.animate.next_to(fa[0], LEFT, buff=0.15), R["PC"].set("0x2000"))
        self.say("函数把结果算好放进 a0……", FadeOut(jump))
        self.play(R["a0"].set(7))
        self.play(arrow.animate.next_to(fa[1], LEFT, buff=0.15), R["PC"].set("0x2004"))
        back = CurvedArrow(fn.right_of(2, 0.2), main.right_of(3, 0.2), angle=TAU / 4, color=RED_B)
        self.say("……然后 jr ra：跳回 ra 记下的地址 0x100C，接着往下执行。",
                 Indicate(R["ra"], color=RED_B))
        self.play(Create(back), arrow.animate.next_to(ma[3], LEFT, buff=0.15), R["PC"].set("0x100C"))
        self.play(R["s0"].set(7), FadeOut(back), FadeOut(link))
        self.say("为什么不用 j 跳回去？因为 sum 可能在很多地方被调用，只有 ra 知道这一次该回到哪里。")
        ret = CodeListing(["jr ra   =   jalr x0, 0(ra)   =   ret"], font_size=28).to_edge(DOWN, buff=1.35)
        self.say("jr ra 是 jalr x0, 0(ra) 的简写，也常写成 ret。", FadeIn(ret, shift=UP * 0.15))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ convention
    def convention(self):
        caller = box_label("调用者", BLUE_C, w=3.0, h=0.8).move_to(LEFT * 4 + UP * 2.2)
        callee = box_label("被调用的函数 f", GOLD_C, w=3.6, h=0.8).move_to(RIGHT * 3.6 + UP * 2.2)
        t0 = RegBox("t0", 42, width=1.4).next_to(caller, DOWN, buff=0.6)
        note = zh("重要数据，调用后还要用", 24, GREY_A).next_to(t0, DOWN, buff=0.25)
        self.say("麻烦来了：寄存器只有一套，调用者和被调用的函数共用它们。",
                 FadeIn(caller), FadeIn(callee), FadeIn(t0), FadeIn(note))
        call = Arrow(caller.get_right(), callee.get_left(), buff=0.2, color=GREY_B)
        call_l = mono("jal f", 26, C_MNEM).next_to(call, UP, buff=0.1)
        self.play(GrowArrow(call), FadeIn(call_l))
        use = CodeListing(["addi t0, x0, 7"], font_size=28).next_to(callee, DOWN, buff=0.6)
        self.say("可 f 也要用寄存器。如果它改写了调用者还要用的值，数据就被悄悄破坏了。", FadeIn(use))
        v = mono("7", 26, RED_B).move_to(use.get_center())
        self.play(v.animate.move_to(t0.box), run_time=1.0)
        self.play(FadeOut(v), t0.set(7))
        cross = Cross(t0, stroke_color=RED_C, stroke_width=5)
        self.play(Create(cross))
        self.say("所以大家约定了一套规则，叫做调用约定（calling convention）。")
        self.hold()
        self.clear_stage()

        col1 = VGroup(
            box_label("调用者保存 caller-saved", C_T, w=5.8, h=0.8, font_size=28),
            mono("t0–t6   a0–a7   ra", 30, C_T),
            zh("函数可以随意改写。\n调用者若之后还要用，要自己先存好。", 26, GREY_A),
        ).arrange(DOWN, buff=0.4)
        col2 = VGroup(
            box_label("被调用者保存 callee-saved", C_S, w=5.8, h=0.8, font_size=28),
            mono("s0–s11   sp", 30, C_S),
            zh("函数若要使用，必须先保存旧值，\n返回前原样恢复。", 26, GREY_A),
        ).arrange(DOWN, buff=0.4)
        VGroup(col1, col2).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to(UP * 0.5)
        self.say("t、a 寄存器和 ra 是“调用者保存”的：被调用的函数可以随便改。调用者如果之后还要用，得自己先存好。",
                 FadeIn(col1, shift=UP * 0.2))
        self.say("s 寄存器和 sp 是“被调用者保存”的：函数要用，就得先存旧值，返回前原样恢复。",
                 FadeIn(col2, shift=UP * 0.2))
        self.say("换句话说：跨过一次函数调用，s 寄存器的值保证不变；t、a 寄存器则不保证。")
        self.say("那么，这些旧值要存到哪里？答案是内存里的“栈”。")
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ stack
    def stack(self):
        segs = [("栈 Stack", BLUE_C, 1.2), ("", GREY_E, 1.3), ("堆 Heap", GREEN_C, 0.9),
                ("静态数据 Static", GOLD_C, 0.7), ("代码 Text", PURPLE_B, 0.9)]
        layout = VGroup()
        for name, col, h in segs:
            r = Rectangle(width=3.6, height=h, stroke_color=GREY_B, stroke_width=2,
                          fill_color=col, fill_opacity=0.18 if name else 0.0)
            t = zh(name, 26, WHITE).move_to(r)
            layout.add(VGroup(r, t))
        layout.arrange(DOWN, buff=0).move_to(LEFT * 2.2 + UP * 0.2)
        hi = zh("高地址", 24, GREY_B).next_to(layout, RIGHT, buff=0.3).align_to(layout, UP)
        lo = zh("低地址", 24, GREY_B).next_to(layout, RIGHT, buff=0.3).align_to(layout, DOWN)
        down = Arrow(layout[0].get_bottom() + UP * 0.1, layout[0].get_bottom() + DOWN * 0.7,
                     buff=0, color=BLUE_B)
        up = Arrow(layout[2].get_top() + DOWN * 0.1, layout[2].get_top() + UP * 0.6, buff=0, color=GREEN_B)
        self.say("一个程序的内存大致分成几块：代码、静态数据、堆，以及位于高地址的栈。",
                 LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in reversed(layout)], lag_ratio=0.2),
                 FadeIn(hi), FadeIn(lo))
        sp = VGroup(Arrow(RIGHT * 1.2, ORIGIN, buff=0, color=C_SP), mono("sp", 28, C_SP))
        sp[1].next_to(sp[0], RIGHT, buff=0.1)
        sp.next_to(layout[0].get_corner(DR), RIGHT, buff=0.05)
        self.say("栈从高地址往低地址“向下”生长。sp（栈指针）指向栈顶，也就是当前用到的最低地址。",
                 GrowArrow(down), GrowArrow(up), FadeIn(sp))
        self.hold()
        self.clear_stage()

        col = WordColumn(0x1000, 5, cell_w=2.8, font_size=24).move_to(RIGHT * 3.0 + DOWN * 0.3)
        col.texts[0].become(zh("调用者的数据", 22, GREY).move_to(col.cells[0]))
        col.cells[0].set_fill(GREY_D, 0.5)
        sp_arrow = VGroup(Arrow(RIGHT * 1.0, ORIGIN, buff=0, color=C_SP), mono("sp", 28, C_SP))
        sp_arrow[1].next_to(sp_arrow[0], RIGHT, buff=0.1)
        sp_arrow.next_to(col.cells[0], RIGHT, buff=0.1)
        regs = reg_column([("sp", "0x1000"), ("ra", "0x1010"), ("s0", 42)], width=1.7, font_size=24)
        regs.to_corner(UL, buff=0.6).shift(RIGHT * 0.5)
        push = CodeListing([
            "addi sp, sp, -8   # 腾出 2 个字",
            "sw   ra, 4(sp)",
            "sw   s0, 0(sp)",
        ], font_size=26, line_gap=0.48).next_to(regs, DOWN, buff=0.6).align_to(regs, LEFT)
        self.say("放大来看。假设函数要保存 ra 和 s0 两个寄存器。",
                 FadeIn(col), FadeIn(sp_arrow), FadeIn(regs))
        self.say("压栈：先把 sp 减 8，腾出两个字的空间……", FadeIn(push, shift=UP * 0.15))
        box = push.line_box(0)
        self.play(FadeIn(box))
        self.play(regs[0].set("0xFF8"), sp_arrow.animate.next_to(col.cells[2], RIGHT, buff=0.1))
        self.say("……再用 sw 把寄存器存进去：ra 放在 sp + 4，s0 放在 sp + 0。",
                 box.animate.become(push.line_box(1)))
        v = regs[1].val.copy()
        self.play(v.animate.move_to(col.cells[1]), run_time=0.8)
        self.play(FadeOut(v), col.set(0xFFC, "ra = 0x1010", C_RA))
        self.play(box.animate.become(push.line_box(2)))
        v = regs[2].val.copy()
        self.play(v.animate.move_to(col.cells[2]), run_time=0.8)
        self.play(FadeOut(v), col.set(0xFF8, "s0 = 42", C_S))
        self.hold()

        self.say("函数现在可以放心地改 ra 和 s0 了。", regs[1].set("0x2468"), regs[2].set(-1))
        self.hold()
        pop = CodeListing([
            "lw   s0, 0(sp)",
            "lw   ra, 4(sp)",
            "addi sp, sp, 8    # 归还空间",
        ], font_size=26, line_gap=0.48).move_to(push, aligned_edge=UL)
        self.say("返回之前出栈，顺序正好反过来：用 lw 取回旧值，再把 sp 加回去。",
                 FadeOut(box), ReplacementTransform(push, pop))
        box = pop.line_box(0)
        self.play(FadeIn(box))
        v = col.texts[2].copy()
        self.play(v.animate.move_to(regs[2].box).scale(0.6), run_time=0.8)
        self.play(FadeOut(v), regs[2].set(42))
        self.play(box.animate.become(pop.line_box(1)))
        v = col.texts[1].copy()
        self.play(v.animate.move_to(regs[1].box).scale(0.6), run_time=0.8)
        self.play(FadeOut(v), regs[1].set("0x1010"))
        self.play(box.animate.become(pop.line_box(2)))
        self.play(regs[0].set("0x1000"), sp_arrow.animate.next_to(col.cells[0], RIGHT, buff=0.1))
        self.say("sp 回到原处，寄存器恢复原值。存过的数据不用清除，它们只是不再属于任何人。",
                 col.cells[1].animate.set_fill(opacity=0.05), col.cells[2].animate.set_fill(opacity=0.05),
                 col.texts[1].animate.set_opacity(0.35), col.texts[2].animate.set_opacity(0.35))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ sumSquare
    def sum_square(self):
        c = CodeListing([
            "int sumSquare(int x, int y) {",
            "    return mult(x, x) + y;",
            "}",
        ], lang="c", font_size=26, line_gap=0.42).to_corner(UL, buff=0.4)
        self.say("最后看一个完整的例子：sumSquare 会调用另一个函数 mult。", FadeIn(c, shift=RIGHT * 0.2))
        src = [
            "sumSquare:",
            "    addi sp, sp, -8    # 腾出空间",
            "    sw   ra, 4(sp)     # 保存 ra",
            "    sw   a1, 0(sp)     # 保存 y",
            "    mv   a1, a0        # a1 = x",
            "    jal  ra, mult      # ra 被覆盖！",
            "    lw   a1, 0(sp)     # 恢复 y",
            "    add  a0, a0, a1    # + y",
            "    lw   ra, 4(sp)     # 恢复 ra",
            "    addi sp, sp, 8",
            "    jr   ra",
        ]
        asm = CodeListing(src, font_size=23, line_gap=0.4).next_to(c, DOWN, buff=0.35).align_to(c, LEFT)
        asm.shift(RIGHT * 1.0)
        regs = VGroup(
            RegBox("sp", "0x1000", width=1.5, font_size=24),
            RegBox("ra", "0x1010", width=1.5, font_size=24),
            RegBox("a0", 3, width=1.5, font_size=24),
            RegBox("a1", 5, width=1.5, font_size=24),
        )
        regs.arrange_in_grid(2, 2, buff=(0.6, 0.2)).to_corner(UR, buff=0.45)
        R = dict(zip(["sp", "ra", "a0", "a1"], regs))
        col = WordColumn(0x1000, 4, cell_w=2.5, font_size=22).next_to(regs, DOWN, buff=0.6)
        col.set_x(3.6)
        col.texts[0].become(zh("调用者的数据", 20, GREY).move_to(col.cells[0]))
        col.cells[0].set_fill(GREY_D, 0.5)
        sp_arrow = VGroup(Arrow(RIGHT * 0.6, ORIGIN, buff=0, color=C_SP), mono("sp", 24, C_SP))
        sp_arrow[1].next_to(sp_arrow[0], RIGHT, buff=0.1)
        sp_arrow.next_to(col.cells[0], RIGHT, buff=0.08)
        xy = zh("x = 3，y = 5", 24, GREY_A).next_to(col, DOWN, buff=0.35)
        self.say("调用时 x = 3 在 a0，y = 5 在 a1，ra 里是调用者的返回地址。",
                 FadeIn(asm, shift=UP * 0.2), FadeIn(regs), FadeIn(col), FadeIn(sp_arrow), FadeIn(xy))
        self.say("sumSquare 自己也要 jal 调用 mult，而 jal 会覆盖 ra。不先保存 ra，就再也回不到调用者了。",
                 Circumscribe(asm[5], color=RED_B))
        self.say("y 也得存到栈上：a1 马上要用来传 x，而且 a 寄存器由调用者保存，mult 也可能改掉它。",
                 Circumscribe(asm[3], color=YELLOW_D))
        self.hold()

        box = asm.line_box(1)

        def go(i, *anims, rt=0.7):
            self.play(box.animate.become(asm.line_box(i)), *anims, run_time=rt)

        self.say("先是序言（prologue）：腾出两个字，存好 ra 和 y。", FadeIn(box))
        self.play(R["sp"].set("0xFF8"), sp_arrow.animate.next_to(col.cells[2], RIGHT, buff=0.08))
        go(2)
        self.play(col.set(0xFFC, "ra = 0x1010", C_RA))
        go(3)
        self.play(col.set(0xFF8, "y = 5", C_A))
        self.say("准备参数 mult(3, 3)，然后 jal：ra 被改成 jal 下一条指令的地址，这里是 0x2014。",
                 box.animate.become(asm.line_box(4)))
        self.play(R["a1"].set(3))
        go(5, R["ra"].set("0x2014"))
        mult = box_label("mult：a0 = 3 × 3 = 9", GREY_B, w=4.2, h=0.7, font_size=24)
        mult.next_to(xy, DOWN, buff=0.35)
        self.play(FadeIn(mult, shift=LEFT * 0.2))
        self.play(R["a0"].set(9), R["a1"].set("???"))
        self.say("mult 返回后，a1 里是什么已经说不准了——幸好 y 存在栈上。", FadeOut(mult))
        go(6, R["a1"].set(5))
        self.say("算出 9 + 5 = 14。然后是尾声（epilogue）：恢复 ra，sp 加回 8，最后 jr ra 回到调用者。",
                 box.animate.become(asm.line_box(7)))
        self.play(R["a0"].set(14))
        go(8, R["ra"].set("0x1010"))
        go(9, R["sp"].set("0x1000"), sp_arrow.animate.next_to(col.cells[0], RIGHT, buff=0.08))
        go(10)
        self.play(Circumscribe(R["a0"], color=YELLOW_D), Circumscribe(R["ra"], color=RED_B))
        self.hold()
        pro = Brace(VGroup(asm[1], asm[3]), LEFT, color=BLUE_B)
        epi = Brace(VGroup(asm[8], asm[10]), LEFT, color=BLUE_B)
        pro_l = zh("序言", 22, BLUE_B)
        epi_l = zh("尾声", 22, BLUE_B)
        if EN:  # "prologue"/"epilogue" are too wide for the left margin: run them along the braces
            pro_l.rotate(PI / 2)
            epi_l.rotate(PI / 2)
        pro_l.next_to(pro, LEFT, buff=0.1)
        epi_l.next_to(epi, LEFT, buff=0.1)
        self.say("序言保存现场，尾声恢复现场。几乎每个会调用其他函数的函数，都是这个结构。",
                 GrowFromCenter(pro), GrowFromCenter(epi), FadeIn(pro_l), FadeIn(epi_l))
        self.hold(0.5)
