import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F403


# ---------------------------------------------------------------- checked values
M32 = 0xFFFFFFFF


def enc_r(f7, rs2, rs1, f3, rd, op):
    return (f7 << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op


def enc_i(imm, rs1, f3, rd, op):
    return ((imm & 0xFFF) << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op


def enc_u(imm20, rd, op):
    return (imm20 << 12) | (rd << 7) | op


def signed32(v):
    return v - (1 << 32) if v >> 31 else v


# The practice program as it sits in memory. 0x34FF does not fit in a 12-bit
# immediate, so `li x10 0x34FF` becomes lui + addi and slli lands at 0x08.
PROG = [
    enc_u(0x3, 10, 0b0110111),                  # 0x00  lui  x10 0x3
    enc_i(0x4FF, 10, 0b000, 10, 0b0010011),     # 0x04  addi x10 x10 0x4FF
    enc_i(0x10, 10, 0b001, 12, 0b0010011),      # 0x08  slli x12 x10 0x10
    enc_i(0x08, 12, 0b101, 12, 0b0010011),      # 0x0C  srli x12 x12 0x08
    enc_r(0, 10, 12, 0b111, 12, 0b0110011),     # 0x10  and  x12 x12 x10
]
assert PROG == [0x00003537, 0x4FF50513, 0x01051613, 0x00865613, 0x00A67633]
assert PROG[2] == 0x01051613                    # the notes' example word
assert 0x34FF > 2047 and (0x3 << 12) + 0x4FF == 0x34FF

X10 = 0x000034FF
SLLI = (X10 << 0x10) & M32
SRLI = SLLI >> 0x08
AND = SRLI & X10
assert (SLLI, SRLI, AND) == (0x34FF0000, 0x0034FF00, 0x00003400)
assert SLLI >> 31 == 0                           # srai would give the same result
BOTH_ONE = [k for k in range(32) if (SRLI >> (31 - k)) & 1 and (X10 >> (31 - k)) & 1]
assert BOTH_ONE == [18, 19, 21]                  # bit columns (MSB = 0) kept by the and

# slt vs sltu on the same bits
A, B = 0xFFFFFFFF, 1
assert signed32(A) == -1 and A == 4294967295
assert int(signed32(A) < signed32(B)) == 1 and int(A < B) == 0      # slt / sltu
assert int(signed32(A) < 10) == 1 and int(A < 10) == 0              # slti / sltiu 10
assert int(3 < 5) == 1

# the pointer-style loop: 1..20 as in the notes' Venus demo
assert sum(range(1, 21)) == 210
EP05_BODY = ["bge", "slli", "add", "lw", "add", "addi", "j"]
NOTES_BODY = ["bge", "lw", "add", "addi", "addi", "j"]
assert len(EP05_BODY) - len(NOTES_BODY) == 1

HEX_Y = 0.27   # distance from a bit row's centre to its hex digits


class Word32(VGroup):
    """32 bit cells in nibble groups, with the hex digit under each nibble."""

    def __init__(self, value, color=BLUE_B, box=0.3, gap=0.09, font_size=18, hex_size=22, **kw):
        super().__init__(**kw)
        self.box, self.font_size, self.hex_size = box, font_size, hex_size
        self.value = value
        self.cells = VGroup()
        for k in range(32):
            sq = Square(box, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=0.12)
            sq.move_to(RIGHT * (k * box + (k // 4) * gap))
            self.cells.add(sq)
        self.digits = VGroup(*[self._dig(ch).move_to(self.cells[k])
                               for k, ch in enumerate(format(value, "032b"))])
        self.hexes = self._hexes(value)
        self.prefix = mono("0x", hex_size, YELLOW_D).next_to(self.hexes[0], LEFT, buff=0.12)
        self.add(self.cells, self.digits, self.hexes, self.prefix)

    def _dig(self, ch):
        return mono(ch, self.font_size, WHITE if ch == "1" else GREY_B)

    def nibble(self, k):
        return VGroup(*self.cells[4 * k:4 * k + 4])

    def _hexes(self, value):
        y = self.cells.get_center()[1] - self.box / 2 - HEX_Y
        return VGroup(*[mono(h, self.hex_size, YELLOW_D).move_to([self.nibble(k).get_center()[0], y, 0])
                        for k, h in enumerate(f"{value:08X}")])

    def place(self, x, y):
        self.shift(np.array([x, y, 0]) - self.cells.get_center())
        return self

    def shift_bits(self, scene, k, value):
        """Animate a shift by k places (k > 0: left), filling with zeros."""
        old = list(self.digits)
        new = [None] * 32
        moves, drops = [], []
        for i, d in enumerate(old):
            j = i - k
            if 0 <= j < 32:
                moves.append(d.animate.move_to(self.cells[j]))
                new[j] = d
            else:
                drops.append(d)
        away = LEFT if k > 0 else RIGHT
        scene.play(*[d.animate.shift(away * 0.35).set_opacity(0) for d in drops], run_time=0.5)
        self.digits.remove(*drops)
        scene.play(*moves, run_time=1.1)
        fills = []
        for j in range(32):
            if new[j] is None:
                z = self._dig("0").move_to(self.cells[j]).set_opacity(0)
                new[j] = z
                fills.append(z)
        self.digits.add(*fills)
        scene.play(*[z.animate.set_opacity(1) for z in fills],
                   Transform(self.hexes, self._hexes(value)), run_time=0.7)
        self.digits.submobjects = new
        self.value = value


def vdots(color=GREY_B):
    return VGroup(*[Dot(radius=0.028, color=color) for _ in range(3)]).arrange(DOWN, buff=0.06)


def tint(listing, words, color=C_KEYWORD):
    """Color whole-word occurrences of `words` in a CodeListing."""
    for i, s in enumerate(listing.src):
        for w in words:
            start, occ = 0, 0
            while (idx := s.find(w, start)) >= 0:
                before = s[idx - 1] if idx > 0 else " "
                end = idx + len(w)
                after = s[end] if end < len(s) else " "
                if not (before.isalnum() or before == "_") and not (after.isalnum() or after == "_"):
                    listing.glyphs(i, w, occ).set_color(color)
                occ += 1
                start = idx + 1
    return listing


class Ep06ControlPatterns(NarratedScene):
    def construct(self):
        self.title_card()
        self.fetch_execute()
        self.practice()
        self.set_less_than()
        self.if_without_else()
        self.goto_patterns()
        self.pointer_loop()
        self.end_card(
            [
                "控制单元的循环：读 PC → 取指令 → 执行 → 更新 PC",
                "slt、sltu、slti、sltiu：比较结果写成 1 或 0",
                "比特没有类型：有符号还是无符号，由指令决定",
                "没有 else 的 if：条件取反，直接跳过，指令更少",
                "任何循环都能先改写成 goto，再换成分支和 j",
            ],
        )

    # ------------------------------------------------------------------ fetch / execute
    def fetch_execute(self):
        mem = VGroup()
        for k, w in enumerate(PROG):
            r = Rectangle(width=2.5, height=0.6, stroke_color=GREY_B, stroke_width=1.5,
                          fill_color=GREY_E, fill_opacity=0.3).move_to(DOWN * 0.6 * k)
            t = mono(hex32(w), 22).move_to(r)
            a = mono(f"0x{4 * k:08X}", 20, GREY_B).next_to(r, LEFT, buff=0.2)
            mem.add(VGroup(r, t, a))
        mem.shift(np.array([5.4, 1.55, 0]) - mem[0][0].get_center())
        cells = VGroup(*[m[0] for m in mem])
        mem_l = zh("内存", 26, GREY_A).next_to(cells, UP, buff=0.25)
        mem_n = zh("每条指令占 4 个字节", 22, GREY_B).next_to(cells, DOWN, buff=0.3)
        self.say("程序运行前先被装进内存的代码段（text segment）：每条指令是一个 32 位的字，占 4 个字节，一条挨着一条。",
                 FadeIn(mem_l), LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in mem], lag_ratio=0.15))
        self.play(FadeIn(mem_n))

        cpu = RoundedRectangle(corner_radius=0.15, width=8.3, height=5.0, stroke_color=GREY_B,
                               stroke_width=2).move_to([-2.5, 0.25, 0])
        cpu_l = zh("处理器", 24, GREY_A).next_to(cpu.get_corner(UL), DR, buff=0.14)
        cu = RoundedRectangle(corner_radius=0.1, width=3.2, height=1.75, stroke_color=BLUE_C,
                              fill_color=BLUE_C, fill_opacity=0.08).move_to([-4.85, 1.3, 0])
        cu_l = zh("控制单元", 22, BLUE_B).next_to(cu.get_top(), DOWN, buff=0.12)
        dp = RoundedRectangle(corner_radius=0.1, width=4.3, height=4.6, stroke_color=GREEN_C,
                              fill_color=GREEN_C, fill_opacity=0.05).move_to([-0.75, 0.2, 0])
        dp_l = zh("数据通路", 22, GREEN_B).next_to(dp.get_top(), DOWN, buff=0.12)
        rf = RoundedRectangle(corner_radius=0.08, width=3.9, height=2.6, stroke_color=GREY_B,
                              stroke_width=1.5).move_to([-0.75, 0.6, 0])
        rf_l = zh("32 个寄存器 x0–x31", 20, GREY_A).next_to(rf.get_top(), DOWN, buff=0.1)
        x10 = RegBox("x10", X10, color=BLUE_B, width=2.0, fmt="hex", font_size=20)
        x12 = RegBox("x12", 0, color=BLUE_B, width=2.0, fmt="hex", font_size=20)
        x10.shift(np.array([-0.35, 0.72, 0]) - x10.box.get_center())
        x12.shift(np.array([-0.35, 0.1, 0]) - x12.box.get_center())
        dots = VGroup(vdots().next_to(x10.box, UP, buff=0.08), vdots().next_to(x12.box, DOWN, buff=0.08))
        self.say("处理器由控制单元（control unit）和数据通路（datapath）组成。数据通路里有 32 个寄存器 x0–x31。",
                 Create(cpu), FadeIn(cpu_l), FadeIn(cu), FadeIn(cu_l), FadeIn(dp), FadeIn(dp_l),
                 FadeIn(rf), FadeIn(rf_l), FadeIn(x10), FadeIn(x12), FadeIn(dots))

        pc = RegBox("PC", 8, color=YELLOW_D, width=2.0, fmt="hex", font_size=20)
        pc.shift(np.array([-0.35, -1.25, 0]) - pc.box.get_center())
        pc_n = zh("单独的寄存器，不属于 x0–x31", 18, YELLOW_D).next_to(pc, DOWN, buff=0.2)
        pc_n.set_x(dp.get_center()[0])
        self.say("PC 也在数据通路里，存着当前指令的地址。它也是寄存器，但不属于 x0–x31，指令一般不会直接读写它。",
                 FadeIn(pc, shift=UP * 0.15), FadeIn(pc_n))

        names = ["读 PC", "从内存取指令", "执行指令", "更新 PC"]
        steps = VGroup(*[
            VGroup(mono(str(k + 1), 22, YELLOW_D), zh(s, 22)).arrange(RIGHT, buff=0.22)
            for k, s in enumerate(names)
        ]).arrange(DOWN, buff=0.17, aligned_edge=LEFT)
        steps.next_to(cu, DOWN, buff=0.3).align_to(cu, LEFT).shift(RIGHT * 0.12)
        self.say("控制单元不停地重复四步：读 PC，从内存取出指令，执行，再更新 PC。",
                 LaggedStart(*[FadeIn(s, shift=RIGHT * 0.15) for s in steps], lag_ratio=0.3))
        self.hold()

        def mark(k):
            return SurroundingRectangle(steps[k], color=YELLOW_D, buff=0.07, stroke_width=0,
                                        fill_color=YELLOW_D, fill_opacity=0.18)

        hl = mark(0)
        arrow = Arrow(pc.box.get_right(), mem[2][2].get_left(), buff=0.1, color=YELLOW_D,
                      stroke_width=4, max_tip_length_to_length_ratio=0.08)
        cur = SurroundingRectangle(mem[2][0], color=YELLOW_D, buff=0.04)
        self.say("用课程笔记里的例子走一遍。第一步：读 PC，得到 0x00000008。",
                 FadeIn(hl), Indicate(pc.box, color=YELLOW_D))
        self.play(GrowArrow(arrow), Create(cur))

        word = mem[2][1].copy()
        self.say("第二步：到内存里这个地址取出指令。在内存里，它只是一个 32 位的数：0x01051613。",
                 hl.animate.become(mark(1)))
        self.play(word.animate.move_to(cu.get_center() + UP * 0.05), run_time=1.2)
        asm = CodeListing(["slli x12 x10 0x10"], font_size=20)
        asm.move_to(cu.get_center() + DOWN * 0.5)
        self.say("控制单元把它解读成 slli x12 x10 0x10。这一集沿用笔记的写法，操作数之间不写逗号。编码细节留到第 9 集。",
                 FadeIn(asm, shift=DOWN * 0.1))
        self.hold()

        self.say("第三步：执行。x10 是 0x000034FF，左移 0x10 位（也就是 16 位），x12 变成 0x34FF0000。",
                 hl.animate.become(mark(2)), Indicate(x10.box, color=BLUE_B))
        self.play(x12.set(SLLI))
        self.hold()

        plus4 = mono("PC + 4", 20, GREY_A).next_to(steps[3], RIGHT, buff=0.35)
        new_arrow = Arrow(pc.box.get_right(), mem[3][2].get_left(), buff=0.1, color=YELLOW_D,
                          stroke_width=4, max_tip_length_to_length_ratio=0.08)
        self.say("第四步：更新 PC。每条指令占 4 个字节，所以默认让 PC 加 4，变成 0x0000000C，指向下一条指令。",
                 hl.animate.become(mark(3)), FadeIn(plus4))
        self.play(pc.set(12), Transform(arrow, new_arrow), cur.animate.move_to(mem[3][0]))
        self.say("所以这条算术指令其实改了两个寄存器：目的寄存器 x12，以及 PC。",
                 Circumscribe(x12.box, color=BLUE_B), Circumscribe(pc.box, color=YELLOW_D))
        alt = zh("分支、跳转：换成标签地址", 18, C_LABEL).next_to(steps[3], DOWN, buff=0.16)
        alt.align_to(steps[3][0], LEFT)
        self.say("分支和跳转则会在第四步把 PC 换成标签的地址（条件分支只在条件成立时才换）。",
                 FadeIn(alt, shift=UP * 0.1))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ practice
    def practice(self):
        src = [
            "li    x10 0x34FF",
            "slli  x12 x10 0x10",
            "srli  x12 x12 0x08",
            "and   x12 x12 x10",
        ]
        code = CodeListing(src, font_size=24, line_gap=0.44)
        code.move_to([-5.5, 3.35, 0], aligned_edge=UL)
        addrs = VGroup(*[mono(a, 20, GREY).next_to(code.left_of(i, 0.3), LEFT, buff=0)
                         for i, a in enumerate(["0x00", "0x08", "0x0C", "0x10"])])
        self.say("内存里那 5 个字，写成汇编是这 4 行。它们正好是笔记里的一道练习题。",
                 FadeIn(code, shift=UP * 0.2), FadeIn(addrs))
        li_n = zh("伪指令：展开成 2 条，占 0x00 和 0x04", 20, GREY_B).next_to(code.right_of(0, 0.4), RIGHT, buff=0)
        self.say("li 要装的 0x34FF 超出了 12 位立即数的范围，会展开成两条指令（第 12 集细讲），所以 slli 在 0x08。",
                 FadeIn(li_n), Indicate(addrs[1], color=YELLOW_D))
        self.hold()

        opts = VGroup(*[mono(o, 24) for o in
                        ["A. 0x0", "B. 0x3400", "C. 0x4F0", "D. 0xFF00", "E. 0x34FF", "F. 其他"]])
        opts.arrange_in_grid(2, 3, buff=(0.5, 0.3), col_alignments="lll")
        opts.move_to([3.6, 2.95, 0])
        self.say("问题：这 4 行执行完，x12 里是什么？先暂停，自己想一想。",
                 FadeOut(li_n), LaggedStart(*[FadeIn(o, shift=DOWN * 0.1) for o in opts], lag_ratio=0.1))
        self.hold(2.5)

        box = code.line_box(0)
        r10 = Word32(X10, BLUE_B).place(0.5, 1.0)
        l10 = mono("x10", 26, C_REG).next_to(r10.cells, LEFT, buff=0.4)
        self.say("第一条执行完，x10 = 0x000034FF。把 32 位全画出来，每 4 位对应一个十六进制数字。",
                 FadeIn(box), FadeIn(r10), FadeIn(l10))
        self.play(LaggedStart(*[Indicate(r10.nibble(k), scale_factor=1.05) for k in (4, 5, 6, 7)],
                              lag_ratio=0.25), run_time=1.4)
        self.hold()

        r12 = Word32(X10, TEAL_C).place(0.5, -0.25)
        l12 = mono("x12", 26, C_REG).next_to(r12.cells, LEFT, buff=0.4)
        self.say("slli 左移 16 位，右边补 0：x12 = 0x34FF0000，和刚才处理器里算的一样。",
                 box.animate.become(code.line_box(1)), TransformFromCopy(r10, r12), FadeIn(l12))
        r12.shift_bits(self, 16, SLLI)
        self.hold()

        self.say("srli 右移 8 位，左边补 0：x12 = 0x0034FF00。最高位本来是 0，所以用 srai 也一样。",
                 box.animate.become(code.line_box(2)), Circumscribe(r12.cells[0], color=YELLOW_D))
        r12.shift_bits(self, -8, SRLI)
        self.hold()

        res = Word32(AND, GREEN_C).place(0.5, -1.5)
        for d in res.digits:
            d.set_opacity(0)
        res_hex = VGroup(res.hexes, res.prefix)
        res_hex.set_opacity(0)
        line = Line(res.cells.get_left() + LEFT * 0.15, res.cells.get_right() + RIGHT * 0.15,
                    stroke_color=GREY_B).move_to([res.cells.get_center()[0], -0.98, 0])
        op = mono("and", 26, C_MNEM).next_to(res.cells, LEFT, buff=0.4)
        cols = VGroup(*[
            Rectangle(width=r10.box, height=r10.cells[k].get_top()[1] - res.cells[k].get_bottom()[1] + 0.08,
                      stroke_width=0, fill_color=YELLOW_D, fill_opacity=0.22)
            .move_to([r10.cells[k].get_center()[0],
                      (r10.cells[k].get_top()[1] + res.cells[k].get_bottom()[1]) / 2, 0])
            for k in BOTH_ONE
        ])
        self.say("最后 and 逐位相与：同一位上两个都是 1，结果才是 1。",
                 box.animate.become(code.line_box(3)), Create(line), FadeIn(op), FadeIn(res.cells))
        self.play(LaggedStart(*[d.animate.set_opacity(1) for d in res.digits], lag_ratio=0.03), run_time=1.6)
        self.play(FadeIn(cols))
        self.say("只有 3 列上下都是 1，所以 x12 = 0x00003400，答案是 B。",
                 res_hex.animate.set_opacity(1), Create(SurroundingRectangle(opts[1], color=GREEN_C, buff=0.1)))
        self.play(Circumscribe(res_hex, color=GREEN_C))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ slt family
    def set_less_than(self):
        head = self.heading("比较指令：slt 家族")
        c = CodeListing(["int lt = (a < b);"], lang="c", font_size=30).move_to([-3.0, 2.0, 0])
        self.say("分支指令比较完就跳转。但有时我们只想要比较的结果，比如 C 里的 lt = (a < b)：成立是 1，不成立是 0。",
                 Write(head), FadeIn(c, shift=RIGHT * 0.2))
        syn = CodeListing(["slt rd rs1 rs2"], font_size=32).move_to([-3.0, 0.9, 0])
        mean = mono("rd = (rs1 < rs2) ? 1 : 0", 26, GREY_A).next_to(syn, DOWN, buff=0.3)
        self.say("对应的指令是 slt（set less than）：rs1 < rs2 时把 rd 置为 1，否则置为 0。",
                 FadeIn(syn, shift=UP * 0.15), FadeIn(mean))
        regs = reg_column([("x5", 3), ("x6", 5), ("x7", 0)], width=2.4, font_size=24, color=BLUE_B)
        regs.move_to([4.35, 1.3, 0])
        names = VGroup(*[mono(s, 24, GREY_B).next_to(r, RIGHT, buff=0.2)
                         for s, r in zip(["a", "b", "lt"], regs)])
        ex = CodeListing(["slt x7 x5 x6"], font_size=32).move_to([-3.0, -0.8, 0])
        self.say("a、b 放在 x5、x6，结果放进 x7：slt x7 x5 x6。3 < 5 成立，x7 = 1。",
                 FadeIn(regs), FadeIn(names), FadeIn(ex, shift=UP * 0.15))
        self.play(regs[2].set(1))
        self.hold()

        self.say("sltu 是它的无符号版本（u 代表 unsigned）。两者什么时候结果不同？看一个例子。",
                 FadeOut(VGroup(c, syn, mean, ex)), regs[0].set("0xFFFFFFFF"), regs[1].set(1),
                 regs[2].set("?"))
        bits = mono("1111 1111 1111 1111 1111 1111 1111 1111", 20).move_to([-2.3, 1.6, 0])
        bl = mono("x5", 24, C_REG).next_to(bits, LEFT, buff=0.3)
        sgn = zh("当作有符号数：−1", 26, GREEN_C).next_to(bits, DOWN, buff=0.4).align_to(bits, LEFT)
        uns = zh("当作无符号数：4294967295", 26, TEAL_C).next_to(sgn, DOWN, buff=0.25).align_to(bits, LEFT)
        self.say("x5 = 0xFFFFFFFF，32 位全是 1。当作有符号数，它是 −1；当作无符号数，它是 4294967295。",
                 FadeIn(bits), FadeIn(bl))
        self.play(FadeIn(sgn, shift=UP * 0.1))
        self.play(FadeIn(uns, shift=UP * 0.1))
        self.hold()

        pair = CodeListing([
            "slt  x7 x5 x6    # -1 < 1 成立：x7 = 1",
            "sltu x7 x5 x6    # 4294967295 < 1 不成立：x7 = 0",
        ], font_size=24, line_gap=0.55).next_to(uns, DOWN, buff=0.6).align_to(bits, LEFT)
        self.say("slt 比的是 −1 < 1，成立，得 1；sltu 比的是 4294967295 < 1，不成立，得 0。",
                 FadeIn(pair[0], shift=UP * 0.1), regs[2].set(1))
        self.play(FadeIn(pair[1], shift=UP * 0.1), regs[2].set(0))
        self.hold()
        self.say("在 C 里，类型由变量的声明决定；在汇编里，比特本身没有类型，当有符号数还是无符号数，由指令决定。",
                 Indicate(bits, color=YELLOW_D, scale_factor=1.05))
        self.hold()

        imm = CodeListing([
            "slti  x7 x5 10    # -1 < 10 成立：x7 = 1",
            "sltiu x7 x5 10    # 4294967295 < 10 不成立：x7 = 0",
        ], font_size=24, line_gap=0.55).move_to(pair, aligned_edge=UL)
        self.say("立即数版本 slti 和 sltiu 拿寄存器和常数比较。x5 不变：slti x7 x5 10 得 1，sltiu 得 0。",
                 FadeOut(pair, shift=UP * 0.1), FadeIn(imm, shift=UP * 0.1))
        self.hold()
        self.clear_stage()

        base = RoundedRectangle(corner_radius=0.12, width=6.4, height=3.3, stroke_color=BLUE_C,
                                fill_color=BLUE_C, fill_opacity=0.08).move_to([-2.8, 0.3, 0])
        base_l = zh("RV32I 基础指令集", 28, BLUE_B).next_to(base.get_top(), DOWN, buff=0.2)
        base_c = VGroup(*[mono(s, 24, C_MNEM) for s in [
            "add  sub  and  or  xor",
            "sll  srl  sra  slt  sltu",
            "lw  sw  beq  bne  jal  …",
        ]]).arrange(DOWN, buff=0.28).next_to(base_l, DOWN, buff=0.35)
        mx = RoundedRectangle(corner_radius=0.12, width=5.0, height=1.75, stroke_color=GOLD_C,
                              fill_color=GOLD_C, fill_opacity=0.08).move_to([3.75, 1.1, 0])
        mx_l = zh("M 扩展：乘法与除法", 26, GOLD_B).next_to(mx.get_top(), DOWN, buff=0.18)
        mx_c = CodeListing(["mul t0, s0, s0"], font_size=24).next_to(mx_l, DOWN, buff=0.3)
        fx = RoundedRectangle(corner_radius=0.12, width=5.0, height=1.1, stroke_color=TEAL_C,
                              fill_color=TEAL_C, fill_opacity=0.08).move_to([3.75, -0.75, 0])
        fx_l = zh("F 扩展：浮点运算", 26, TEAL_B).move_to(fx)
        self.say("顺便一提：乘法 mul 不在 RV32I 基础指令集里，它属于 M 扩展（M extension）。",
                 FadeIn(base), FadeIn(base_l), FadeIn(base_c), FadeIn(mx), FadeIn(mx_l), FadeIn(mx_c))
        self.say("通用乘法的电路比移位复杂得多，所以不放进基础指令集。除法、取余也在 M 扩展里，浮点运算在 F 扩展里。",
                 FadeIn(fx), FadeIn(fx_l))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ if without else
    def if_without_else(self):
        c1 = CodeListing([
            "if (i == j) {",
            "  x = y + z;",
            "} else {",
            "  x = y - z;",
            "}",
            "// …",
        ], lang="c", font_size=24, line_gap=0.42).to_corner(UL, buff=0.5)
        mp = VGroup(mono("x    y    z    i    j", 24),
                    mono("x10  x11  x12  x13  x14", 24, C_REG)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        mp.to_corner(UR, buff=0.6)
        self.say("回到分支。先看一个 if-else，变量 x、y、z、i、j 依次放在 x10 到 x14。",
                 FadeIn(c1, shift=RIGHT * 0.2), FadeIn(mp))

        def asm(lines):
            return CodeListing(lines, font_size=24, line_gap=0.44)

        a1 = asm(["       beq x13 x14 If", "       sub x10 x11 x12", "       j End",
                  "If:    add x10 x11 x12", "End:   # …"])
        b1 = asm(["       bne x13 x14 Else", "       add x10 x11 x12", "       j End",
                  "Else:  sub x10 x11 x12", "End:   # …"])
        a1.move_to([-6.3, 0.2, 0], aligned_edge=UL)
        b1.move_to([0.9, 0.2, 0], aligned_edge=UL)
        ta = zh("选项 A", 26, YELLOW_D).next_to(a1, UP, buff=0.3).align_to(a1, LEFT)
        tb = zh("选项 B", 26, YELLOW_D).next_to(b1, UP, buff=0.3).align_to(b1, LEFT)
        self.say("这个 if-else 有两种翻译。选项 B 和第 5 集一样：用 bne 把条件取反。",
                 FadeIn(tb), FadeIn(b1, shift=UP * 0.15))
        self.play(Circumscribe(b1.glyphs(0, "bne"), color=RED_B), Circumscribe(c1.glyphs(0, "=="), color=RED_B))
        self.say("选项 A 不取反：用 beq，相等就跳到 If，于是 else 部分反而写在前面。两种都对，都是 4 条指令。",
                 FadeIn(ta), FadeIn(a1, shift=UP * 0.15))
        self.hold()

        c2 = CodeListing([
            "if (i == j) {",
            "  x = y + z;",
            "}",
            "// …",
        ], lang="c", font_size=24, line_gap=0.42).move_to(c1, aligned_edge=UL)
        a2 = asm(["       beq x13 x14 If", "       j End", "If:    add x10 x11 x12", "End:   # …"])
        b2 = asm(["       bne x13 x14 End", "       add x10 x11 x12", "End:   # …"])
        a2.move_to(a1, aligned_edge=UL)
        b2.move_to(b1, aligned_edge=UL)
        self.say("那如果没有 else 呢？",
                 FadeTransform(c1, c2), FadeOut(a1, shift=DOWN * 0.1), FadeOut(b1, shift=DOWN * 0.1))
        self.play(FadeIn(a2, shift=UP * 0.1), FadeIn(b2, shift=UP * 0.1))

        ja = CurvedArrow(a2.right_of(0, 0.2), a2.right_of(2, 0.2), angle=-TAU / 4, color=YELLOW_D)
        jb = CurvedArrow(a2.right_of(1, 0.55), a2.right_of(3, 0.55), angle=-TAU / 4, color=RED_B)
        self.say("选项 A 用 beq：相等时跳到 If 执行 add；不相等时，还得靠 j End 绕过 add。",
                 Create(ja))
        self.play(Create(jb))
        self.hold()
        jc = CurvedArrow(b2.right_of(0, 0.2), b2.right_of(2, 0.2), angle=-TAU / 4, color=TEAL_C)
        self.say("选项 B 用 bne：不相等就直接跳到 End；相等时顺着往下执行 add。",
                 Create(jc))
        self.hold()
        na = zh("3 条指令", 24, GREY_B).next_to(ta, RIGHT, buff=0.5)
        nb = zh("2 条指令", 24, GREEN_C).next_to(tb, RIGHT, buff=0.5)
        self.say("两种都对。但 B 和 C 代码的结构一致，只要 2 条指令，比 A 少一条，性能也更好。",
                 FadeIn(na), FadeIn(nb), Create(SurroundingRectangle(b2, color=GREEN_C, buff=0.15)))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ goto recipes
    def goto_patterns(self):
        head = self.heading("循环的套路：先改写成 goto")
        def rule(c_src, a_src):
            left = tint(CodeListing([c_src], lang="c", font_size=30), ["goto"])
            return VGroup(left, mono("→", 30, GREY_B), CodeListing([a_src], font_size=30)).arrange(RIGHT, buff=0.4)

        rules = VGroup(rule("goto L;", "j L"), rule("if (x5 < x6) goto L;", "blt x5 x6 L"))
        rules.arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(UP * 0.5)
        self.say("汇编里没有 while 和 for，只有分支和跳转。它们相当于 C 里的 goto：跳到某个标签处接着执行。",
                 Write(head), LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in rules], lag_ratio=0.5))
        self.hold()
        self.say("在真正的 C 程序里别写 goto，它让代码很难读（xkcd 292 甚至说会招来迅猛龙）。但它很适合当翻译的中间一步。")
        self.hold()

        xs = [-6.5, -1.9, 2.75]
        hdrs = VGroup(mono("C", 26, GREY_A), zh("goto 形式", 26, GREY_A), zh("汇编", 26, GREY_A))
        for h, x in zip(hdrs, xs):
            h.move_to([x, 2.45, 0], aligned_edge=LEFT)
        rule_line = Line([-6.6, 2.12, 0], [6.6, 2.12, 0], stroke_color=GREY_D, stroke_width=1.5)
        cond = mono("cond: x5 < x6", 22, GREY_B).move_to([xs[0], -1.85, 0], aligned_edge=LEFT)
        self.say("套路是：先把控制结构改写成 goto，再一行一行换成指令。为了写出真实的指令，设 cond 为 x5 < x6。",
                 FadeOut(rules), FadeIn(hdrs), Create(rule_line), FadeIn(cond))

        def listing(lines, lang, x):
            lst = CodeListing(lines, lang=lang, font_size=20, line_gap=0.4)
            lst.move_to([x, 1.85, 0], aligned_edge=UL)
            if lang == "c":
                tint(lst, ["goto", "do", "true", "break"])
            return lst

        def cols(c, g, a):
            return [listing(c, "c", xs[0]), listing(g, "c", xs[1]), listing(a, "asm", xs[2])]

        shown = []
        tag = [None]

        def swap(new, name, caption):
            t = mono(name, 30, C_KEYWORD).to_corner(UR, buff=0.5)
            anims = [FadeOut(m, shift=UP * 0.15) for m in shown]
            anims += [FadeIn(m, shift=UP * 0.15) for m in new]
            anims.append(FadeIn(t) if tag[0] is None else Transform(tag[0], t))
            self.say(caption, *anims)
            if tag[0] is None:
                tag[0] = t
            shown[:] = new

        swap(cols(
            ["if(cond) {", "    line1;", "    line2;", "}", "line3;"],
            ["    if(!cond) goto AfterIf;", "    line1;", "    line2;", "AfterIf:", "    line3;"],
            ["    bge x5 x6 AfterIf", "    # line1", "    # line2", "AfterIf:", "    # line3"],
        ), "if", "刚才的 if 就是这样：if (!cond) goto AfterIf。条件不成立，就跳过 then 部分。")
        self.hold()
        swap(cols(
            ["while(cond) {", "    line1;", "    line2;", "}", "line3;"],
            ["Loop:", "    if(!cond) goto AfterLoop;", "    line1;", "    line2;", "    goto Loop;",
             "AfterLoop:", "    line3;"],
            ["Loop:", "    bge x5 x6 AfterLoop", "    # line1", "    # line2", "    j Loop",
             "AfterLoop:", "    # line3"],
        ), "while", "while：开头判断，不成立就跳出；末尾 goto Loop 回到开头。第 5 集的循环就是这个样子。")
        self.hold()
        swap(cols(
            ["while(true) {", "    line;", "    break;", "}", "line;"],
            ["while(true) {", "    line;", "    goto AfterWhile;", "}", "AfterWhile:", "    line;"],
            ["Loop:", "    # line", "    j AfterWhile", "    j Loop", "AfterWhile:", "    # line"],
        ), "break", "break 就是一句跳到循环后面的 goto，翻译出来是一条 j。")
        self.play(Indicate(shown[2][2], color=YELLOW_D, scale_factor=1.05))
        self.hold()

        f_c = listing(["for(startline;cond;incline) {", "    line1;", "    line2;", "}", "line3;"], "c", xs[0])
        w_c = listing(["startline;", "while(cond) {", "    line1;", "    line2;", "    incline;", "}", "line3;"],
                      "c", xs[0])
        swap([f_c], "for", "for 先改写成 while：初始化 startline 提到循环前面，递增 incline 放到循环体末尾……")
        self.play(FadeTransform(f_c, w_c), run_time=1.2)
        shown[:] = [w_c]
        g_f = listing(
            ["startline;", "Loop:", "    if(!cond) goto AfterLoop;", "    line1;", "    line2;", "    incline;",
             "    goto Loop;", "AfterLoop:", "    line3;"], "c", xs[1])
        a_f = listing(
            ["    # startline", "Loop:", "    bge x5 x6 AfterLoop", "    # line1", "    # line2", "    # incline",
             "    j Loop", "AfterLoop:", "    # line3"], "asm", xs[2])
        self.say("……然后照 while 的套路翻译。", FadeIn(g_f, shift=UP * 0.15), FadeIn(a_f, shift=UP * 0.15))
        shown[:] = [w_c, g_f, a_f]
        self.hold()
        swap(cols(
            ["do {", "    line1;", "    line2;", "} while(cond);", "line3;"],
            ["Loop:", "    line1;", "    line2;", "    if(cond) goto Loop;", "line3;"],
            ["Loop:", "    # line1", "    # line2", "    blt x5 x6 Loop", "    # line3"],
        ), "do-while", "do-while 先执行循环体，最后才判断，成立就跳回 Loop。条件不用取反，也不需要 j。")
        self.play(Indicate(shown[2][3], color=YELLOW_D, scale_factor=1.05))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ pointer loop + quiz
    def pointer_loop(self):
        c = CodeListing([
            "int arr[20];",
            "... // 给 arr 填入数据",
            "int sum = 0;",
            "for (int i=0; i<20; i++) {",
            "    sum += arr[i];",
            "}",
        ], lang="c", font_size=22, line_gap=0.4).move_to([-1.4, 3.4, 0], aligned_edge=UL)
        self.say("最后看一个完整的例子：把 int 数组 arr 的 20 个元素加起来。", FadeIn(c, shift=RIGHT * 0.2))

        g = CodeListing([
            "      int sum = 0;",
            "      int i = 0;",
            "Loop: if(i >= 20) goto End",
            "      sum += arr[i];",
            "      i++;",
            "      goto Loop",
            "End:  // …",
        ], lang="c", font_size=20, line_gap=0.4).move_to([-6.6, 3.2, 0], aligned_edge=UL)
        tint(g, ["goto"])
        self.say("先按套路改写成 goto：条件取反，i >= 20 就跳到 End。", FadeIn(g, shift=UP * 0.15))
        self.play(Circumscribe(g.glyphs(2, "i >= 20"), color=RED_B))
        self.hold()

        asm = CodeListing([
            "    add   x9  x8  x0",
            "    add  x10  x0  x0",
            "    add  x11  x0  x0",
            "    addi x13  x0  20",
            "Loop:",
            "    bge  x11 x13 End",
            "    lw   x12  0(x9)",
            "    add  x10 x10 x12",
            "    addi  x9  x9   4",
            "    addi x11 x11   1",
            "    j Loop",
            "End:",
            "    ...",
        ], font_size=22, line_gap=0.4).move_to([-6.6, 3.35, 0], aligned_edge=UL)
        asm.glyphs(12).set_color(GREY)
        self.say("这是笔记给出的汇编，一行注释也没有。每个寄存器对应 C 里的什么？",
                 FadeOut(g, shift=LEFT * 0.2), FadeIn(asm, shift=RIGHT * 0.2))
        self.hold()

        order = ["x8", "x11", "x9", "x12", "x10", "x13"]
        regs = VGroup()
        for n in order:
            r = RoundedRectangle(corner_radius=0.08, width=1.0, height=0.52, stroke_color=C_REG,
                                 fill_color=C_REG, fill_opacity=0.1)
            regs.add(VGroup(r, mono(n, 24, C_REG).move_to(r)))
        regs.arrange(RIGHT, buff=0.4).move_to([2.3, 0.3, 0])
        slots = VGroup(*[
            DashedVMobject(RoundedRectangle(corner_radius=0.08, width=1.3, height=0.46, stroke_color=GREY_B,
                                            stroke_width=1.5), num_dashes=16)
            .next_to(r, DOWN, buff=0.2) for r in regs
        ])
        opt_s = [("A", "sum"), ("B", "i"), ("C", "20"), ("D", "arr[0]"), ("E", "&arr[0]"),
                 ("F", "arr[i]"), ("G", "&arr[i]")]
        chips = VGroup()
        for letter, expr in opt_s:
            t = VGroup(mono(letter, 22, YELLOW_D), mono(expr, 22)).arrange(RIGHT, buff=0.18)
            r = RoundedRectangle(corner_radius=0.08, width=t.width + 0.35, height=0.46, stroke_color=GREY_B,
                                 stroke_width=1.5, fill_color=GREY_E, fill_opacity=0.4)
            t.move_to(r)
            chips.add(VGroup(r, t))
        top = VGroup(*chips[:4]).arrange(RIGHT, buff=0.25)
        bot = VGroup(*chips[4:]).arrange(RIGHT, buff=0.25)
        VGroup(top, bot).arrange(DOWN, buff=0.22).move_to([2.3, -1.5, 0])
        self.say("把上面的寄存器和下面的 C 表达式配对。提示：x8 存的是 arr 的地址。暂停一下，自己试试。",
                 LaggedStart(FadeIn(regs), FadeIn(slots), FadeIn(chips), lag_ratio=0.3))
        self.hold(3.0)

        answers = {"x8": "E", "x11": "B", "x9": "G", "x12": "F", "x10": "A", "x13": "C"}
        letters = [o[0] for o in opt_s]
        evidence = {"x8": [0], "x11": [2, 9], "x9": [0, 8], "x12": [6, 7], "x10": [1, 7], "x13": [3, 5]}
        text = {
            "x8": "x8 是 &arr[0]：数组首元素的地址，也就是数组 arr 的地址。",
            "x11": "x11 是 i：循环前清零，每轮末尾加 1。",
            "x9": "x9 是 &arr[i]：从 x8 出发，每轮加 4 而不是 1，因为一个 int 占 4 个字节。这就是指针运算。",
            "x12": "x12 是 arr[i]，是值而不是地址：lw 从 x9 指向的地址读出当前元素。",
            "x10": "x10 是 sum：先清零，循环里的 add x10 x10 x12 就是 sum += arr[i]。",
            "x13": "x13 是常数 20：bge 只能比较两个寄存器，所以先用 addi x13 x0 20（即 li x13 20）把 20 放进寄存器。",
        }
        marks = VGroup()
        boxes = None
        for k, n in enumerate(order):
            chip = chips[letters.index(answers[n])]
            placed = mono(dict(opt_s)[answers[n]], 20, YELLOW_D).move_to(slots[k])
            hl = VGroup(*[asm.line_box(i, color=C_REG, opacity=0.2) for i in evidence[n]])
            anims = [TransformFromCopy(chip[1][1], placed), FadeIn(hl),
                     Indicate(regs[k][1], color=YELLOW_D), chip.animate.set_opacity(0.35)]
            if boxes is not None:
                anims.append(FadeOut(boxes))
            self.say(text[n], *anims)
            marks.add(placed)
            boxes = hl
            self.hold()

        lb = asm.line_box(5, color=C_LABEL, opacity=0.18)
        self.say("注意 Loop 和 End 不是指令，只是地址的名字：Loop 就是 bge 那条指令的地址。",
                 FadeOut(boxes), FadeIn(lb),
                 Circumscribe(asm.glyphs(4), color=C_LABEL), Circumscribe(asm.glyphs(11), color=C_LABEL))
        self.hold()
        self.play(FadeOut(VGroup(regs, slots, chips, marks, lb)))

        brace = Brace(VGroup(*[asm[i] for i in range(5, 11)]), RIGHT, color=GREY_B)
        per = VGroup(zh("这里：每轮 6 条指令", 26, GREEN_C),
                     zh("第 5 集：每轮 7 条指令", 26, GREY_B)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        per.next_to(brace, RIGHT, buff=0.3)
        self.say("和第 5 集比一比：那里每轮用 slli 和 add 重新算 A + 4i；这里让指针每轮后移 4 个字节，每轮少一条指令。",
                 GrowFromCenter(brace), FadeIn(per[0]))
        self.play(FadeIn(per[1], shift=UP * 0.1))
        self.hold()
        run = mono("arr = {1, 2, …, 20}   →   sum = 210", 26, YELLOW_D).move_to([2.3, -1.5, 0])
        self.say("笔记还附了一个能在模拟器 Venus 里运行的完整版：arr 装着 1 到 20，程序最后打印出 210。",
                 FadeIn(run, shift=UP * 0.15))
        self.hold()
