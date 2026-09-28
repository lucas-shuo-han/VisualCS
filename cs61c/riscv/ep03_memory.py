import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F403

A = [5, 12, 42, 7, 100, 9]
BASE = 0x100


class Ep03Memory(NarratedScene):
    def construct(self):
        self.title_card()
        self.why_memory()
        self.byte_addressing()
        self.load_store()
        self.bytes_and_sign()
        self.end_card(
            [
                "内存按字节寻址；一个字 = 4 字节",
                "RISC-V 是小端序：低位字节放在低地址",
                "lw / sw  寄存器, 偏移(基址)：地址 = 基址 + 偏移",
                "A[i] 的字节偏移是 4 × i",
                "lb 符号扩展，lbu 零扩展",
            ],
        )

    # ------------------------------------------------------------------ why
    def why_memory(self):
        head = self.heading("内存 Memory")
        regs = box_label("寄存器 × 32", BLUE_C, w=3.2, h=2.2, font_size=30).move_to(LEFT * 3.8)
        mem = box_label("内存：数组、结构体……", GREEN_C, w=4.6, h=4.2, font_size=30).move_to(RIGHT * 3.0)
        self.say("寄存器只有 32 个，可程序里有数组、结构体，成千上万个变量。它们都放在内存里。",
                 Write(head), FadeIn(regs, shift=RIGHT * 0.2), FadeIn(mem, shift=LEFT * 0.2))
        load = Arrow(mem.get_left() + UP * 0.6, regs.get_right() + UP * 0.6, buff=0.15, color=YELLOW_D)
        store = Arrow(regs.get_right() + DOWN * 0.6, mem.get_left() + DOWN * 0.6, buff=0.15, color=TEAL_C)
        ll = zh("load 加载", 26, YELLOW_D).next_to(load, UP, buff=0.12)
        sl = zh("store 存储", 26, TEAL_C).next_to(store, DOWN, buff=0.12)
        self.say("RISC-V 是“加载-存储”架构：算术指令只能操作寄存器，访问内存必须用专门的指令。")
        self.say("load 把数据从内存搬进寄存器，store 把寄存器的值写回内存。",
                 GrowArrow(load), FadeIn(ll), GrowArrow(store), FadeIn(sl))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ bytes
    def byte_addressing(self):
        mem = MemoryView(BASE, 6, 4, cell_w=0.95, cell_h=0.52, font_size=24).move_to(DOWN * 0.3 + LEFT * 0.6)
        self.mem = mem
        self.say("可以把内存想象成一个巨大的字节数组：每个字节都有自己的编号，也就是地址。",
                 LaggedStart(*[FadeIn(VGroup(mem.cells[i], mem.texts[i]), scale=0.8)
                               for i in range(24)], lag_ratio=0.04, run_time=2))
        self.play(FadeIn(mem.addr_labels), FadeIn(mem.offsets))
        self.say("为了看得清楚，每行画 4 个字节：第一行是 0x100 到 0x103，下一行从 0x104 开始。",
                 Indicate(mem.addr_labels[0], color=YELLOW_D), Indicate(mem.offsets, color=YELLOW_D))
        self.hold()

        rows = VGroup(*[SurroundingRectangle(mem.word(BASE + 4 * r), color=BLUE_B, buff=0.03,
                                             stroke_width=2.5) for r in range(6)])
        self.say("一个字占 4 个字节，所以相邻两个字的地址相差 4，而不是 1。",
                 LaggedStart(*[Create(r) for r in rows], lag_ratio=0.15))
        self.play(LaggedStart(*[Indicate(l, color=BLUE_B) for l in mem.addr_labels], lag_ratio=0.15))
        align = zh("字地址通常是 4 的倍数\n这叫“对齐”", 26, GREY_A).next_to(mem, RIGHT, buff=0.8)
        self.say("字的地址通常是 4 的倍数，叫做“对齐”。不对齐的访问可能更慢，甚至直接出错。",
                 FadeIn(align, shift=LEFT * 0.2))
        self.hold()
        self.play(FadeOut(rows), FadeOut(align))

        # little endian
        num = mono("0x12345678", 44, WHITE).move_to(RIGHT * 4.3 + UP * 1.6)
        self.say("一个 32 位的数，怎么放进 4 个字节？比如 0x12345678。", Write(num))
        byte_cols = [RED_B, GOLD_B, GREEN_B, BLUE_B]
        pieces = VGroup(*[mono(f"{b:02X}", 40, c) for b, c in zip([0x12, 0x34, 0x56, 0x78], byte_cols)])
        pieces.arrange(RIGHT, buff=0.35).move_to(num)
        self.play(ReplacementTransform(num, pieces))
        hi = zh("高位", 22, GREY_B).next_to(pieces[0], DOWN, buff=0.2)
        lo = zh("低位", 22, GREY_B).next_to(pieces[3], DOWN, buff=0.2)
        self.play(FadeIn(hi), FadeIn(lo))
        self.say("RISC-V 采用小端序（little-endian）：最低位的字节放在最小的地址。")
        targets = []
        for k in range(4):
            t = mono(f"{[0x78, 0x56, 0x34, 0x12][k]:02X}", mem.font_size, byte_cols[3 - k]).move_to(mem.cell(BASE + k))
            targets.append(t)
        self.play(FadeOut(hi), FadeOut(lo), FadeOut(mem.word_texts(BASE)))
        self.play(LaggedStart(*[
            ReplacementTransform(pieces[3 - k], targets[k]) for k in range(4)
        ], lag_ratio=0.35, run_time=2.4))
        self.say("所以从 0x100 往后看，依次是 78、56、34、12，像是“倒着”存的。",
                 *[Indicate(t, scale_factor=1.4) for t in targets])
        self.say("好在按字读写时，硬件会自动拼回原来的数，大多数时候你不用操心字节顺序。")
        self.hold()
        # replace the demo bytes with the placeholders so the view is consistent
        for k in range(4):
            self.mem.texts[k].become(targets[k])
            self.remove(targets[k])
        self.add(self.mem)

    # ------------------------------------------------------------------ lw / sw
    def load_store(self):
        mem = self.mem
        self.play(mem.animate.move_to(DOWN * 0.85 + LEFT * 0.4))
        anims = []
        for i, v in enumerate(A):
            anims.append(mem.set_word(BASE + 4 * i, v))
        labels = VGroup(*[
            mono(f"A[{i}] = {v}", 24, C_NUM).next_to(mem.cells[4 * i + 3], RIGHT, buff=0.35)
            for i, v in enumerate(A)
        ])
        self.say("现在假设内存里有一个 int 数组 A：从地址 0x100 开始，每个元素占一个字。",
                 *anims, LaggedStart(*[FadeIn(l, shift=LEFT * 0.2) for l in labels], lag_ratio=0.1))
        self.hold()

        regs = reg_column([("s0", "0x100"), ("t0", 0)], width=1.6).move_to(LEFT * 5.5 + DOWN * 0.3)
        self.say("数组的起始地址，也叫基地址，放在 s0 里。", FadeIn(regs, shift=RIGHT * 0.2))

        code = CodeListing(["lw t0, 8(s0)"], font_size=40).move_to(UP * 2.55)
        self.say("lw 是 load word。lw t0, 8(s0)：从地址 s0 + 8 读一个字，放进 t0。",
                 FadeIn(code, shift=DOWN * 0.2))
        self.play(Circumscribe(code.glyphs(0, "8(s0)"), color=YELLOW_D))
        calc = mono("0x100 + 8 = 0x108", 28, YELLOW_D).next_to(code, DOWN, buff=0.3)
        row = SurroundingRectangle(mem.word(BASE + 8), color=YELLOW_D, buff=0.04)
        self.say("偏移量 8 加上基地址，得到 0x108，正是 A[2] 所在的位置。",
                 TransformFromCopy(code.glyphs(0, "8(s0)"), calc))
        self.play(Create(row), Indicate(mem.row_label(BASE + 8), color=YELLOW_D), Indicate(labels[2]))
        flying = mem.word_texts(BASE + 8).copy()
        self.play(flying.animate.arrange(RIGHT, buff=0.1).move_to(regs[1].box).scale(0.8), run_time=1.2)
        self.play(FadeOut(flying), regs[1].set(42))
        self.hold()

        self.play(FadeOut(calc), FadeOut(row))
        c2 = CodeListing(["x = A[3];"], lang="c", font_size=34)
        a2 = CodeListing(["lw t0, 12(s0)"], font_size=34)
        pair = VGroup(c2, mono("→", 34, GREY_B), a2).arrange(RIGHT, buff=0.5).move_to(UP * 2.55)
        self.say("所以 C 里的 A[i]，对应的字节偏移是 4 × i。",
                 FadeOut(code), FadeIn(pair, shift=DOWN * 0.2))
        warn = zh("偏移是 12，不是 3！", 28, RED_B).next_to(pair, DOWN, buff=0.3)
        self.say("比如 A[3] 的偏移是 12，而不是 3。这是写汇编时最常见的错误之一。",
                 Circumscribe(a2.glyphs(0, "12"), color=RED_B), FadeIn(warn))
        self.hold()
        self.play(FadeOut(pair), FadeOut(warn))

        # full example: A[3] = h + A[1]
        c3 = CodeListing(["A[3] = h + A[1];"], lang="c", font_size=34).move_to(UP * 3.1 + LEFT * 3.7)
        asm = CodeListing([
            "lw  t0, 4(s0)     # t0 = A[1]",
            "add t0, s1, t0    # t0 = h + A[1]",
            "sw  t0, 12(s0)    # A[3] = t0",
        ], font_size=26, line_gap=0.44).next_to(c3, RIGHT, buff=0.7).align_to(c3, UP)
        h = RegBox("s1", 10, width=1.6).next_to(regs, DOWN, buff=0.22)
        h.shift(RIGHT * (regs[0].box.get_center()[0] - h.box.get_center()[0]))
        hl = zh("h", 24, GREY_A).next_to(h, RIGHT, buff=0.15)
        self.say("sw 是 store word，方向相反：把寄存器的值写进内存。来看一个完整的例子。",
                 FadeIn(c3, shift=DOWN * 0.2), FadeIn(h), FadeIn(hl), regs[1].set(0))
        self.say("A[3] = h + A[1]，其中 h 在 s1 里。先把 A[1] 读进来……", FadeIn(asm, shift=DOWN * 0.2))
        cur = asm.line_box(0)
        self.play(FadeIn(cur))
        row = SurroundingRectangle(mem.word(BASE + 4), color=YELLOW_D, buff=0.04)
        self.play(Create(row))
        flying = mem.word_texts(BASE + 4).copy()
        self.play(flying.animate.arrange(RIGHT, buff=0.1).move_to(regs[1].box).scale(0.8), run_time=1.0)
        self.play(FadeOut(flying), FadeOut(row), regs[1].set(12))
        self.say("……再加上 h：t0 = 10 + 12 = 22……", cur.animate.become(asm.line_box(1)))
        self.play(Indicate(h), Indicate(regs[1]))
        self.play(regs[1].set(22))
        note = zh("注意：sw 的源寄存器写在前面", 24, TEAL_C).next_to(asm, DOWN, buff=0.25).align_to(asm, LEFT)
        self.say("……最后用 sw 写回 A[3]。注意 sw 把源寄存器写在前面，内存地址写在后面。",
                 cur.animate.become(asm.line_box(2)), FadeIn(note))
        row = SurroundingRectangle(mem.word(BASE + 12), color=TEAL_C, buff=0.04)
        self.play(Create(row))
        v = regs[1].val.copy()
        self.play(v.animate.move_to(row.get_center()), run_time=1.0)
        new_lab = mono("A[3] = 22", 24, C_NUM).move_to(labels[3], aligned_edge=LEFT)
        self.play(FadeOut(v), mem.set_word(BASE + 12, 22), Transform(labels[3], new_lab))
        self.say("22 的十六进制是 0x16，按小端序存进 0x10C：16 00 00 00。",
                 Indicate(mem.word_texts(BASE + 12), color=TEAL_C, scale_factor=1.3))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ bytes, sign extension
    def bytes_and_sign(self):
        head = self.heading("字节读写：lb / lbu / sb")
        self.say("除了整个字，也可以只读写一个字节：lb、lbu 和 sb。", Write(head))
        cell = VGroup(
            Rectangle(width=1.2, height=0.7, stroke_color=GREY_B, fill_color=GREY_E, fill_opacity=0.3),
        )
        byte_txt = mono("F3", 34, YELLOW_D).move_to(cell)
        addr = mono("0x200", 24, GREY_B).next_to(cell, LEFT, buff=0.25)
        byte = VGroup(cell, byte_txt, addr).move_to(UP * 2.2 + LEFT * 3.2)
        mem_lab = zh("内存中的一个字节", 24, GREY_A).next_to(byte, RIGHT, buff=0.4)
        self.play(FadeIn(byte), FadeIn(mem_lab))

        bf = BitField([("扩展出来的 24 位", 24, GREY_B), ("读入的字节", 8, YELLOW_D)],
                      box_w=0.36, show_ranges=False).move_to(DOWN * 0.3)
        reg_lab = mono("t0", 28, C_T).next_to(bf.frames, LEFT, buff=0.3)
        self.say("lb 把这个字节读进 32 位的寄存器。那多出来的 24 位，要填什么？",
                 FadeIn(bf.frames), FadeIn(bf.labels), FadeIn(reg_lab))
        self.play(bf.fill_field(1, "11110011"))
        sign = bf.field_digits[1][0]
        mark = SurroundingRectangle(sign, color=RED_B, buff=0.05)
        self.say("lb 做“符号扩展”：把最高位（符号位）复制到所有高位。0xF3 的最高位是 1……",
                 Create(mark))
        ones = VGroup(*[mono("1", 22, RED_B).move_to(d) for d in bf.field_digits[0]])
        self.play(LaggedStart(*[TransformFromCopy(sign, o) for o in reversed(ones)],
                              lag_ratio=0.06, run_time=2.2))
        val = mono("= 0xFFFFFFF3 = −13", 32, RED_B).next_to(bf, DOWN, buff=0.45)
        self.say("……于是高 24 位全是 1，结果是 0xFFFFFFF3，也就是 −13。有符号的值保持不变。",
                 Write(val))
        self.hold()
        zeros = VGroup(*[mono("0", 22, BLUE_B).move_to(d) for d in bf.field_digits[0]])
        val2 = mono("= 0x000000F3 = 243", 32, BLUE_B).move_to(val)
        self.say("lbu 是无符号版本：高位一律填 0，结果是 243。",
                 FadeOut(mark),
                 LaggedStart(*[Transform(o, z) for o, z in zip(ones, zeros)], lag_ratio=0.03),
                 Transform(val, val2))
        self.hold()
        sb = zh("sb：只把寄存器最低的 8 位写入内存，其余 24 位被忽略", 26, GREY_A)
        sb.next_to(val, DOWN, buff=0.4)
        self.say("sb 则只把寄存器最低的 8 位写进内存，高 24 位直接忽略。",
                 FadeIn(sb), Indicate(bf.frames[1], color=YELLOW_D))
        self.hold()
        self.clear_stage()

        tbl = VGroup(
            VGroup(zh("宽度", 26, GREY_B), zh("有符号", 26, GREY_B), zh("无符号", 26, GREY_B), zh("写入", 26, GREY_B)),
            VGroup(zh("字节 8 位", 26), mono("lb", 28, C_MNEM), mono("lbu", 28, C_MNEM), mono("sb", 28, C_MNEM)),
            VGroup(zh("半字 16 位", 26), mono("lh", 28, C_MNEM), mono("lhu", 28, C_MNEM), mono("sh", 28, C_MNEM)),
            VGroup(zh("字 32 位", 26), mono("lw", 28, C_MNEM), mono("—", 28, GREY), mono("sw", 28, C_MNEM)),
        )
        for row in tbl:
            for k, m in enumerate(row):
                m.move_to([-3.6 + k * 2.6, 0, 0])
        tbl.arrange(DOWN, buff=0.45).move_to(UP * 0.3)
        for row in tbl:
            for k, m in enumerate(row):
                m.set_x(-3.6 + k * 2.6)
        line = Line(LEFT * 5, RIGHT * 5, stroke_color=GREY, stroke_width=1.5).next_to(tbl[0], DOWN, buff=0.2)
        self.say("半字（16 位）也是同样的规则：lh、lhu、sh。",
                 FadeIn(tbl[0]), Create(line),
                 LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in tbl[1:]], lag_ratio=0.3))
        self.say("在 RV32 里，lw 已经读满 32 位，不需要扩展，所以没有 lwu。",
                 Indicate(tbl[3][2], color=YELLOW_D))
        self.hold(0.5)
