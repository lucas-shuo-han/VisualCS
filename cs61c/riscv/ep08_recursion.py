import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403


# ---------------------------------------------------------------- the notes' code
# Every value shown in the episode (addresses, sp, ra, saved words, a0) is checked
# below by running the notes' code on a tiny RV32 interpreter.

MAIN = ["main:", "  li a0 3", "  jal ra factorial", "  …"]
FACT = [
    "factorial:",
    "  addi sp sp -8",
    "  sw ra 0(sp)",
    "  sw s0 4(sp)",
    "  mv s0 a0",
    "  li t0 1",
    "  bne s0 t0 recurse",
    "  li a0 1",
    "  j epilogue",
    "recurse:",
    "  addi a0 s0 -1",
    "  jal ra factorial",
    "  mul a0 s0 a0",
    "epilogue:",
    "  lw ra 0(sp)",
    "  lw s0 4(sp)",
    "  addi sp sp 8",
    "  jr ra",
]
FOO = [
    "foo:",
    "  addi sp sp -8",
    "  sw ra 0(sp)",
    "  sw s0 4(sp)",
    "  mv s0 a0",
    "  bne s0 x0 Next",
    "  li a0 0",
    "  j Epilogue",
    "Next:",
    "  addi a0 s0 -1",
    "  jal ra foo",
    "  add a0 s0 a0",
    "Epilogue:",
    "  lw ra 0(sp)",
    "  lw s0 4(sp)",
    "  addi sp sp 8",
    "  jr ra",
]
FOO_MAIN = [
    "main:",
    "  li a0 3",
    "  jal ra foo",
    "  mv s0 a0",
    "  li a0 100",
    "  jal ra foo",
    "  mv s1 a0",
    "  add a0 s0 s1",
    "  …",
]
FUNC_A = [
    "func_a:",
    "  addi sp, sp, -8",
    "  sw   ra, 0(sp)",
    "  sw   s0, 4(sp)",
    "  addi t1, x0, 10",
    "  addi s0, x0, 20",
    "  addi sp, sp, -4",
    "  sw   t1, 0(sp)",
    "  jal  func_b",
    "  lw   t1, 0(sp)",
    "  addi sp, sp, 4",
    "  addi t1, t1, 5",
    "  addi s0, s0, 5",
    "  lw   ra, 0(sp)",
    "  lw   s0, 4(sp)",
    "  addi sp, sp, 8",
    "  ret",
]
FUNC_B = ["func_b:", "  addi t1, x0, 99", "  ret"]   # stand-in callee that clobbers t1


def layout(lines, base):
    """Address of every instruction line (None for label lines) and the label table."""
    addrs, labels, a = [], {}, base
    for s in lines:
        s = s.strip()
        if s.endswith(":"):
            labels[s[:-1]] = a
            addrs.append(None)
        else:
            addrs.append(a)
            a += 4
    return addrs, labels


def run(progs, regs, stop, limit=5000):
    """Run (lines, base) programs from regs['pc'] until pc == stop.
    Returns final registers, the list of stores (addr, value) and a per-step
    snapshot (pc, registers before the instruction)."""
    code, labels = {}, {}
    for lines, base in progs:
        addrs, lab = layout(lines, base)
        labels.update(lab)
        code.update({a: s.replace(",", " ").split() for s, a in zip(lines, addrs) if a is not None})
    R = dict(regs)
    mem, stores, steps = {}, [], []

    def rv(r):
        return 0 if r in ("x0", "zero") else R.get(r, 0)

    def wr(r, v):
        if r not in ("x0", "zero"):
            R[r] = v & 0xFFFFFFFF

    def ea(m):
        off, base = re.fullmatch(r"(-?\d+)\((\w+)\)", m).groups()
        return (rv(base) + int(off)) & 0xFFFFFFFF

    while R["pc"] != stop:
        assert len(steps) < limit
        pc = R["pc"]
        op, *a = code[pc]
        steps.append((pc, dict(R)))
        nxt = pc + 4
        if op == "addi":
            wr(a[0], rv(a[1]) + int(a[2]))
        elif op == "mv":
            wr(a[0], rv(a[1]))
        elif op == "li":
            wr(a[0], int(a[1]))
        elif op == "add":
            wr(a[0], rv(a[1]) + rv(a[2]))
        elif op == "mul":
            wr(a[0], rv(a[1]) * rv(a[2]))
        elif op == "sw":
            mem[ea(a[1])] = rv(a[0])
            stores.append((ea(a[1]), rv(a[0])))
        elif op == "lw":
            wr(a[0], mem[ea(a[1])])
        elif op == "bne":
            if rv(a[0]) != rv(a[1]):
                nxt = labels[a[2]]
        elif op == "j":
            nxt = labels[a[0]]
        elif op == "jal":
            rd, lab = (a[0], a[1]) if len(a) == 2 else ("ra", a[0])
            wr(rd, pc + 4)
            nxt = labels[lab]
        elif op == "jr":
            nxt = rv(a[0])
        elif op == "ret":
            nxt = rv("ra")
        else:
            raise ValueError(op)
        R["pc"] = nxt
    return R, stores, steps


MAIN_BASE, FACT_BASE = 0x1000, 0x2000
MAIN_ADDR, _ = layout(MAIN, MAIN_BASE)
FACT_ADDR, _ = layout(FACT, FACT_BASE)
SP_MAIN = 0xFFFFFFE0 - 12          # main's 12-byte frame, as in the notes' stack animation
assert SP_MAIN == 0xFFFFFFD4 and SP_MAIN - 8 == 0xFFFFFFCC
assert MAIN_ADDR[2] == 0x1004 and MAIN_ADDR[3] == 0x1008
assert FACT_ADDR[11] == 0x2024 and FACT_ADDR[12] == 0x2028 and FACT_ADDR[17] == 0x2038

_R, _ST, _STEPS = run([(MAIN, MAIN_BASE), (FACT, FACT_BASE)],
                      {"pc": 0x1000, "sp": SP_MAIN, "s0": 42}, stop=0x1008)
FRAME_SP = {3: 0xFFFFFFCC, 2: 0xFFFFFFC4, 1: 0xFFFFFFBC}
assert [r["sp"] for pc, r in _STEPS if pc == 0x2004] == [FRAME_SP[3], FRAME_SP[2], FRAME_SP[1]]
assert _ST == [(0xFFFFFFCC, 0x1008), (0xFFFFFFD0, 42),     # factorial(3): ra, main's s0
               (0xFFFFFFC4, 0x2028), (0xFFFFFFC8, 3),      # factorial(2)
               (0xFFFFFFBC, 0x2028), (0xFFFFFFC0, 2)]      # factorial(1)
assert [(r["s0"], r["a0"]) for pc, r in _STEPS if pc == 0x2028] == [(2, 1), (3, 2)]   # at mul
assert [r["ra"] for pc, r in _STEPS if pc == 0x2038] == [0x2028, 0x2028, 0x1008]      # at jr ra
assert [r["sp"] for pc, r in _STEPS if pc == 0x2038] == [0xFFFFFFC4, 0xFFFFFFCC, SP_MAIN]
assert (_R["a0"], _R["sp"], _R["s0"], _R["ra"]) == (6, SP_MAIN, 42, 0x1008)

# foo: foo(3) = 6, foo(100) = 5050; foo(100) keeps 101 frames (808 bytes) on the stack at once
_FOO_PROG = ["  j main"] + FOO + FOO_MAIN
_R, _ST, _STEPS = run([(_FOO_PROG, 0x1000)], {"pc": 0x1000, "sp": SP_MAIN},
                      stop=layout(_FOO_PROG, 0x1000)[0][-1])       # stop at main's "…"
assert (_R["s0"], _R["s1"], _R["a0"]) == (6, 5050, 5056)
assert SP_MAIN - min(r["sp"] for _, r in _STEPS) == 101 * 8 == 808

# func_a (entered from main with ra = 0x1008, sp = 0xFFFFFFD4, s0 = 42)
FUNC_A_BASE = 0x3000
FUNC_A_ADDR, _ = layout(FUNC_A, FUNC_A_BASE)
_R, _ST, _STEPS = run([(FUNC_A, FUNC_A_BASE), (FUNC_B, 0x4000)],
                      {"pc": FUNC_A_BASE, "ra": 0x1008, "sp": SP_MAIN, "s0": 42}, stop=0x1008)
assert FUNC_A_ADDR[8] == 0x301C and FUNC_A_ADDR[9] == 0x3020
assert _ST == [(0xFFFFFFCC, 0x1008), (0xFFFFFFD0, 42), (0xFFFFFFC8, 10)]
assert [(r["ra"], r["t1"], r["sp"]) for pc, r in _STEPS if pc == 0x3020] == [(0x3020, 99, 0xFFFFFFC8)]
assert [(r["t1"], r["s0"], r["sp"]) for pc, r in _STEPS if pc == 0x3030] == [(15, 25, 0xFFFFFFCC)]
assert (_R["t1"], _R["s0"], _R["sp"], _R["ra"]) == (15, 42, SP_MAIN, 0x1008)

FRAME_COLORS = {3: BLUE_C, 2: TEAL_C, 1: GREEN_C}


# ---------------------------------------------------------------- helpers
def addr_col(listing, addrs, size=16):
    g = VGroup()
    for i, a in enumerate(addrs):
        if a is not None:
            g.add(mono(f"0x{a:X}", size, GREY).next_to(listing.left_of(i, 0.22), LEFT, buff=0))
    return g


def place_listing(lst, left_x, top_y):
    """Put the code's left edge at left_x and the first line's center at top_y."""
    lst.shift(np.array([left_x - lst.get_left()[0], top_y - lst[0].get_center()[1], 0]))
    return lst


def side_brace(lst, i, j, text, color=BLUE_B, size=22, x=None):
    grp = VGroup(*[lst[k] for k in range(i, j + 1)])
    b = Brace(grp, RIGHT, color=color, buff=0.1)
    x = lst.get_right()[0] + 0.12 if x is None else x
    b.shift(RIGHT * (x - b.get_left()[0]))
    t = zh(text, size, color).next_to(b, RIGHT, buff=0.1)
    return VGroup(b, t)


def frame_brace(col, i, j, text, color, size=20):
    b = Brace(VGroup(col.cells[i], col.cells[j]), LEFT, color=color, buff=0.05)
    x = col.addr_labels.get_left()[0] - 0.1
    b.shift(RIGHT * (x - b.get_right()[0]))
    t = mono(text, size, color).next_to(b, LEFT, buff=0.1)
    return VGroup(b, t)


def sp_pointer(size=22):
    g = VGroup(Arrow(RIGHT * 0.55, ORIGIN, buff=0, color=C_SP, stroke_width=5,
                     max_tip_length_to_length_ratio=0.4), mono("sp", size, C_SP))
    g[1].next_to(g[0], RIGHT, buff=0.08)
    return g


class Ep08Recursion(NarratedScene):
    def construct(self):
        self.title_card()
        self.jumps()
        self.clobber()
        self.contract()
        self.fact_code()
        self.fact_trace()
        self.foo_compare()
        self.leaf()
        self.reg_table()
        self.func_a()
        self.quiz()
        self.six_steps()
        self.end_card(
            [
                "真正的跳转指令只有 jal（跳到标签）和 jalr（跳到寄存器里的地址）",
                "j、jr、ret 都是 rd = x0 的伪指令：只跳，不链接",
                "递归的每一层都有自己的栈帧，各存一份 ra 和 s0",
                "跨调用还要用的值，放进 s 寄存器或存到栈上",
                "叶子函数不必保存 ra，常常连栈都不用",
            ],
        )

    # ------------------------------------------------------------------ jal / jalr
    def jumps(self):
        head = self.heading("无条件跳转：jal 与 jalr")
        real_l = zh("真正的指令", 24, GREY_B)
        r1 = CodeListing(["jal  rd, label"], font_size=26)
        r2 = CodeListing(["jalr rd, rs1, imm"], font_size=26)
        m1 = mono("rd = PC + 4;  PC = PC + offset", 24, GREY_A)
        m2 = mono("rd = PC + 4;  PC = rs1 + imm", 24, GREY_A)
        x0, x1 = -5.6, -1.4
        real_l.move_to([x0, 2.55, 0], aligned_edge=LEFT)
        for row, (c, m) in enumerate([(r1, m1), (r2, m2)]):
            y = 1.95 - row * 0.62
            c.move_to([x0, y, 0], aligned_edge=LEFT)
            m.move_to([x1, y, 0], aligned_edge=LEFT)
        alt = mono("也写作 jalr rd, imm(rs1)", 20, GREY).next_to(r2, DOWN, buff=0.14).align_to(r2, LEFT)
        self.say("第 7 集用过 jal 和 jr ra。其实 RISC-V 真正的无条件跳转指令只有两条。",
                 Write(head), FadeIn(real_l))
        self.say("jal rd, label 意为“跳转并链接”，其实先链接：把 PC + 4 写进 rd，再跳到 label。",
                 FadeIn(r1, shift=RIGHT * 0.2), FadeIn(m1, shift=RIGHT * 0.2))
        self.play(Circumscribe(m1[:8], color=C_RA))
        self.say("jalr rd, rs1, imm 同样先链接，但跳到 rs1 + imm：地址来自寄存器。",
                 FadeIn(r2, shift=RIGHT * 0.2), FadeIn(m2, shift=RIGHT * 0.2), FadeIn(alt))
        self.hold()

        pseudo_l = zh("伪指令（由汇编器展开）", 24, GREY_B).move_to([x0, 0.25, 0], aligned_edge=LEFT)
        rows = [
            ("j    label", "jal  x0, label", "只跳，不留返回地址"),
            ("jal  label", "jal  ra, label", "调用：返回地址写进 ra"),
            ("jr   rs", "jalr x0, rs, 0", "跳到寄存器里的地址"),
            ("ret", "jalr x0, ra, 0", "从函数返回"),
        ]
        prow = VGroup()
        for k, (p, e, tag) in enumerate(rows):
            y = -0.3 - k * 0.52
            a = CodeListing([p], font_size=26).move_to([x0, y, 0], aligned_edge=LEFT)
            eq = mono("=", 26, GREY_B).move_to([-3.05, y, 0])
            b = CodeListing([e], font_size=26).move_to([-2.65, y, 0], aligned_edge=LEFT)
            t = zh(tag, 24, GREY_A).move_to([0.75, y, 0], aligned_edge=LEFT)
            prow.add(VGroup(a, eq, b, t))
        self.say("其余跳转都是伪指令。j、jr、ret 把返回地址写进 x0，等于丢掉；省略 rd 的 jal 则链接到 ra。",
                 FadeIn(pseudo_l), LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in prow], lag_ratio=0.3))
        self.play(*[Indicate(prow[k][2].glyphs(0, "x0"), color=RED_B) for k in (0, 2, 3)])
        self.hold()

        self.play(FadeOut(VGroup(pseudo_l, prow)))
        why_a = VGroup(
            zh("目标 = PC + 偏移：汇编时就确定了", 24, C_MNEM),
            zh("适合调用有名字的函数", 24, GREY_A),
            CodeListing(["jal  ra, factorial"], font_size=24),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        why_b = VGroup(
            zh("目标 = rs1 + imm：运行时才算出来", 24, C_MNEM),
            CodeListing(["jr   ra         # 返回：回到哪里由 ra 决定",
                         "jalr ra, t0, 0  # 函数指针：调用 t0 里的地址"], font_size=22, line_gap=0.42),
            zh("远跳转：auipc + jalr（第 12 集）", 24, GREY_A),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        why_a.move_to([x0, -0.35, 0], aligned_edge=LEFT)
        why_b.move_to([x0, -0.55, 0], aligned_edge=LEFT)
        self.say("为什么要两条？jal 的目标在汇编时就定了，正适合调用有名字的函数。",
                 FadeIn(why_a, shift=UP * 0.15), Circumscribe(VGroup(r1, m1), color=C_MNEM))
        self.hold()
        self.say("jalr 的目标由寄存器在运行时给出：返回 ra 里的地址、调用函数指针，配合 auipc 还能跳得很远。",
                 FadeOut(why_a), FadeIn(why_b, shift=UP * 0.15), Circumscribe(VGroup(r2, m2), color=C_MNEM))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ what goes wrong
    def clobber(self):
        c = CodeListing([
            "// 假设 n 是正整数",
            "int factorial(int n) {",
            "  if (n == 1) return 1;",
            "  int a = n * factorial(n-1);",
            "  return a;",
            "}",
        ], lang="c", font_size=22, line_gap=0.44).to_corner(UL, buff=0.5)
        self.say("本集的主角是阶乘：factorial(1) = 1，factorial(n) = n × factorial(n − 1)。",
                 FadeIn(c, shift=RIGHT * 0.2))
        self.hold()

        def call_box(name, color):
            return box_label(name, color, w=2.9, h=0.7, font_size=26, font=MONO)

        chain = VGroup(call_box("main", GREY_B), call_box("factorial(2)", BLUE_C),
                       call_box("factorial(1)", GREEN_C)).arrange(DOWN, buff=0.85)
        chain.move_to(RIGHT * 3.9 + UP * 0.55)
        calls = VGroup(*[Arrow(chain[k].get_bottom(), chain[k + 1].get_top(), buff=0.08, color=GREY_B)
                         .shift(LEFT * 0.5) for k in range(2)])
        call_l = VGroup(*[mono("jal", 22, C_MNEM).next_to(a, LEFT, buff=0.12) for a in calls])
        a0 = RegBox("a0", 2, width=3.2, font_size=24)
        ra = RegBox("ra", "→ main", width=3.2, font_size=24)
        regs = VGroup(a0, ra).arrange(DOWN, buff=0.3).next_to(c, DOWN, buff=0.6).align_to(c, LEFT).shift(RIGHT * 0.5)
        self.say("如果什么都不保存，会怎样？设 main 调用 factorial(2)：a0 = 2，ra 记着回 main 的地址。",
                 FadeIn(chain[:2]), GrowArrow(calls[0]), FadeIn(call_l[0]), FadeIn(regs))
        self.say("factorial(2) 把参数 1 放进 a0，再 jal：ra 被改成回 factorial(2) 的地址。",
                 FadeIn(chain[2]), GrowArrow(calls[1]), FadeIn(call_l[1]))
        self.play(a0.set(1))
        self.play(ra.set("→ factorial(2)"))
        self.hold()
        back = Arrow(chain[2].get_top(), chain[1].get_bottom(), buff=0.08, color=GOLD_B).shift(RIGHT * 0.5)
        back_l = mono("a0 = 1", 22, C_A).next_to(back, RIGHT, buff=0.12)
        want = mono("2 × a0", 26, WHITE).next_to(regs, DOWN, buff=0.5).align_to(regs, LEFT)
        lost = mono("? × 1", 26, RED_B).move_to(want, aligned_edge=LEFT)
        self.say("factorial(1) 返回 1，可 factorial(2) 的 2 早被参数 1 覆盖了；ra 也还指着 factorial(2) 自己，再也回不到 main。",
                 GrowArrow(back), FadeIn(back_l))
        self.play(FadeIn(want))
        self.play(Transform(want, lost), Indicate(a0, color=RED_B))
        cross = Cross(calls[0], stroke_color=RED_C, stroke_width=5).scale(0.7)
        self.play(Indicate(ra, color=RED_B), Create(cross))
        self.hold()
        self.clear_stage()

        # strawman: save everything
        cells = VGroup()
        for i in range(1, 32):
            name = ABI_NAMES[i]
            sq = RoundedRectangle(corner_radius=0.05, width=1.15, height=0.5, stroke_color=abi_color(name),
                                  stroke_width=2, fill_color=abi_color(name), fill_opacity=0.12)
            t = mono(f"x{i}", 20, WHITE).move_to(sq)
            cells.add(VGroup(sq, t))
        cells.arrange_in_grid(4, 8, buff=(0.18, 0.2)).move_to(UP * 1.0)
        cost = zh("每次调用：31 次 sw，再加 31 次 lw", 30, YELLOW_D).next_to(cells, DOWN, buff=0.55)
        self.say("最省事的办法：每次调用都把 x1 到 x31 全部压栈，返回后再全部取回。",
                 LaggedStart(*[FadeIn(k, shift=DOWN * 0.1) for k in cells], lag_ratio=0.02, run_time=1.6))
        self.play(FadeIn(cost, shift=UP * 0.15))
        keep = [0, 7]   # ra (x1), s0 (x8)
        self.say("可访问内存很慢，而一次调用真正要保护的，往往只有几个寄存器。",
                 *[cells[k].animate.set_opacity(0.18) for k in range(31) if k not in keep],
                 *[Indicate(cells[k], color=YELLOW_D) for k in keep])
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ the contract
    def contract(self):
        def card(title, color, rows):
            t = zh(title, 28, color)
            body = VGroup()
            for regs, note, rc in rows:
                body.add(VGroup(mono(regs, 24, rc), zh(note, 24, GREY_A)).arrange(RIGHT, buff=0.3))
            body.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
            inner = VGroup(t, body).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
            frame = RoundedRectangle(corner_radius=0.15, width=6.2, height=inner.height + 0.6,
                                     stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.07)
            inner.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.3)
            return VGroup(frame, inner)

        left = card("调用者可以指望", BLUE_C, [
            ("s0–s11, sp", "调用后保持不变", C_S),
            ("t0–t6, a0–a7, ra", "可能已经被改", C_T),
        ])
        right = card("被调用者必须做到", GOLD_C, [
            ("t0–t6, a0–a7", "随便用", C_T),
            ("s0–s11, sp", "用前保存，返回前恢复", C_S),
        ])
        VGroup(left, right).arrange(RIGHT, buff=0.4).move_to(UP * 1.7)
        self.say("解决办法是第 7 集的调用约定：调用者只能指望 s 寄存器和 sp 不变；被调用者要用 s 寄存器，得先存旧值、返回前恢复。",
                 FadeIn(left[0]), FadeIn(left[1][0]), FadeIn(right[0]), FadeIn(right[1][0]))
        self.play(FadeIn(left[1][1], shift=UP * 0.1))
        self.play(FadeIn(right[1][1], shift=UP * 0.1))
        self.hold()

        def fbox(name, color):
            return box_label(name, color, h=0.7, font_size=24, font=MONO)

        chain = VGroup(fbox("main", GREY_B), fbox("factorial(3)", BLUE_C), fbox("factorial(2)", TEAL_C))
        chain.arrange(RIGHT, buff=1.3).move_to(DOWN * 1.25)
        arrows = VGroup(*[Arrow(chain[k].get_right(), chain[k + 1].get_left(), buff=0.1, color=GREY_B)
                          for k in range(2)])
        up_t = zh("对 main：被调用者", 22, GOLD_C).next_to(chain[1], UP, buff=0.18)
        dn_t = zh("对 factorial(2)：调用者", 22, BLUE_C).next_to(chain[1], DOWN, buff=0.18)
        self.say("递归函数身兼两职：对上一层它是被调用者，对下一层它又是调用者。",
                 FadeIn(chain), GrowArrow(arrows[0]), GrowArrow(arrows[1]))
        self.play(FadeIn(up_t, shift=DOWN * 0.1))
        self.play(FadeIn(dn_t, shift=UP * 0.1))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ the notes' factorial
    def build_fact(self):
        lst = place_listing(CodeListing(FACT, font_size=20, line_gap=0.31), -5.7, 3.5)
        addrs = addr_col(lst, FACT_ADDR)
        self.lst, self.lst_addrs = lst, addrs
        return lst, addrs

    def fact_code(self):
        lst, addrs = self.build_fact()
        c = CodeListing([
            "int factorial(int n) {",
            "  if (n == 1) return 1;",
            "  int a = n * factorial(n-1);",
            "  return a;",
            "}",
        ], lang="c", font_size=20, line_gap=0.36)
        c.move_to([6.6, 3.5, 0], aligned_edge=UR).shift(DOWN * c[0].height / 2)
        pro = side_brace(lst, 1, 3, "序言")
        epi = side_brace(lst, 14, 17, "尾声")
        self.say("这是笔记里遵守调用约定的阶乘，从地址 0x2000 开始。先认出序言和尾声。",
                 FadeIn(lst, shift=RIGHT * 0.2), FadeIn(addrs), FadeIn(c))
        self.play(GrowFromCenter(pro[0]), FadeIn(pro[1]), GrowFromCenter(epi[0]), FadeIn(epi[1]))
        self.hold()

        def hl(i, j=None):
            """Highlight lines i..j (all lines share one height)."""
            j = i if j is None else j
            b = lst.line_box(i)
            b.stretch_to_fit_height(lst[i].get_top()[1] - lst[j].get_bottom()[1] + 0.08)
            return b.move_to([b.get_center()[0], (lst[i].get_center()[1] + lst[j].get_center()[1]) / 2, 0])

        box = hl(1, 3)
        mini = VGroup()
        for k, (off, what, col) in enumerate([("4(sp)", "s0", C_S), ("0(sp)", "ra", C_RA)]):
            r = Rectangle(width=1.2, height=0.42, stroke_color=GREY_B, stroke_width=1.5,
                          fill_color=col, fill_opacity=0.15).move_to(DOWN * k * 0.42)
            lab = mono(off, 18, GREY_B).next_to(r, LEFT, buff=0.15)
            mini.add(VGroup(r, lab, mono(what, 20, col).move_to(r)))
        mini.move_to([0.4 if EN else -0.2, 2.4, 0])     # clear of the wider "prologue" label
        mini_t = zh("8 字节的栈帧", 20, GREY_A).next_to(mini, DOWN, buff=0.15)
        self.say("序言在栈上划出 8 字节，这就是本次调用的栈帧：后面的 jal 会覆盖 ra，要借用的 s0 也得先存旧值。",
                 FadeIn(box), FadeIn(mini), FadeIn(mini_t))
        self.hold()
        self.say("mv s0 a0 把 n 放进 s0：s 寄存器跨调用不变，递归调用回来，n 还在。",
                 box.animate.become(hl(4)), Circumscribe(c.glyphs(0, "int n"), color=C_S))
        self.say("bne 只能比较两个寄存器，所以先用 li 把 1 放进 t0；n ≠ 1 就跳到 recurse。",
                 box.animate.become(hl(5, 6)))
        self.hold()
        jump = CurvedArrow(lst.right_of(8, 0.15), lst.right_of(13, 0.15), angle=-TAU / 4, color=YELLOW_D)
        self.say("否则是基本情况：a0 = 1。这里不能直接 jr ra：s0 还没恢复，栈帧也没弹，所以 j 到尾声。",
                 box.animate.become(hl(7, 8)), Circumscribe(c[1], color=YELLOW_D))
        self.play(Create(jump))
        self.hold()
        self.say("recurse：a0 = n − 1，调用自己；回来时 a0 = (n − 1)!，再乘上 s0 里的 n。",
                 FadeOut(jump), box.animate.become(hl(10, 12)), Circumscribe(c[2], color=YELLOW_D))
        self.hold()
        self.say("尾声的顺序和序言相反：先从栈上取回 ra 和 s0，再把 sp 加 8 弹掉栈帧，最后 jr ra。",
                 box.animate.become(hl(14, 17)))
        self.hold()
        self.play(FadeOut(VGroup(box, c, pro, epi, mini, mini_t)))

    # ------------------------------------------------------------------ trace factorial(3)
    def fact_trace(self):
        lst, addrs = self.lst, self.lst_addrs
        main = place_listing(CodeListing(MAIN, font_size=20, line_gap=0.31), -1.1, 3.5)
        m_addrs = addr_col(main, MAIN_ADDR)
        regs = VGroup(
            RegBox("sp", hex32(SP_MAIN), width=1.65, font_size=20),
            RegBox("ra", "—", width=1.65, font_size=20),
            RegBox("s0", 42, width=1.65, font_size=20),
            RegBox("a0", "—", width=1.65, font_size=20),
        ).arrange_in_grid(2, 2, buff=(0.45, 0.16)).to_corner(UR, buff=0.35)
        R = dict(zip(["sp", "ra", "s0", "a0"], regs))

        col = WordColumn(0xFFFFFFDC, 9, cell_w=2.1, cell_h=0.42, font_size=18)
        col.shift(np.array([4.45 - col.cells.get_center()[0], 1.85 - col.cells[0].get_center()[1], 0]))
        for k in range(3):
            col.cells[k].set_fill(GREY_D, 0.5)
        col.texts[1].become(zh("main 的数据", 18, GREY).move_to(col.cells[1]))
        main_fb = frame_brace(col, 0, 2, "main", GREY_B)
        sp = sp_pointer().next_to(col.cells[2], RIGHT, buff=0.08)

        def sp_to(addr):
            return sp.animate.next_to(col.cell(addr), RIGHT, buff=0.08)

        self.say("完整跟踪一次 factorial(3)。main 已经分配了 12 字节的栈帧，此时 sp = 0xFFFFFFD4。",
                 FadeIn(main), FadeIn(m_addrs), FadeIn(regs), FadeIn(col), FadeIn(main_fb), FadeIn(sp))
        self.hold()

        box = main.line_box(1)

        def at(listing, i, *anims, rt=0.45):
            self.play(box.animate.become(listing.line_box(i)), *anims, run_time=rt)

        def fly(src, addr, s, color, rt=0.7):
            v = src.val.copy()
            self.play(v.animate.move_to(col.cell(addr)), run_time=rt)
            self.play(FadeOut(v), col.set(addr, s, color), run_time=0.4)

        self.say("main 把 3 放进 a0，在 0x1004 执行 jal：ra = 0x1008，跳进 factorial。", FadeIn(box))
        self.play(R["a0"].set(3))
        at(main, 2, R["ra"].set("0x1008"))
        at(lst, 1)
        self.hold()

        frames = {}

        def push(n, rt=0.45, slow=False):
            s = FRAME_SP[n]
            color = FRAME_COLORS[n]
            fb = frame_brace(col, col.i_of(s + 4), col.i_of(s), f"factorial({n})", color)
            frames[n] = fb
            at(lst, 1, R["sp"].set(hex32(s)), sp_to(s), FadeIn(fb),
               col.cell(s).animate.set_fill(color, 0.18), col.cell(s + 4).animate.set_fill(color, 0.18), rt=rt)
            ra_v, s0_v = R["ra"].value, R["s0"].value
            if slow:
                at(lst, 2, rt=rt)
                fly(R["ra"], s, f"ra = {ra_v}", C_RA)
                at(lst, 3, rt=rt)
                fly(R["s0"], s + 4, f"s0 = {s0_v}", C_S)
            else:
                at(lst, 2, col.set(s, f"ra = {ra_v}", C_RA), rt=rt)
                at(lst, 3, col.set(s + 4, f"s0 = {s0_v}", C_S), rt=rt)

        def body_to_call(n, rt=0.45):
            at(lst, 4, R["s0"].set(n), rt=rt)
            at(lst, 5, rt=rt)
            at(lst, 6, rt=rt)
            at(lst, 10, R["a0"].set(n - 1), rt=rt)
            at(lst, 11, rt=rt)
            at(lst, 1, R["ra"].set("0x2028"), rt=rt)

        self.say("factorial(3) 的序言：sp 减 8，变成 0xFFFFFFCC，再存下 ra = 0x1008 和 main 的 s0 = 42。")
        push(3, rt=0.6, slow=True)
        self.hold()
        self.say("mv 让 s0 = 3；3 ≠ 1，跳到 recurse：a0 = 2，在 0x2024 执行 jal，ra = 0x2028。")
        body_to_call(3, rt=0.55)
        self.hold()
        self.say("factorial(2) 照样压栈帧：sp = 0xFFFFFFC4，存下 ra = 0x2028 和 s0 = 3，再以 a0 = 1 调用自己。")
        push(2, rt=0.4)
        body_to_call(2, rt=0.4)
        self.hold()
        self.say("factorial(1) 也压一个：sp = 0xFFFFFFBC，存下 ra = 0x2028 和 s0 = 2。")
        push(1, rt=0.4)
        at(lst, 4, R["s0"].set(1), rt=0.4)
        at(lst, 5, rt=0.4)
        at(lst, 6, rt=0.4)
        self.hold()
        saved_ra = VGroup(*[col.texts[col.i_of(FRAME_SP[n])] for n in (3, 2, 1)])
        self.say("三个栈帧各存一份 ra 和 s0：factorial(3) 存的 ra 回 main，另两份都回 0x2028 的 mul。",
                 *[Indicate(t, color=C_RA) for t in saved_ra])
        mul_addr = addrs[sum(a is not None for a in FACT_ADDR[:12])]   # the label of line 12
        self.play(Indicate(mul_addr, color=C_RA), Indicate(lst[12], color=C_RA))
        self.hold()

        def pop(n, s0_back, ret_val, dest, rt=0.4):
            s = FRAME_SP[n]
            at(lst, 14, R["ra"].set("0x1008" if n == 3 else "0x2028"), rt=rt)
            at(lst, 15, R["s0"].set(s0_back), rt=rt)
            fb = frames[n]
            new_l = mono(f"factorial({n}) = {ret_val}", 20, FRAME_COLORS[n]).next_to(fb[0], LEFT, buff=0.1)
            at(lst, 16, R["sp"].set(hex32(s + 8)), sp_to(s + 8), Transform(fb[1], new_l),
               fb[0].animate.set_opacity(0.4),
               col.texts[col.i_of(s)].animate.set_opacity(0.35), col.texts[col.i_of(s + 4)].animate.set_opacity(0.35),
               col.cell(s).animate.set_fill(opacity=0.05), col.cell(s + 4).animate.set_fill(opacity=0.05), rt=rt)
            at(lst, 17, rt=rt)
            at(*dest, rt=rt)

        self.say("factorial(1) 是基本情况：a0 = 1，然后 j 到尾声。")
        at(lst, 7, R["a0"].set(1))
        at(lst, 8)
        at(lst, 14)
        self.say("尾声取回 ra = 0x2028 和 s0 = 2，sp 回到 0xFFFFFFC4，jr ra 回到 mul。")
        pop(1, 2, 1, (lst, 12), rt=0.5)
        self.hold()
        # right after the mul line's own text, clear of the frame labels on the right
        f_x = lst[12].get_right()[0] + 0.35
        f1 = mono("2 × 1 = 2", 20, C_A).move_to([f_x, lst[12].get_center()[1], 0], aligned_edge=LEFT)
        self.say("a0 = s0 × a0 = 2 × 1 = 2。s0 里的 2 正是 factorial(2) 的 n：factorial(1) 用过 s0，但返回前恢复了。",
                 R["a0"].set(2), FadeIn(f1, shift=RIGHT * 0.1))
        self.play(Indicate(R["s0"], color=C_S))
        self.hold()
        f2 = mono("3 × 2 = 6", 20, C_A).move_to(f1, aligned_edge=LEFT)
        self.say("factorial(2) 走完尾声：ra = 0x2028，s0 = 3，sp = 0xFFFFFFCC。回到 mul：a0 = 3 × 2 = 6。")
        pop(2, 3, 2, (lst, 12), rt=0.45)
        self.play(R["a0"].set(6), Transform(f1, f2))
        self.hold()
        self.say("factorial(3) 取回 ra = 0x1008 和 main 的 s0 = 42，sp 回到 0xFFFFFFD4，返回 main。")
        pop(3, 42, 6, (main, 3), rt=0.5)
        self.hold()
        self.say("回到 main：a0 = 6，sp 和 s0 都和调用前一样。弹出的栈帧还留在内存里，只是没人再用了。",
                 Circumscribe(R["a0"], color=C_A), Circumscribe(R["sp"], color=C_SP), Circumscribe(R["s0"], color=C_S))
        self.hold()
        self.play(FadeOut(VGroup(main, m_addrs, regs, col, main_fb, sp, box, f1, *frames.values())))

    # ------------------------------------------------------------------ foo
    def foo_compare(self):
        lst, addrs = self.lst, self.lst_addrs
        view = FOO[:5] + [""] + FOO[5:]      # blank line keeps the rows aligned with factorial
        foo = CodeListing(view, font_size=20, line_gap=0.31)
        foo.shift(np.array([-0.9 - foo.get_left()[0], lst[0].get_center()[1] - foo[0].get_center()[1], 0]))
        c = CodeListing([
            "int foo(int i) {",
            "  if (i == 0) return 0;",
            "  int a = i + foo(i-1);",
            "  return a;",
            "}",
        ], lang="c", font_size=20, line_gap=0.36)
        c.move_to([6.6, 3.5, 0], aligned_edge=UR).shift(DOWN * c[0].height / 2)
        self.say("笔记里的 foo 也是递归：foo(i) = i + foo(i − 1)。它的汇编和阶乘并排一看，骨架完全一样。",
                 FadeOut(addrs), FadeIn(foo, shift=LEFT * 0.2), FadeIn(c))
        self.hold()
        rows = [5, 6, 7, 12]
        boxes = VGroup(*[b for r in rows for b in (lst.line_box(r, color=RED_C, opacity=0.2),
                                                   foo.line_box(r, color=RED_C, opacity=0.2))])
        self.say("只有三处不同：直接和 x0 比较，省掉 li；基本情况返回 0；乘法换成加法。",
                 FadeIn(boxes))
        self.play(Indicate(foo.glyphs(6, "x0"), color=RED_B))
        self.hold()
        m = CodeListing(FOO_MAIN[:6], font_size=20, line_gap=0.31)
        m.next_to(c, DOWN, buff=0.45).align_to(c, LEFT)
        depth = VGroup(zh("foo(100) 最深时栈上有", 20, YELLOW_D),
                       zh("101 个栈帧，共 808 字节", 20, YELLOW_D)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        depth.next_to(m, DOWN, buff=0.3).align_to(c, LEFT)
        if depth.get_right()[0] > 6.9:
            depth.shift(LEFT * (depth.get_right()[0] - 6.9))
        self.say("笔记的 main 把 foo(3) 放进 s0，调用 foo(100) 后它还在。foo(100) 最深时压着 101 个栈帧，共 808 字节。",
                 FadeOut(boxes), FadeIn(m))
        self.play(Indicate(m[3], color=C_S), FadeIn(depth, shift=UP * 0.1))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ leaf functions
    def leaf(self):
        c = CodeListing([
            "int mult(int x, int y) {",
            "  return x * y;",
            "}",
            "int sum_square(int x, int y) {",
            "  return mult(x, x) + mult(y, y);",
            "}",
        ], lang="c", font_size=22, line_gap=0.42).to_corner(UL, buff=0.5)

        def node(name, color):
            return box_label(name, color, h=0.65, font_size=24, font=MONO)

        main = node("main", GREY_B)
        ss = node("sum_square", BLUE_C)
        m1, m2 = node("mult", GREEN_C), node("mult", GREEN_C)
        main.move_to(RIGHT * 3.8 + UP * 2.6)
        ss.move_to(RIGHT * 3.8 + UP * 1.1)
        VGroup(m1, m2).arrange(RIGHT, buff=0.8).move_to(RIGHT * 3.8 + DOWN * 0.4)
        edges = VGroup(Line(main.get_bottom(), ss.get_top(), buff=0.05, color=GREY_B),
                       Line(ss.get_bottom(), m1.get_top(), buff=0.05, color=GREY_B),
                       Line(ss.get_bottom(), m2.get_top(), buff=0.05, color=GREY_B))
        self.say("并非每个函数都需要栈。笔记里的 sum_square 调用两次 mult，而 mult 不再调用任何函数。",
                 FadeIn(c, shift=RIGHT * 0.2), FadeIn(main), FadeIn(ss), FadeIn(m1), FadeIn(m2), Create(edges))
        leaf_t = zh("叶子", 24, GREEN_B).next_to(VGroup(m1, m2), DOWN, buff=0.2)
        asm = CodeListing(["mult:", "    mul  a0, a0, a1", "    ret"], font_size=26, line_gap=0.48)
        asm.next_to(c, DOWN, buff=0.6).align_to(c, LEFT)
        note = zh("没有 sw，没有 lw，sp 一动不动", 24, GREEN_B).next_to(asm, DOWN, buff=0.35).align_to(c, LEFT)
        self.say("mult 这样的函数叫叶子函数：它没有 jal，ra 不会被覆盖；只用 t、a 寄存器的话，连一条 sw、lw 都不用。",
                 FadeIn(leaf_t), Indicate(m1, color=GREEN_B), Indicate(m2, color=GREEN_B))
        self.play(FadeIn(asm, shift=UP * 0.15))
        self.play(FadeIn(note))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ the full table
    def reg_table(self):
        data = [
            ("x0", "zero", "常数 0", "—"),
            ("x1", "ra", "返回地址", "调用者"),
            ("x2", "sp", "栈指针", "被调用者"),
            ("x3", "gp", "全局指针", "—"),
            ("x4", "tp", "线程指针", "—"),
            ("x5–7", "t0–2", "临时寄存器", "调用者"),
            ("x8", "s0 / fp", "保存寄存器 / 帧指针", "被调用者"),
            ("x9", "s1", "保存寄存器", "被调用者"),
            ("x10–11", "a0–1", "参数 / 返回值", "调用者"),
            ("x12–17", "a2–7", "参数", "调用者"),
            ("x18–27", "s2–11", "保存寄存器", "被调用者"),
            ("x28–31", "t3–6", "临时寄存器", "调用者"),
        ]
        xs = [-4.6, -2.7, -0.4, 3.9]
        head = VGroup(*[zh(s, 22, YELLOW_D).move_to([x, 3.45, 0], aligned_edge=LEFT)
                        for s, x in zip(["编号", "名字", "用途", "由谁保存"], xs)])
        rows = VGroup()
        for k, (num, name, use, saver) in enumerate(data):
            y = 2.95 - k * 0.405
            base = name.split()[0].split("–")[0]
            col = abi_color(base if base != "t0" else "t0")
            sv_col = C_T if saver == "调用者" else (C_S if saver == "被调用者" else GREY)
            rows.add(VGroup(
                mono(num, 22, GREY_A).move_to([xs[0], y, 0], aligned_edge=LEFT),
                mono(name, 22, col).move_to([xs[1], y, 0], aligned_edge=LEFT),
                zh(use, 22, WHITE).move_to([xs[2], y, 0], aligned_edge=LEFT),
                zh(saver, 22, sv_col).move_to([xs[3], y, 0], aligned_edge=LEFT),
            ))
        rule = Line([-4.8, 3.2, 0], [5.6, 3.2, 0], stroke_color=GREY_B, stroke_width=1.5)
        def row_box(k, color):
            return SurroundingRectangle(rows[k], color=color, buff=0.06, stroke_width=2.5)

        gt = VGroup(row_box(3, RED_C), row_box(4, RED_C))
        self.say("完整的寄存器约定表如下。gp 和 tp 另有专门用途，不归调用约定管，别去碰它们。",
                 FadeIn(head), Create(rule),
                 LaggedStart(*[FadeIn(r, shift=UP * 0.05) for r in rows], lag_ratio=0.06, run_time=1.6))
        self.play(Create(gt), rows[3].animate.set_opacity(0.45), rows[4].animate.set_opacity(0.45))
        self.hold()
        fp = row_box(6, C_S)
        self.say("s0 又叫 fp，即帧指针：sp 可能在函数中途移动，fp 则一直指着当前栈帧。",
                 FadeOut(gt), Create(fp))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ func_a
    def func_a(self):
        lst = place_listing(CodeListing(FUNC_A, font_size=20, line_gap=0.31), -5.6, 3.5)
        addrs = addr_col(lst, FUNC_A_ADDR)
        braces = VGroup(side_brace(lst, 1, 3, "序言", size=20), side_brace(lst, 6, 7, "存 t1", C_T, size=20),
                        side_brace(lst, 9, 10, "取回 t1", C_T, size=20), side_brace(lst, 13, 16, "尾声", size=20))
        regs = VGroup(
            RegBox("sp", hex32(SP_MAIN), width=1.65, font_size=20),
            RegBox("ra", "0x1008", width=1.65, font_size=20),
            RegBox("s0", 42, width=1.65, font_size=20),
            RegBox("t1", "—", width=1.65, font_size=20),
        ).arrange_in_grid(2, 2, buff=(0.45, 0.16)).to_corner(UR, buff=0.35)
        R = dict(zip(["sp", "ra", "s0", "t1"], regs))
        col = WordColumn(0xFFFFFFD8, 5, cell_w=2.1, cell_h=0.46, font_size=18)
        col.shift(np.array([4.45 - col.cells.get_center()[0], 1.6 - col.cells[0].get_center()[1], 0]))
        for k in range(2):
            col.cells[k].set_fill(GREY_D, 0.5)
        col.texts[0].become(zh("main 的数据", 18, GREY).move_to(col.cells[0]))
        sp = sp_pointer().next_to(col.cells[1], RIGHT, buff=0.08)

        def sp_to(addr):
            return sp.animate.next_to(col.cell(addr), RIGHT, buff=0.08)

        self.say("笔记里的 func_a 就在中途动了 sp：它要调用 func_b，调用前后都要用 t1。",
                 FadeIn(lst, shift=RIGHT * 0.2), FadeIn(addrs), FadeIn(regs), FadeIn(col), FadeIn(sp))
        self.play(LaggedStart(*[FadeIn(b) for b in braces], lag_ratio=0.2))
        self.hold()
        box = lst.line_box(1)

        def at(i, *anims, rt=0.45):
            self.play(box.animate.become(lst.line_box(i)), *anims, run_time=rt)

        fa = frame_brace(col, 2, 3, "func_a", BLUE_C)
        self.say("序言压 8 字节，存下 ra 和 s0。ra 本归调用者保存，但习惯上也在序言里存。", FadeIn(box))
        at(1, R["sp"].set(hex32(0xFFFFFFCC)), sp_to(0xFFFFFFCC), FadeIn(fa))
        at(2, col.set(0xFFFFFFCC, "ra = 0x1008", C_RA))
        at(3, col.set(0xFFFFFFD0, "s0 = 42", C_S))
        self.hold()
        tb = frame_brace(col, 4, 4, "t1", C_T)
        self.say("t1 = 10，s0 = 20。t1 归调用者保存，func_b 可能改掉它，所以调用前再压 4 字节存下 t1。")
        at(4, R["t1"].set(10))
        at(5, R["s0"].set(20))
        at(6, R["sp"].set(hex32(0xFFFFFFC8)), sp_to(0xFFFFFFC8), FadeIn(tb))
        at(7, col.set(0xFFFFFFC8, "t1 = 10", C_T))
        self.hold()
        fb = box_label("func_b", GREY_B, w=1.8, h=0.6, font_size=22, font=MONO)
        fb.next_to(lst.right_of(8, 1.9), RIGHT, buff=0)
        self.say("func_b 返回后，t1 里是什么已经说不准了。好在栈上有备份：取回 t1 = 10，马上弹掉这 4 字节。")
        at(8, R["ra"].set("0x3020"), FadeIn(fb, shift=LEFT * 0.2))
        self.play(R["t1"].set("???"))
        self.play(FadeOut(fb), run_time=0.4)
        at(9, R["t1"].set(10))
        at(10, R["sp"].set(hex32(0xFFFFFFCC)), sp_to(0xFFFFFFCC), tb.animate.set_opacity(0.3),
           col.texts[4].animate.set_opacity(0.35))
        self.hold()
        self.say("sp 一动，偏移就跟着变：刚才 0(sp) 是 t1，弹掉之后才又是 ra。",
                 Indicate(col.texts[3], color=C_RA))
        self.hold()
        self.say("最后 t1 = 15，s0 = 25。尾声取回 ra 和调用者的 s0 = 42，sp 复原，ret 返回。")
        at(11, R["t1"].set(15))
        at(12, R["s0"].set(25))
        at(13, R["ra"].set("0x1008"))
        at(14, R["s0"].set(42))
        at(15, R["sp"].set(hex32(SP_MAIN)), sp_to(SP_MAIN), fa.animate.set_opacity(0.3),
           col.texts[2].animate.set_opacity(0.35), col.texts[3].animate.set_opacity(0.35))
        at(16)
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ quiz
    def quiz(self):
        head = self.heading("判断题")
        qs = [
            ("函数返回后，t 寄存器可能变了，但 a 寄存器不会。", "错", RED_C),
            ("函数要用 s0–s11，必须先保存旧值，返回前恢复。", "对", GREEN_C),
            ("栈只能在函数的开头和结尾操作。", "错", RED_C),
        ]
        size = 24 if EN else 28     # the English statements run longer
        rows = VGroup()
        for k, (q, _, _) in enumerate(qs):
            rows.add(VGroup(mono(f"{k + 1}.", size, YELLOW_D), zh(q, size)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to(LEFT * 0.6 + UP * 0.6)
        if EN:
            rows.to_edge(LEFT, buff=0.7)
        marks = VGroup(*[zh(a, 32, col).next_to(r, RIGHT, buff=0.6).set_x(6.2 if EN else 5.8)
                         for r, (_, a, col) in zip(rows, qs)])
        self.say("三道判断题，取自笔记的练习。先自己想一想。", Write(head),
                 LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.3))
        self.hold(1.5)
        self.say("第 1 题错：a0、a1 要带回返回值。a 寄存器和 t 一样，都由调用者保存。",
                 FadeIn(marks[0], scale=1.4))
        self.say("第 2 题对：s 寄存器由被调用者保存，通常在序言里存、在尾声里恢复。", FadeIn(marks[1], scale=1.4))
        self.say("第 3 题错：func_a 就在中途压栈保存了 t1。只要压栈、弹栈配对，栈随时能用。",
                 FadeIn(marks[2], scale=1.4))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ six steps
    def six_steps(self):
        head = self.heading("六个步骤，再看一遍")
        steps = [
            ("1", "调用者", "要保留的 t、a 寄存器先存好；参数放进 a0–a7", C_T),
            ("2", "调用者", "jal ra, 函数名", C_T),
            ("3", "序言", "sp 减一次；保存要用的 s 寄存器，要调用别人就保存 ra", C_S),
            ("4", "函数体", "做该做的事", C_S),
            ("5", "尾声", "返回值放进 a0；恢复 ra 和 s 寄存器；sp 加回去", C_S),
            ("6", "尾声", "jr ra", C_S),
        ]
        rows = VGroup()
        for num, who, what, color in steps:
            who = tr(who)  # "prologue" is lower-case in the brace labels; capitalize it here
            r = VGroup(mono(num, 28, YELLOW_D), zh(who[:1].upper() + who[1:], 26, color), zh(what, 26))
            rows.add(r)
        for k, r in enumerate(rows):
            y = 2.4 - k * 0.62
            r[0].move_to([-6.2, y, 0], aligned_edge=LEFT)
            r[1].move_to([-5.6, y, 0], aligned_edge=LEFT)
            r[2].move_to([-3.7 if EN else -3.9, y, 0], aligned_edge=LEFT)
        proc = zh("RISC-V 手册里的“过程”（procedure），就是函数", 22, GREY_B).move_to([-6.2, -1.3, 0], aligned_edge=LEFT)
        self.say("最后，再过一遍第 7 集的六个步骤。第 1、2 步归调用者：存好还要用的 t、a 寄存器，放好参数，然后 jal。",
                 Write(head), FadeIn(proc),
                 LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows[:2]], lag_ratio=0.3))
        self.say("第 3 步序言：sp 只减一次，局部数组一并分配；存下要用的 s 寄存器，要调用别人就存 ra。",
                 FadeIn(rows[2], shift=RIGHT * 0.2))
        self.say("第 4 步是函数体；第 5、6 步是尾声：返回值放进 a0，恢复寄存器、弹栈帧，jr ra。",
                 LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows[3:]], lag_ratio=0.3))
        self.hold()
        self.play(FadeOut(rows), FadeOut(proc))

        pairs = [
            ("桌子", "寄存器"), ("壁橱", "内存"), ("父母", "调用者"), ("你", "被调用者"),
            ("父母备在桌上的东西", "参数"), ("你留下的礼物", "返回值"),
        ]
        grid = VGroup()
        for a, b in pairs:
            grid.add(VGroup(zh(a, 26, GOLD_B), mono("→", 26, GREY_B), zh(b, 26, BLUE_B)).arrange(RIGHT, buff=0.3))
        grid.arrange_in_grid(3, 2, buff=(1.2, 0.5), col_alignments="ll").move_to(UP * 1.0)
        self.say("笔记的比喻：调用函数就像替父母看家。父母是调用者，你是被调用者；桌子是寄存器，壁橱是内存。",
                 LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in grid[:4]], lag_ratio=0.2))
        self.say("父母备在桌上的是参数。桌上别的东西，先收进壁橱（序言）；走前原样摆回，再留一份礼物：返回值（尾声）。",
                 LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in grid[4:]], lag_ratio=0.3))
        self.hold()
