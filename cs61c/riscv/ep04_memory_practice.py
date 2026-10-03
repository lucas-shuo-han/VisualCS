import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403


# ---------------------------------------------------------------- a tiny RV32 model
# Every value shown on screen is checked against this model (asserts below).

def _reg(regs, r):
    return 0 if r in ("x0", "zero") else regs[r]


def _sx(v, bits):
    v &= (1 << bits) - 1
    return v - (1 << bits) if v >> (bits - 1) else v


def run(lines, regs, mem):
    """Execute asm lines (the subset used in this episode) on regs/mem (dicts,
    mem is byte-addressed). Returns a snapshot of regs after every line."""
    trace = []
    for line in lines:
        op, *args = line.split("#")[0].replace(",", " ").split()

        def ea(s):
            off, base = s.rstrip(")").split("(")
            return (_reg(regs, base) + int(off, 0)) & 0xFFFFFFFF

        def rd_set(v):
            if args[0] not in ("x0", "zero"):
                regs[args[0]] = v & 0xFFFFFFFF

        if op == "li":
            rd_set(int(args[1], 0))
        elif op in ("add", "sub"):
            a, b = _reg(regs, args[1]), _reg(regs, args[2])
            rd_set(a + b if op == "add" else a - b)
        elif op == "addi":
            rd_set(_reg(regs, args[1]) + int(args[2], 0))
        elif op == "slli":
            rd_set(_reg(regs, args[1]) << int(args[2], 0))
        elif op in ("sw", "sb"):
            n = 4 if op == "sw" else 1
            a, v = ea(args[1]), _reg(regs, args[0])
            for k in range(n):
                mem[a + k] = (v >> (8 * k)) & 0xFF
        elif op in ("lw", "lb", "lbu"):
            a = ea(args[1])
            if op == "lw":
                rd_set(sum(mem[a + k] << (8 * k) for k in range(4)))
            else:
                rd_set(_sx(mem[a], 8) if op == "lb" else mem[a])
        else:
            raise ValueError(op)
        trace.append(dict(regs))
    return trace


# ---------------------------------------------------------------- facts (checked)
SP = 0x1000

# assembly vs C: the same 32 bits read two ways
assert _sx(0xFFFFFFFF, 32) == -1 and 0xFFFFFFFF == 4294967295

# f = (g + h) - (i + j), notes' register mapping f,g,h,i,j -> x19..x23
G, H, I, J = 10, 20, 3, 4
APPROACH_A = ["add  x5, x20, x21", "add  x6, x22, x23", "sub x19,  x5,  x6"]
APPROACH_B = ["add x19, x20, x21", "sub x19, x19, x22", "sub x19, x19, x23"]
_start = {"x19": 0, "x20": G, "x21": H, "x22": I, "x23": J, "x5": 42, "x6": 61}
TA = run(APPROACH_A, dict(_start), {})
TB = run(APPROACH_B, dict(_start), {})
assert [TA[0]["x5"], TA[1]["x6"], TA[2]["x19"]] == [30, 7, 23]
assert [t["x19"] for t in TB] == [30, 27, 23] and TB[-1]["x5"] == 42 and TB[-1]["x6"] == 61
assert (G + H) - (I + J) == 23 and ABI_NAMES[5] == "t0" and ABI_NAMES[6] == "t1"

# the stack-array example (notes, "Example: Stack Arrays")
C_SRC = [
    "int a = 5;",
    'char b[] = "string";  // 数组会存放在栈上',
    "int c[10];",
    "uint8_t d = b[3];",
    "c[4] = a+d;",
    "c[a] = 20;",
]
C_SHORT = [s.split("  //")[0] for s in C_SRC]
CHUNKS = [
    ["li  t0, 5          # R[t0] = 5",
     "sw  t0, 0(sp)      # a"],
    ["li  t0, 0x69727473   # \"stri\"",
     "sw  t0, 4(sp)",
     "li  t1, 0x0000676E   # \"ng\\0\" + 0",
     "sw  t1, 8(sp)"],
    [],
    ["lb  t0, 7(sp)      # b[3]: 4+3",
     "sb  t0, 52(sp)     # d"],
    ["lw  t0, 0(sp)      # a",
     "lbu t1, 52(sp)     # d",
     "add t2, t0, t1     # R[t2] = a+d",
     "sw  t2, 28(sp)     # c[4]: 12+16"],
    ["li   t0, 20        # R[t0] = 20",
     "lw   t1, 0(sp)     # R[t1] = a",
     "slli t1, t1, 2     # a*4 = a<<2",
     "addi t1, t1, 12    # + 12 (c)",
     "add  t1, t1, sp    # &c[a]",
     "sw   t0, 0(t1)     # c[a] = 20"],
]
STACK_ASM = [ln for ch in CHUNKS for ln in ch]
assert len(STACK_ASM) == 18
STRING = b"string\0"
assert list(STRING) == [0x73, 0x74, 0x72, 0x69, 0x6E, 0x67, 0x00]
W0 = int.from_bytes(STRING[:4], "little")
W1 = int.from_bytes(STRING[4:] + b"\0", "little")
assert (W0, W1) == (0x69727473, 0x0000676E)
TEDIOUS = []
for k, ch in enumerate(STRING[:6]):
    TEDIOUS += [f"li t0, 0x{ch:02X}", f"sb t0, {4 + k}(sp)"]
TEDIOUS.append("sb x0, 10(sp)")
assert len(TEDIOUS) == 13
LAYOUT = {"a": 0, "b": 4, "c": 12, "d": 52}
assert LAYOUT["b"] + len(STRING) == 11 and LAYOUT["c"] % 4 == 0 and LAYOUT["c"] + 40 == LAYOUT["d"]

_mem_t = {}
TR = run(STACK_ASM, {"sp": SP, "t0": 0, "t1": 0, "t2": 0}, _mem_t)
_tm = {}
run(TEDIOUS, {"sp": SP, "t0": 0}, _tm)
assert [_tm[SP + 4 + k] for k in range(7)] == list(STRING)
# state after each instruction, as displayed
assert TR[0]["t0"] == 5
assert TR[2]["t0"] == 0x69727473 and TR[4]["t1"] == 0x676E
assert [_mem_t[SP + 4 + k] for k in range(7)] == list(STRING)
assert LAYOUT["b"] + 3 == 7 and TR[6]["t0"] == 0x69 == ord("i")       # lb: top bit 0
assert _mem_t[SP + 52] == 0x69
assert TR[8]["t0"] == 5 and TR[9]["t1"] == 105 and TR[10]["t2"] == 110 == 0x6E == ord("n")
assert LAYOUT["c"] + 4 * 4 == 28 and _mem_t[SP + 28] == 0x6E
assert TR[12]["t0"] == 20 and TR[13]["t1"] == 5
assert TR[14]["t1"] == 20 and bin(5) == "0b101" and bin(20) == "0b10100"
assert TR[15]["t1"] == 32 == 0x20 and TR[16]["t1"] == SP + 32 == 0x1020
assert [_mem_t[SP + 32 + k] for k in range(4)] == [0x14, 0, 0, 0]      # c[5] = 20
assert 12 + 4 * 5 == 32                                                  # &c[a] - sp

# notes, Example 1
EX1 = ["li x11, 0x93F5", "sw x11, 0(x5)", "lb x12, 1(x5)"]
_m1 = {}
T1 = run(EX1, {"x5": 0x100, "x11": 0, "x12": 0}, _m1)
assert T1[0]["x11"] == 0x000093F5
assert [_m1[0x100 + k] for k in range(4)] == [0xF5, 0x93, 0x00, 0x00]
assert _m1[0x101] == 0x93 == 0b10010011 and T1[2]["x12"] == 0xFFFFFF93

# notes, Example 2: *x = *y, x in x3, y in x5
PX, PY, VX, VY = 0x108, 0x100, 7, 42
_m2 = {PY + k: (VY >> 8 * k) & 0xFF for k in range(4)}
_m2.update({PX + k: (VX >> 8 * k) & 0xFF for k in range(4)})
T2 = run(["lw x8, 0(x5)", "sw x8, 0(x3)"], {"x3": PX, "x5": PY, "x8": 0}, _m2)
assert T2[0]["x8"] == 42 and [_m2[PX + k] for k in range(4)] == [42, 0, 0, 0]
CANDIDATES = [
    "add x3, x5, zero",
    "add x5, x3, zero",
    "lw  x3, 0(x5)",
    "lw  x5, 0(x3)",
    "lw  x8, 0(x5)",
    "sw  x8, 0(x3)",
    "lw  x5, 0(x8)",
    "sw  x3, 0(x8)",
]

VAR_COL = {"a": BLUE_C, "b": GREEN_C, "c": GOLD_C, "d": PURPLE_B}


class Ep04MemoryPractice(NarratedScene):
    def construct(self):
        self.title_card()
        self.assembly_vs_c()
        self.warmup()
        self.load_store()
        self.stack_array()
        self.example_one()
        self.example_two()
        self.fine_print()
        self.end_card(
            [
                "寄存器没有类型：指令决定怎样解读比特",
                "一行一条指令；表达式要拆开，可借用临时寄存器",
                "从内存 load，往内存 store；运算只在寄存器上做",
                "元素地址 = 基地址 + 下标 × 大小；变量下标要在寄存器里算",
                "load 要填满 32 位（lb 符号扩展），store 无需扩展",
            ],
        )

    # ------------------------------------------------------------------ assembly vs C
    def assembly_vs_c(self):
        c = CodeListing(C_SHORT, lang="c", font_size=30, line_gap=0.55)
        asm = CodeListing(STACK_ASM[:4] + ["..."], font_size=30, line_gap=0.55)
        arrow = Arrow(LEFT * 0.7, RIGHT * 0.7, color=GREY_B)
        pre = VGroup(c, arrow, asm).arrange(RIGHT, buff=0.6)
        if pre.width > 12.6:
            pre.scale_to_fit_width(12.6)
        pre.move_to(UP * 0.5)
        self.say("这一集是练习课：亲手把 C 代码翻译成 RISC-V 汇编。",
                 FadeIn(c, shift=RIGHT * 0.2), GrowArrow(arrow), FadeIn(asm, shift=LEFT * 0.2))
        self.hold()
        self.clear_stage(run_time=0.6)

        head = self.heading("汇编 vs. C")
        rows = [
            ("变量要声明，有类型", "寄存器没有类型，只有比特"),
            ("类型决定运算", "指令决定怎样解读比特"),
            ("一个运算符，多种运算", "指令名与运算一一对应"),
            ("一条语句，多个运算", "一行只有一条指令"),
        ]
        hdr = VGroup(zh("C / Java", 26, GREY_B), zh("RISC-V 汇编", 26, GREY_B))
        hdr[0].move_to([-3.4, 2.6, 0])
        hdr[1].move_to([3.4, 2.6, 0])
        rule = Line([-6.6, 2.3, 0], [6.6, 2.3, 0], stroke_color=GREY, stroke_width=1.5)
        mid = Line([0, 2.8, 0], [0, 0.1, 0], stroke_color=GREY, stroke_width=1.5)
        table = VGroup()
        for k, (l, r) in enumerate(rows):
            y = 1.95 - 0.55 * k
            num = mono(f"{k + 1}", 24, YELLOW_D).move_to([-6.45, y, 0])
            lt = zh(l, 24).move_to([-3.4, y, 0])
            rt = zh(r, 24, YELLOW_D).move_to([3.4, y, 0])
            table.add(VGroup(num, lt, rt))
        self.play(Write(head), FadeIn(hdr), Create(rule), Create(mid))
        self.say("先对比汇编和 C。第一，C 的变量有类型；寄存器没有类型，只是 32 个比特。",
                 FadeIn(table[0], shift=UP * 0.1))

        # 1 & 2: the operation decides how the bits are read
        reg = RegBox("t0", "0xFFFFFFFF", width=2.8, font_size=28).move_to(DOWN * 0.75)
        s_lab = zh("有符号：−1", 26, BLUE_B).move_to([-3.2, -1.85, 0])
        u_lab = zh("无符号：4294967295", 26, GREEN_B).move_to([3.4, -1.85, 0])
        a1 = Arrow(reg.box.get_bottom() + LEFT * 0.4, s_lab.get_top(), buff=0.12, color=BLUE_B)
        a2 = Arrow(reg.box.get_bottom() + RIGHT * 0.4, u_lab.get_top(), buff=0.12, color=GREEN_B)
        self.say("第二，C 由类型决定运算；汇编反过来，由指令决定怎样解读这些比特。",
                 FadeIn(table[1], shift=UP * 0.1), FadeIn(reg))
        self.say("比如 t0 全是 1：当成有符号数是 −1，当成无符号数就是 4294967295，全看指令怎么用。",
                 GrowArrow(a1), FadeIn(s_lab), GrowArrow(a2), FadeIn(u_lab))
        self.hold()
        self.play(FadeOut(VGroup(reg, s_lab, u_lab, a1, a2)))

        # 3: one operator, several operations
        code = CodeListing(["int *p = …;", "p = p + 2;", "int x = 42;", "x = 3 * x + *p + 4;"],
                           lang="c", font_size=24, line_gap=0.44).move_to([-3.6, -1.0, 0])
        plus_p = SurroundingRectangle(code.glyphs(1, "+"), color=GOLD_B, buff=0.05)
        lab_p = zh("指针运算", 22, GOLD_B).next_to(code.right_of(1), RIGHT, buff=0.2)
        marks = VGroup(
            SurroundingRectangle(code.glyphs(3, "*", 0), color=GREEN_B, buff=0.05),
            SurroundingRectangle(code.glyphs(3, "+", 0), color=BLUE_B, buff=0.05),
            SurroundingRectangle(code.glyphs(3, "*", 1), color=RED_B, buff=0.05),
        )
        lab_x = VGroup(zh("乘法", 22, GREEN_B), zh("·", 22, GREY_B), zh("整数加法", 22, BLUE_B),
                       zh("·", 22, GREY_B), zh("解引用", 22, RED_B)).arrange(RIGHT, buff=0.12)
        lab_x.next_to(code.right_of(3), RIGHT, buff=0.2)
        self.say("第三，C 的运算符有多种含义：第 2 行的 + 是指针运算，第 4 行的 + 是整数加法，两个 * 是乘法和解引用。",
                 FadeIn(table[2], shift=UP * 0.1), FadeIn(code, shift=UP * 0.1))
        self.play(Create(plus_p), FadeIn(lab_p))
        self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.3), FadeIn(lab_x))
        addi = CodeListing(["addi s0, s0, 8   # p = p + 2"], font_size=24)
        addi.next_to(code.right_of(1), RIGHT, buff=0.35)
        self.say("汇编里指令名和运算一一对应，字节数得自己算：p + 2 前进 8 字节，就写 addi 加 8。",
                 FadeOut(lab_p), FadeIn(addi, shift=LEFT * 0.2))
        self.play(Circumscribe(addi.glyphs(0, "8", 0), color=GOLD_B))
        self.hold()
        self.play(FadeOut(VGroup(code, plus_p, marks, lab_x, addi)))

        # 4: one instruction per line
        stmt = CodeListing(["a = b * 2 - (arr[2] + *p);"], lang="c", font_size=30).move_to(DOWN * 0.8)
        six = zh("≈ 6 条指令", 28, YELLOW_D).next_to(stmt, DOWN, buff=0.4)
        self.say("第四，C 的一条语句可以有多个运算，汇编一行只有一条指令。这一行大约要六条。",
                 FadeIn(table[3], shift=UP * 0.1), FadeIn(stmt, shift=UP * 0.1))
        self.play(FadeIn(six, shift=UP * 0.1))
        self.hold()
        self.play(FadeOut(VGroup(stmt, six)))

        cm = CodeListing([
            "# f = (g + h) - (i + j)",
            "add x5, x20, x21     # x5 = g + h",
        ], font_size=26, line_gap=0.5).move_to(DOWN * 1.0)
        self.say("汇编里也没有变量名，所以注释很重要：# 到行尾都是注释，没有多行注释。",
                 FadeIn(cm, shift=UP * 0.1))
        self.play(Circumscribe(cm.glyphs(0, "#"), color=YELLOW_D),
                  Circumscribe(cm.glyphs(1, "#"), color=YELLOW_D))
        self.hold()
        self.clear_stage(run_time=0.6)

    # ------------------------------------------------------------------ (g + h) - (i + j)
    def warmup(self):
        c = CodeListing(["f = (g + h) - (i + j);"], lang="c", font_size=34).move_to(UP * 2.95)
        specs = [("x20", G, "g"), ("x21", H, "h"), ("x22", I, "i"), ("x23", J, "j")]
        row1 = VGroup(*[RegBox(n, v, color=C_S, width=1.1, font_size=24) for n, v, _ in specs])
        row1.arrange(RIGHT, buff=0.9).move_to(DOWN * 0.45)
        row2 = VGroup(
            RegBox("x5", 42, color=C_T, width=1.1, font_size=24),
            RegBox("x6", 61, color=C_T, width=1.1, font_size=24),
            RegBox("x19", "?", color=C_S, width=1.1, font_size=24),
        ).arrange(RIGHT, buff=0.9).move_to(DOWN * 1.6)
        R = {b.label.text: b for b in [*row1, *row2]}
        tags = VGroup(*[mono(t, 24, GREY_A).next_to(R[n].box, UP, buff=0.08) for n, _, t in specs])
        tags.add(mono("f", 24, GREY_A).next_to(R["x19"].box, UP, buff=0.08))
        self.say("先热身：f = (g + h) - (i + j)，g 到 j 在 x20 到 x23 里，f 放进 x19。",
                 FadeIn(c, shift=DOWN * 0.2), FadeIn(row1), FadeIn(row2), FadeIn(tags))

        la = CodeListing(APPROACH_A, font_size=26, line_gap=0.45)
        lb = CodeListing(APPROACH_B, font_size=26, line_gap=0.45)
        la.move_to([-3.3, 0.95, 0])
        lb.move_to([3.3, 0.95, 0])
        ta = zh("写法 A", 26, YELLOW_D).next_to(la, UP, buff=0.25)
        tb = zh("写法 B", 26, YELLOW_D).next_to(lb, UP, buff=0.25)
        box = la.line_box(0)
        self.say("写法 A 照着 C 的顺序，把两个括号先算进临时寄存器 x5 和 x6，再相减得 23。但它们原来的值被覆盖了。",
                 FadeIn(ta), FadeIn(la), FadeIn(box))
        self.play(R["x5"].set(30))
        self.play(box.animate.become(la.line_box(1)), R["x6"].set(7))
        self.play(box.animate.become(la.line_box(2)), R["x19"].set(23))
        old = VGroup(mono("42", 22, RED_B), mono("61", 22, RED_B))
        for o, n in zip(old, ["x5", "x6"]):
            o.next_to(R[n].box, DOWN, buff=0.12)
        strike = VGroup(*[Line(o.get_left(), o.get_right(), color=RED_B, stroke_width=3) for o in old])
        self.play(FadeOut(box), FadeIn(old), Create(strike),
                  Indicate(R["x5"], color=RED_B), Indicate(R["x6"], color=RED_B))
        self.hold()

        box = lb.line_box(0)
        self.say("写法 B 从同样的初值出发，利用代数：先算 g + h，再依次减去 i 和 j。",
                 FadeOut(old), FadeOut(strike), R["x5"].set(42), R["x6"].set(61), R["x19"].set("?"),
                 FadeIn(tb), FadeIn(lb), FadeIn(box))
        self.play(R["x19"].set(30))
        self.play(box.animate.become(lb.line_box(1)), R["x19"].set(27))
        self.play(box.animate.become(lb.line_box(2)), R["x19"].set(23))
        self.say("同样得 23，且没动 x5、x6。代价是要做代数变形，式子复杂了（比如展开乘法）就得靠更聪明的编译器。",
                 FadeOut(box), Circumscribe(VGroup(R["x5"], R["x6"]), color=GREEN_B))
        self.hold()
        self.clear_stage(run_time=0.6)

    # ------------------------------------------------------------------ load / store
    def load_store(self):
        head = self.heading("访问内存：load 与 store")
        cpu = RoundedRectangle(corner_radius=0.15, width=3.4, height=3.0, stroke_color=BLUE_C,
                               fill_color=BLUE_C, fill_opacity=0.08).move_to([-4.0, 0.2, 0])
        cpu_t = zh("处理器", 26, BLUE_B).next_to(cpu.get_top(), DOWN, buff=0.2)
        cells = VGroup(*[Rectangle(width=0.3, height=0.22, stroke_color=BLUE_B, stroke_width=1.2,
                                   fill_color=BLUE_C, fill_opacity=0.35) for _ in range(32)])
        cells.arrange_in_grid(4, 8, buff=0.05).next_to(cpu_t, DOWN, buff=0.15)
        mem = Rectangle(width=3.4, height=3.6, stroke_color=GREEN_C, fill_color=GREEN_C,
                        fill_opacity=0.06).move_to([3.9, 0.2, 0])
        mem_t = zh("内存", 26, GREEN_B).next_to(mem.get_top(), DOWN, buff=0.2)
        slots = VGroup(*[Rectangle(width=0.55, height=0.26, stroke_color=GREEN_C, stroke_width=1,
                                   stroke_opacity=0.5) for _ in range(40)])
        slots.arrange_in_grid(8, 5, buff=0.05).next_to(mem_t, DOWN, buff=0.15)
        extra = VGroup(*[Square(0.22, stroke_width=0, fill_color=GOLD_C, fill_opacity=0.9)
                         for _ in range(12)])
        extra.arrange_in_grid(2, 6, buff=0.14).next_to(cells, DOWN, buff=0.3)
        self.say("寄存器只有 32 个，变量再多也不怕：放不下的就“溢出”（spill）到内存里。",
                 Write(head), FadeIn(cpu), FadeIn(cpu_t), FadeIn(cells), FadeIn(mem), FadeIn(mem_t),
                 FadeIn(slots))
        self.play(LaggedStart(*[FadeIn(e, scale=0.5) for e in extra], lag_ratio=0.05))
        self.play(LaggedStart(*[e.animate.move_to(slots[k + 10]) for k, e in enumerate(extra)],
                              lag_ratio=0.06, run_time=1.6))

        addr = Arrow(cpu.get_right() + UP * 0.9, mem.get_left() + UP * 0.9, buff=0.1, color=GREY_B)
        addr_t = zh("地址", 22, GREY_B).next_to(addr, UP, buff=0.08)
        load = Arrow(mem.get_left() + UP * 0.05, cpu.get_right() + UP * 0.05, buff=0.1, color=YELLOW_D)
        load_t = mono("load from memory", 22, YELLOW_D).next_to(load, UP, buff=0.08)
        store = Arrow(cpu.get_right() + DOWN * 0.9, mem.get_left() + DOWN * 0.9, buff=0.1, color=TEAL_C)
        store_t = mono("store to memory", 22, TEAL_C).next_to(store, DOWN, buff=0.08)
        self.say("处理器靠地址访问内存。方向以处理器为准：读进来叫 load from，写出去叫 store to。",
                 GrowArrow(addr), FadeIn(addr_t))
        self.play(GrowArrow(load), FadeIn(load_t), GrowArrow(store), FadeIn(store_t))
        self.hold()
        self.play(FadeOut(VGroup(cpu, cpu_t, cells, mem, mem_t, slots, extra, addr, addr_t,
                                 load, load_t, store, store_t)))

        steps = VGroup(
            box_label("① load 进寄存器", YELLOW_D, h=0.75, font_size=26),
            box_label("② 在寄存器上运算", BLUE_C, h=0.75, font_size=26),
            box_label("③ store 回内存（如需要）", TEAL_C, h=0.75, font_size=26),
        ).arrange(RIGHT, buff=0.6)
        if steps.width > 13.0:
            steps.scale_to_fit_width(13.0)
        steps.move_to(UP * 1.9)
        arrows = VGroup(*[Arrow(steps[k].get_right(), steps[k + 1].get_left(), buff=0.08,
                                color=GREY_B, max_tip_length_to_length_ratio=0.3)
                          for k in range(2)])
        self.say("RISC-V 是“加载-存储”架构，只在寄存器上运算：内存里的数先 load，算完需要时再 store 回去。",
                 LaggedStart(FadeIn(steps[0]), GrowArrow(arrows[0]), FadeIn(steps[1]),
                             GrowArrow(arrows[1]), FadeIn(steps[2]), lag_ratio=0.3))
        x86_t = zh("x86（CISC）", 26, GREY_B).move_to([-3.4, 0.5, 0])
        x86 = mono("add eax, [ebx+8]", 30, C_TEXT, t2c={"add": C_MNEM, "8": C_NUM})
        x86.next_to(x86_t, DOWN, buff=0.45)
        x86_n = zh("一条指令：读内存 + 相加", 22, GREY_A).next_to(x86, DOWN, buff=0.35)
        rv_t = zh("RISC-V", 26, GREY_B).move_to([3.4, 0.5, 0])
        rv = CodeListing(["lw  t0, 8(s1)", "add a0, a0, t0"], font_size=30, line_gap=0.5)
        rv.next_to(rv_t, DOWN, buff=0.35)
        sep = Line([0, 0.8, 0], [0, -2.1, 0], stroke_color=GREY, stroke_width=1.5)
        self.say("x86 则允许一个操作数直接来自内存，一条 add 就够了；RISC-V 得拆成 lw 和 add 两条。",
                 FadeIn(x86_t), FadeIn(x86), FadeIn(x86_n), Create(sep), FadeIn(rv_t), FadeIn(rv))
        self.hold()
        self.play(FadeOut(VGroup(steps, arrows, x86_t, x86, x86_n, rv_t, rv, sep)))

        # base + offset mirrors arrays and structs
        words = VGroup(*[
            VGroup(Rectangle(width=1.5, height=0.55, stroke_color=GOLD_C, fill_color=GOLD_C,
                             fill_opacity=0.12), mono(f"A[{k}]", 22, GOLD_B))
            for k in range(4)
        ]).arrange(RIGHT, buff=0).move_to(UP * 1.7)
        for w in words:
            w[1].move_to(w[0])
        base = VGroup(mono("s0", 26, C_S), Arrow(DOWN * 0.55, ORIGIN, buff=0, color=C_S))
        base[0].next_to(base[1], DOWN, buff=0.05)
        base.next_to(words[0].get_corner(DL), DOWN, buff=0.02)
        brace = BraceBetweenPoints(words[0].get_corner(UL), words[3].get_corner(UL), UP, color=YELLOW_D)
        brace_t = zh("偏移量 12 字节", 22, YELLOW_D).next_to(brace, UP, buff=0.08)
        r1 = VGroup(CodeListing(["x = A[3];"], lang="c", font_size=28), mono("→", 28, GREY_B),
                    CodeListing(["lw t0, 12(s0)"], font_size=28)).arrange(RIGHT, buff=0.4)
        r2 = VGroup(CodeListing(["x = p->y;"], lang="c", font_size=28), mono("→", 28, GREY_B),
                    CodeListing(["lw t0, 4(s0)"], font_size=28)).arrange(RIGHT, buff=0.4)
        r1.move_to([-2.4, 0.05, 0])
        r2.move_to(r1, aligned_edge=LEFT).shift(DOWN * 0.95)
        n1 = zh("s0 = A 的基地址", 22, GREY_A).next_to(r1, RIGHT, buff=0.5)
        n2 = zh("s0 = p，成员 y 的偏移量是 4", 22, GREY_A).next_to(r2, RIGHT, buff=0.5)
        n2.align_to(n1, LEFT)
        self.say("“基地址 + 偏移量”是照着数组和结构体设计的：基地址指向开头，偏移量是固定的字节距离，汇编时确定。",
                 FadeIn(words), FadeIn(base), GrowFromCenter(brace), FadeIn(brace_t),
                 FadeIn(r1), FadeIn(n1))
        self.play(FadeIn(r2), FadeIn(n2))
        self.play(Circumscribe(r1[2].glyphs(0, "12"), color=YELLOW_D),
                  Circumscribe(r2[2].glyphs(0, "4"), color=YELLOW_D))
        self.hold()
        self.clear_stage(run_time=0.6)

    # ------------------------------------------------------------------ the stack-array example
    def stack_array(self):
        head = self.heading("大例子：栈上的数组")
        big = CodeListing(C_SRC, lang="c", font_size=26, line_gap=0.52).move_to(UP * 0.95)
        chips = VGroup(*[box_label(n, C_T if n != "sp" else C_SP, w=1.2, h=0.62, font_size=28, font=MONO)
                         for n in ("t0", "t1", "t2", "sp")]).arrange(RIGHT, buff=0.35)
        chips.move_to(DOWN * 1.35)
        self.say("今天的大例子：四个局部变量，两个是数组。规定只能用 t0、t1、t2 和栈指针 sp，内存随便用。",
                 Write(head), FadeIn(big, shift=UP * 0.2))
        self.play(LaggedStart(*[FadeIn(ch, shift=UP * 0.15) for ch in chips], lag_ratio=0.15))
        sp_note = zh("sp = x2：栈指针", 26, C_SP).next_to(chips, DOWN, buff=0.3)
        bad = CodeListing(["add x2, t0, t1"], font_size=26).next_to(chips, RIGHT, buff=0.6)
        bad_x = Cross(bad, stroke_color=RED_C, stroke_width=4)
        self.say("sp 就是 x2，指向存放局部变量的栈。这是约定：谁拿 x2 当临时寄存器，靠 sp 的访存就全乱了。",
                 Indicate(chips[3], color=C_SP), FadeIn(sp_note, shift=UP * 0.1))
        self.play(FadeIn(bad), Create(bad_x))
        self.hold()

        # ---- layout
        cl = CodeListing(C_SHORT, lang="c", font_size=20, line_gap=0.36)
        cl.move_to([-1.9, 3.5, 0], aligned_edge=UL)
        mem = MemoryView(SP, 14, 4, cell_w=0.6, cell_h=0.34, font_size=18)
        for o in mem.offsets:
            o.become(mono(o.text, 14, GREY).move_to(o))
        mem.shift(np.array([-5.85, 3.2, 0]) - mem.cells[0].get_corner(UL))
        for r, lab in enumerate(mem.addr_labels):
            lab.become(mono(f"sp+{4 * r}", 18, GREY_B).next_to(mem.cells[4 * r], LEFT, buff=0.15))
        self.mem = mem
        names = ["a", "b[0..3]", "b[4..6]"] + [f"c[{k}]" for k in range(10)] + ["d"]
        cols = [VAR_COL["a"], VAR_COL["b"], VAR_COL["b"]] + [VAR_COL["c"]] * 10 + [VAR_COL["d"]]
        vlabs = VGroup(*[mono(n, 18, col).next_to(mem.cells[4 * r + 3], RIGHT, buff=0.15)
                         for r, (n, col) in enumerate(zip(names, cols))])
        regs = VGroup(*[RegBox(n, "?", width=2.0, font_size=20) for n in ("t0", "t1", "t2")],
                      RegBox("sp", "0x1000", width=2.0, font_size=20))
        regs.arrange(DOWN, buff=0.16)
        for b in regs[1:]:
            b.shift(RIGHT * (regs[0].box.get_center()[0] - b.box.get_center()[0]))
        regs.shift(np.array([5.7, 3.15, 0]) - regs[0].box.get_center())
        self.R = dict(zip(["t0", "t1", "t2", "sp"], regs))
        self.say("变量放哪儿由我们这个“人肉编译器”决定，前后一致就行。左边是相对 sp 的偏移量。",
                 FadeOut(head), FadeOut(chips), FadeOut(sp_note), FadeOut(bad), FadeOut(bad_x),
                 ReplacementTransform(big, cl), FadeIn(mem), FadeIn(regs))
        setup = CodeListing([
            "int a        0(sp)",
            "char b[7]    4(sp)",
            "int c[10]   12(sp)",
            "uint8_t d   52(sp)",
        ], lang="c", font_size=24, line_gap=0.46).move_to([-1.9, 0.9, 0], aligned_edge=UL)

        def region(var, lo, hi):
            return [mem.cells[i].animate.set_fill(VAR_COL[var], 0.3) for i in range(lo, hi)]

        self.say("a 放在 0(sp)；b 是 \"string\" 加结尾的 \\0，共 7 字节，从 4(sp) 开始。",
                 FadeIn(setup[0]), FadeIn(setup[1]), *region("a", 0, 4), *region("b", 4, 11),
                 FadeIn(vlabs[:3]))
        self.say("c 是 10 个 int，共 40 字节，占 12(sp) 到 51(sp)；d 只有 1 字节，放在 52(sp)。",
                 FadeIn(setup[2]), FadeIn(setup[3]), *region("c", 12, 52), *region("d", 52, 53),
                 FadeIn(vlabs[3:]))
        pad = SurroundingRectangle(mem.cells[11], color=RED_B, buff=0.02)
        self.say("c 从 12(sp) 而不是 11(sp) 开始，这样每个 int 都对齐到 4 的倍数。",
                 Create(pad), Indicate(mem.addr_labels[3], color=GOLD_B))
        self.hold()
        self.play(FadeOut(pad), FadeOut(setup))
        self.cl = cl
        self.walk()

    # ---- helpers for the walk-through
    def chunk(self, i):
        lst = CodeListing(CHUNKS[i], font_size=20, line_gap=0.4)
        lst.move_to([-1.9, 1.05, 0], aligned_edge=UL)
        return lst

    def calc(self, *mobs, y=0.35):
        g = VGroup(*mobs).arrange(DOWN, buff=0.18)
        g.move_to([5.35, y, 0], aligned_edge=UP)
        return g

    def store(self, reg, addr, value, n=4, color=TEAL_C):
        mem = self.mem
        target = mem.word(addr) if n == 4 else mem.cell(addr)
        hl = SurroundingRectangle(target, color=color, buff=0.02)
        v = reg.val.copy()
        self.play(Create(hl), v.animate.move_to(target.get_center()).scale(0.8), run_time=0.9)
        anim = mem.set_word(addr, value) if n == 4 else mem.set_byte(addr, value)
        self.play(FadeOut(v), anim, run_time=0.6)
        self.play(FadeOut(hl), run_time=0.3)

    def load(self, reg, addr, shown, n=4, color=YELLOW_D, keep=False):
        mem = self.mem
        target = mem.word(addr) if n == 4 else mem.cell(addr)
        texts = mem.word_texts(addr) if n == 4 else VGroup(mem.text(addr))
        hl = SurroundingRectangle(target, color=color, buff=0.02)
        self.play(Create(hl), run_time=0.4)
        fly = texts.copy()
        self.play(fly.animate.arrange(RIGHT, buff=0.08).move_to(reg.box), run_time=0.9)
        self.play(FadeOut(fly), reg.set(shown), run_time=0.6)
        if keep:
            return hl
        self.play(FadeOut(hl), run_time=0.3)

    def walk(self):
        mem, R, cl = self.mem, self.R, self.cl
        cbox = cl.line_box(0, color=BLUE_C, opacity=0.22, pad=0.12)

        # int a = 5;
        ch = self.chunk(0)
        box = ch.line_box(0, pad=0.12)
        self.say("第一行 a = 5：sw 只能存寄存器的值，所以先用 li 把 5 装进 t0，再存到 0(sp)。",
                 FadeIn(cbox), FadeIn(ch), FadeIn(box))
        self.play(R["t0"].set("5"))
        self.play(box.animate.become(ch.line_box(1, pad=0.12)))
        self.store(R["t0"], SP, 5)
        self.hold()

        # char b[] = "string";
        chars = ["s", "t", "r", "i", "n", "g", "\\0"]
        ascii_tbl = VGroup()
        for k, (chname, byte) in enumerate(zip(chars, STRING)):
            top = mono(f"'{chname}'", 20, GREEN_B)
            bot = mono(f"{byte:02X}", 20, WHITE)
            ascii_tbl.add(VGroup(top, bot).arrange(DOWN, buff=0.14))
        ascii_tbl.arrange(RIGHT, buff=0.28).move_to([0.9, -1.65, 0])
        self.say("第二行存 \"string\"：查 ASCII 表得到这 7 个字节。最直接的办法是逐个 li 再 sb，\\0 用 x0 存，共 13 条指令。",
                 FadeOut(ch), FadeOut(box), cbox.animate.become(cl.line_box(1, color=BLUE_C, opacity=0.22, pad=0.12)),
                 LaggedStart(*[FadeIn(a, shift=UP * 0.1) for a in ascii_tbl], lag_ratio=0.12))
        ted = VGroup()
        for k in range(7):
            li = mono(TEDIOUS[2 * k] if k < 6 else "", 18, C_TEXT, t2c={"li": C_MNEM})
            sb = mono(TEDIOUS[2 * k + 1] if k < 6 else TEDIOUS[12], 18, C_TEXT, t2c={"sb": C_MNEM})
            ted.add(VGroup(li, sb))
        for k, row in enumerate(ted):
            row[0].move_to([-1.9, 1.0 - 0.33 * k, 0], aligned_edge=LEFT)
            row[1].move_to([0.3, 1.0 - 0.33 * k, 0], aligned_edge=LEFT)
        count = zh("13 条指令", 24, RED_B).next_to(VGroup(*[r[1] for r in ted]), RIGHT, buff=0.45)
        count.set_y(0.0)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in ted], lag_ratio=0.12, run_time=1.8))
        self.play(FadeIn(count), Circumscribe(ted[6][1], color=YELLOW_D))
        self.hold()

        ch = self.chunk(1)
        imm = ch.glyphs(0, "69727473")
        pairs = [VGroup(*imm[6 - 2 * k:8 - 2 * k]) for k in range(4)]
        self.say("更聪明的办法：4 个字符拼成一个字，一条 sw 存下。按小端序，第一个字符要放在最低字节，所以 \"stri\" 写成 0x69727473。",
                 FadeOut(ted), FadeOut(count), FadeIn(ch))
        self.play(LaggedStart(*[Indicate(ascii_tbl[k][1], color=YELLOW_D, scale_factor=1.4) for k in range(4)],
                              lag_ratio=0.25))
        self.play(LaggedStart(*[TransformFromCopy(ascii_tbl[k][1], pairs[k]) for k in range(4)],
                              lag_ratio=0.3, run_time=2.0))
        box = ch.line_box(0, pad=0.12)
        self.play(FadeIn(box), R["t0"].set("0x69727473"))
        self.hold()
        self.say("sw 存到 4(sp) 后，从低地址往高地址看，正好是 s、t、r、i。",
                 box.animate.become(ch.line_box(1, pad=0.12)))
        self.store(R["t0"], SP + 4, W0)
        self.play(LaggedStart(*[Indicate(mem.text(SP + 4 + k), color=GREEN_B, scale_factor=1.5)
                                for k in range(4)], lag_ratio=0.25),
                  LaggedStart(*[Indicate(ascii_tbl[k][0], color=GREEN_B, scale_factor=1.3)
                                for k in range(4)], lag_ratio=0.25))
        self.say("剩下 n、g、\\0 再补一个 0 字节，凑成 0x0000676E，存到 8(sp)。总共只要 4 条指令。",
                 box.animate.become(ch.line_box(2, pad=0.12)))
        self.play(R["t1"].set("0x0000676E"))
        self.play(box.animate.become(ch.line_box(3, pad=0.12)))
        self.store(R["t1"], SP + 8, W1)
        self.hold()
        lui = zh("li → lui + addi（第 12 集）", 22, GREY_A).move_to([0.9, -0.95, 0])
        self.say("常数这么大，addi 的 12 位立即数装不下，li 会展开成 lui + addi 两条，第 12 集细讲。",
                 FadeOut(box), Circumscribe(ch.glyphs(0, "0x69727473"), color=YELLOW_D), FadeIn(lui))
        self.hold()

        # int c[10];
        none = zh("（不需要指令）", 24, GREY_A).move_to([-1.9, 0.9, 0], aligned_edge=UL)
        self.say("第三行 int c[10] 没有初值，不需要指令；布局本身也不产生指令。",
                 FadeOut(ch), FadeOut(lui), FadeOut(ascii_tbl), FadeIn(none),
                 cbox.animate.become(cl.line_box(2, color=BLUE_C, opacity=0.22, pad=0.12)),
                 Indicate(VGroup(*[mem.cells[i] for i in range(12, 52)]), color=GOLD_B, scale_factor=1.03))
        self.hold()

        # uint8_t d = b[3];
        ch = self.chunk(3)
        box = ch.line_box(0, pad=0.12)
        calc = self.calc(mono("4 + 3 = 7", 22, YELLOW_D), mono("7(sp)", 22, YELLOW_D))
        self.say("第四行 d = b[3]：b 从 4(sp) 开始，b[3] 再往后 3 字节，就是 7(sp)。",
                 FadeOut(none), FadeIn(ch), FadeIn(box), FadeIn(calc),
                 cbox.animate.become(cl.line_box(3, color=BLUE_C, opacity=0.22, pad=0.12)))
        hl = self.load(R["t0"], SP + 7, "0x00000069", n=1, keep=True)
        self.say("lb 读出 0x69，即 'i'；最高位是 0，符号扩展补的也是 0。再用 sb 存进 52(sp)，这就是 d。",
                 Indicate(R["t0"].box, color=C_T))
        self.play(FadeOut(hl), FadeOut(calc), box.animate.become(ch.line_box(1, pad=0.12)))
        self.store(R["t0"], SP + 52, 0x69, n=1)
        self.hold()

        # c[4] = a+d;
        ch2 = self.chunk(4)
        box2 = ch2.line_box(0, pad=0.12)
        self.say("第五行 c[4] = a+d：两个数都要先 load 进来。a 是 int，用 lw；d 是无符号的 uint8_t，用 lbu。",
                 FadeOut(ch), FadeOut(box), FadeIn(ch2), FadeIn(box2),
                 cbox.animate.become(cl.line_box(4, color=BLUE_C, opacity=0.22, pad=0.12)))
        self.load(R["t0"], SP, "5")
        calc = self.calc(mono("0x69 = 105", 22, YELLOW_D))
        self.play(box2.animate.become(ch2.line_box(1, pad=0.12)))
        self.load(R["t1"], SP + 52, "105", n=1)
        self.play(FadeIn(calc))
        self.hold()
        calc2 = self.calc(mono("12 + 4×4 = 28", 22, YELLOW_D))
        self.say("5 + 105 = 110。c 从 12(sp) 开始，c[4] 再往后 4 × 4 字节，所以存到 28(sp)。",
                 box2.animate.become(ch2.line_box(2, pad=0.12)), FadeOut(calc))
        self.play(R["t2"].set("110"))
        self.play(box2.animate.become(ch2.line_box(3, pad=0.12)), FadeIn(calc2))
        self.store(R["t2"], SP + 28, 110)
        self.hold()

        # c[a] = 20;
        ch3 = self.chunk(5)
        naive = CodeListing(["sw t0, ??(sp)"], font_size=24).move_to([0.9, -1.55, 0])
        self.say("最后一行 c[a] = 20 最难：能像 c[4] 那样，写一个固定的偏移量吗？",
                 FadeOut(ch2), FadeOut(box2), FadeOut(calc2), FadeIn(naive),
                 cbox.animate.become(cl.line_box(5, color=BLUE_C, opacity=0.22, pad=0.12)))
        cross = Cross(naive, stroke_color=RED_C, stroke_width=4)
        self.say("不行：a 是变量，运行时才知道是 5，而偏移量得在汇编时确定。地址只能在寄存器里算。",
                 Create(cross))
        self.hold()
        formula = mono("&c[a] = sp + 12 + 4×a", 22, YELLOW_D).move_to([0.9, -1.55, 0])
        box3 = ch3.line_box(0, pad=0.12)
        self.say("c[a] 的地址是 sp + 12 + 4 × a。先把 20 放进 t0，再把 a 读进 t1。",
                 FadeOut(naive), FadeOut(cross), FadeIn(formula), FadeIn(ch3), FadeIn(box3))
        self.play(R["t0"].set("20"))
        self.play(box3.animate.become(ch3.line_box(1, pad=0.12)))
        self.load(R["t1"], SP, "5")
        calc = self.calc(mono("0b101", 22, WHITE), mono("↓ << 2", 22, GREY_B), mono("0b10100 = 20", 22, YELLOW_D))
        self.say("乘 4 就是左移 2 位：slli 把 0b101 变成 0b10100，也就是 20。移位第 5 集细讲。",
                 box3.animate.become(ch3.line_box(2, pad=0.12)), FadeIn(calc))
        self.play(R["t1"].set("20"))
        self.hold()
        calc2 = self.calc(mono("20 + 12 = 32", 22, WHITE), mono("= 0x20", 22, WHITE),
                          mono("0x1000 + 0x20", 22, WHITE), mono("= 0x1020", 22, YELLOW_D))
        self.say("加上 c 的偏移量 12 得 32，即 0x20；再加上 sp 的 0x1000，得到完整地址 0x1020。",
                 box3.animate.become(ch3.line_box(3, pad=0.12)), FadeOut(calc), FadeIn(calc2[:2]))
        self.play(R["t1"].set("32"))
        self.play(box3.animate.become(ch3.line_box(4, pad=0.12)), FadeIn(calc2[2:]))
        self.play(R["t1"].set("0x1020"), Indicate(R["sp"].box, color=C_SP))
        self.hold()
        target = SurroundingRectangle(mem.word(SP + 32), color=YELLOW_D, buff=0.02)
        self.say("地址已经完整，所以偏移量写 0：sw t0, 0(t1) 把 20 写进 c[5]。",
                 box3.animate.become(ch3.line_box(5, pad=0.12)), FadeOut(calc2),
                 Create(target), Indicate(mem.row_label(SP + 32), color=YELLOW_D))
        self.play(FadeOut(target))
        self.store(R["t0"], SP + 32, 20)
        quiz = mono("t1 = &c[a]", 24, YELLOW_D)
        quiz = self.calc(quiz)
        self.say("小测验：此刻 t1 里是什么？不是 c[a] 的值，而是它的地址 &c[a]。",
                 FadeIn(quiz), Circumscribe(R["t1"], color=YELLOW_D))
        self.hold()
        self.clear_stage(run_time=0.6)

    # ------------------------------------------------------------------ notes, Example 1
    def example_one(self):
        head = self.heading("练习 1：lb 读到了什么？")
        code = CodeListing(EX1, font_size=30, line_gap=0.55).move_to([-4.3, 1.9, 0])
        regs = VGroup(RegBox("x5", "0x100", width=2.4, font_size=24, color=WHITE),
                      RegBox("x11", "?", width=2.4, font_size=24, color=WHITE),
                      RegBox("x12", "?", width=2.4, font_size=24, color=WHITE)).arrange(DOWN, buff=0.18)
        for b in regs[1:]:
            b.shift(RIGHT * (regs[0].box.get_center()[0] - b.box.get_center()[0]))
        regs.shift(np.array([5.2, 2.4, 0]) - regs[0].box.get_center())
        R = dict(zip(["x5", "x11", "x12"], regs))
        mem = MemoryView(0x100, 2, 4, cell_w=0.9, cell_h=0.5, font_size=24).move_to([0.6, 1.3, 0])
        self.say("再做两道短练习。第一道：x5 = 0x100，执行这三条指令后，x12 里是什么？",
                 Write(head), FadeIn(code), FadeIn(regs), FadeIn(mem))
        box = code.line_box(0)
        self.say("li 把 x11 设成 0x000093F5；sw 按小端序把它存进 0x100：F5 93 00 00。", FadeIn(box))
        self.play(R["x11"].set("0x000093F5"))
        self.play(box.animate.become(code.line_box(1)))
        v = R["x11"].val.copy()
        self.play(v.animate.move_to(mem.word(0x100).get_center()).scale(0.8), run_time=0.9)
        self.play(FadeOut(v), mem.set_word(0x100, 0x93F5))
        self.hold()
        hl = SurroundingRectangle(mem.cell(0x101), color=YELLOW_D, buff=0.03)
        addr = mono("0x100 + 1 = 0x101", 24, YELLOW_D).next_to(mem, DOWN, buff=0.3)
        self.say("lb x12, 1(x5) 读的是 0x101 处的字节：0x93，而不是 0xF5。",
                 box.animate.become(code.line_box(2)), Create(hl), FadeIn(addr))
        self.hold()

        row = bit_row("?" * 32, color=GREY_B, box=0.27, font_size=16).move_to([0.3, -1.45, 0])
        rlab = mono("x12", 24, WHITE).next_to(row, LEFT, buff=0.25)
        byte = "10010011"
        self.say("0x93 是 1001 0011，最高位是 1。lb 做符号扩展，高 24 位全填 1。",
                 FadeOut(addr), FadeIn(row), FadeIn(rlab))
        low = VGroup(*[mono(ch, 16, WHITE if ch == "1" else GREY_B).move_to(row[24 + k][0])
                       for k, ch in enumerate(byte)])
        src = mem.text(0x101).copy()
        self.play(src.animate.move_to(VGroup(*row[24:]).get_center()), run_time=0.8)
        self.play(FadeOut(src), *[FadeOut(row[24 + k][1]) for k in range(8)], FadeIn(low))
        sign = SurroundingRectangle(low[0], color=RED_B, buff=0.03)
        self.play(Create(sign))
        ones = VGroup(*[mono("1", 16, RED_B).move_to(row[k][0]) for k in range(24)])
        self.play(*[FadeOut(row[k][1]) for k in range(24)],
                  LaggedStart(*[TransformFromCopy(low[0], o) for o in reversed(ones)],
                              lag_ratio=0.04, run_time=1.8))
        hexes = VGroup(*[mono(h, 22, RED_B if k < 3 else WHITE).next_to(VGroup(*row[8 * k:8 * k + 8]), DOWN, buff=0.12)
                         for k, h in enumerate(["FF", "FF", "FF", "93"])])
        self.say("所以 x12 = 0xFFFFFF93。两个坑：小端序让 1(x5) 读到 0x93，lb 又把它扩展成了负数。",
                 FadeIn(hexes), R["x12"].set("0xFFFFFF93"))
        self.hold()
        self.clear_stage(run_time=0.6)

    # ------------------------------------------------------------------ notes, Example 2
    def example_two(self):
        head = self.heading("练习 2：*x = *y")
        lst = CodeListing(CANDIDATES, font_size=24, line_gap=0.45).move_to([-4.1, 0.55, 0])
        nums = VGroup(*[mono(f"{k + 1}", 24, GREY).next_to(lst.left_of(k, 0.3), LEFT, buff=0)
                        for k in range(8)])
        data = {PY + k: (VY >> 8 * k) & 0xFF for k in range(4)}
        data.update({PX + k: (VX >> 8 * k) & 0xFF for k in range(4)})
        mem = MemoryView(0x100, 3, 4, data=data, cell_w=0.8, cell_h=0.5, font_size=24).move_to([1.8, 1.4, 0])
        py = mono("*y", 24, GOLD_B).next_to(mem.cells[3], RIGHT, buff=0.3)
        px = mono("*x", 24, GOLD_B).next_to(mem.cells[11], RIGHT, buff=0.3)
        regs = VGroup(RegBox("x3", "0x108", width=1.6, font_size=24, color=WHITE),
                      RegBox("x5", "0x100", width=1.6, font_size=24, color=WHITE),
                      RegBox("x8", "?", width=1.6, font_size=24, color=WHITE)).arrange(RIGHT, buff=0.8)
        regs.move_to([2.2, -0.75, 0])
        R = dict(zip(["x3", "x5", "x8"], regs))
        tags = VGroup(mono("x", 22, GREY_A).next_to(R["x3"].box, DOWN, buff=0.1),
                      mono("y", 22, GREY_A).next_to(R["x5"].box, DOWN, buff=0.1),
                      zh("空闲", 22, GREY_A).next_to(R["x8"].box, DOWN, buff=0.1))
        self.say("第二道：x、y 是 int 指针，分别在 x3 和 x5 里。*x = *y 该选哪几条？",
                 Write(head), FadeIn(lst), FadeIn(nums), FadeIn(mem), FadeIn(py), FadeIn(px),
                 FadeIn(regs), FadeIn(tags))
        self.hold()
        bad = VGroup(*[Line(lst.left_of(k, 0.1), lst.right_of(k, 0.1), color=RED_B, stroke_width=3)
                       for k in range(4)])
        self.say("1 和 2 复制的是指针本身；3 和 4 用 lw 覆盖了指针寄存器。都不对。",
                 LaggedStart(*[Create(b) for b in bad], lag_ratio=0.2),
                 *[lst[k].animate.set_opacity(0.4) for k in range(4)])
        self.hold()
        box = lst.line_box(4)
        self.say("答案是 5 → 6：lw 把 *y 读进空闲的 x8，sw 再写到 x 指向的地址。内存到内存，必须经过寄存器。",
                 FadeIn(box))
        hl = SurroundingRectangle(mem.word(0x100), color=YELLOW_D, buff=0.02)
        self.play(Create(hl))
        fly = mem.word_texts(0x100).copy()
        self.play(fly.animate.arrange(RIGHT, buff=0.08).move_to(R["x8"].box).scale(0.8), run_time=0.9)
        self.play(FadeOut(fly), FadeOut(hl), R["x8"].set(42))
        self.play(box.animate.become(lst.line_box(5)))
        hl = SurroundingRectangle(mem.word(0x108), color=TEAL_C, buff=0.02)
        v = R["x8"].val.copy()
        self.play(Create(hl), v.animate.move_to(mem.word(0x108).get_center()), run_time=0.9)
        self.play(FadeOut(v), mem.set_word(0x108, VY))
        self.play(FadeOut(hl))
        bad2 = VGroup(*[Line(lst.left_of(k, 0.1), lst.right_of(k, 0.1), color=RED_B, stroke_width=3)
                        for k in (6, 7)])
        self.say("顺序不能反：6 → 5 会先存 x8 的旧值；7、8 把 x8 当成了地址，也不对。",
                 FadeOut(box), LaggedStart(*[Create(b) for b in bad2], lag_ratio=0.3),
                 *[lst[k].animate.set_opacity(0.4) for k in (6, 7)])
        self.hold()
        self.clear_stage(run_time=0.6)

    # ------------------------------------------------------------------ no sbu, alignment
    def fine_print(self):
        head = self.heading("两个细节")

        def byte_boxes(vals, color):
            g = VGroup()
            for v in vals:
                r = Rectangle(width=0.8, height=0.55, stroke_color=color, fill_color=color, fill_opacity=0.12)
                g.add(VGroup(r, mono(v, 24, WHITE).move_to(r)))
            return g.arrange(RIGHT, buff=0)

        reg1 = byte_boxes(["12", "34", "56", "EF"], BLUE_C).move_to([-3.2, 1.6, 0])
        mem1 = byte_boxes(["EF"], GREEN_C).move_to([3.3, 1.6, 0])
        mem1_old = byte_boxes(["··"], GREEN_C).move_to(mem1)
        l1 = mono("sb", 26, C_MNEM)
        a1 = Arrow(reg1.get_right(), mem1.get_left(), buff=0.25, color=TEAL_C)
        l1.next_to(a1, UP, buff=0.1)
        rl1 = zh("寄存器", 22, GREY_B).next_to(reg1, LEFT, buff=0.3)
        ml1 = zh("内存", 22, GREY_B).next_to(mem1, RIGHT, buff=0.3)
        sbu = mono("sbu ?", 30, RED_B).move_to([4.8, 3.3, 0])
        self.say("最后两个细节。第一个：有 lbu，为什么没有“sbu”？看看 store 做了什么。",
                 Write(head), FadeIn(sbu), FadeIn(reg1), FadeIn(mem1_old), FadeIn(rl1), FadeIn(ml1))
        self.play(GrowArrow(a1), FadeIn(l1), reg1[:3].animate.set_opacity(0.3))
        self.play(TransformFromCopy(reg1[3][1], mem1[0][1]), FadeOut(mem1_old[0][1]), FadeIn(mem1[0][0]),
                  FadeOut(mem1_old[0][0]))
        note1 = zh("只取最低字节，原样存入", 22, TEAL_C).next_to(a1, DOWN, buff=0.15)
        self.play(FadeIn(note1))

        mem2 = byte_boxes(["EF"], GREEN_C).move_to([3.3, -0.5, 0])
        reg2 = byte_boxes(["??", "??", "??", "EF"], BLUE_C).move_to([-3.2, -0.5, 0])
        a2 = Arrow(mem2.get_left(), reg2.get_right(), buff=0.25, color=YELLOW_D)
        l2 = mono("lb / lbu", 26, C_MNEM).next_to(a2, UP, buff=0.1)
        opts = VGroup(mono("lb : FF FF FF EF", 22, RED_B), mono("lbu: 00 00 00 EF", 22, BLUE_B))
        opts.arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(reg2, DOWN, buff=0.3)
        self.say("sb 只取最低字节，原样放进内存，无需扩展。load 却必须写满寄存器的 32 位。",
                 FadeIn(mem2), FadeIn(VGroup(*[b[0] for b in reg2])), FadeIn(reg2[3][1]),
                 GrowArrow(a2), FadeIn(l2))
        self.play(LaggedStart(*[Indicate(reg2[k][1], color=YELLOW_D) for k in range(3)], lag_ratio=0.2),
                  FadeIn(VGroup(*[reg2[k][1] for k in range(3)])))
        self.say("寄存器只是比特，后续指令怎么用它说不准，所以高位得明确：符号扩展，还是补 0。",
                 FadeIn(opts, shift=UP * 0.1))
        self.hold()
        self.play(FadeOut(VGroup(reg1, mem1, a1, l1, rl1, ml1, note1, mem2, reg2, a2, l2, opts, sbu)))

        # alignment
        strip = VGroup()
        for k in range(8):
            r = Rectangle(width=0.95, height=0.6, stroke_color=GREY_B, fill_color=GREY_E, fill_opacity=0.3)
            strip.add(VGroup(r, mono(f"0x{0x100 + k:X}", 18, GREY_B).next_to(r, UP, buff=0.1)))
        strip.arrange(RIGHT, buff=0).move_to(UP * 1.0)
        for s in strip:
            s[1].next_to(s[0], UP, buff=0.1)
        good = VGroup()
        for w in range(2):
            grp = VGroup(*[strip[4 * w + k][0] for k in range(4)])
            br = Brace(grp, DOWN, color=GREEN_B)
            good.add(VGroup(br, mono(f"lw 0x{0x100 + 4 * w:X}  ✓", 22, GREEN_B).next_to(br, DOWN, buff=0.1)))
        self.say("第二个是对齐：地址是访问大小整数倍的 load 和 store，规范保证绝不触发不对齐异常。",
                 FadeIn(strip), LaggedStart(*[FadeIn(g) for g in good], lag_ratio=0.4))
        mis = VGroup(*[strip[k][0] for k in range(2, 6)])
        mrect = SurroundingRectangle(mis, color=RED_B, buff=0.05)
        mlab = mono("lw 0x102  ?", 22, RED_B).next_to(good, DOWN, buff=0.35)
        self.say("不对齐的访问由具体实现决定：可能很慢，也可能报错。所以把“应该对齐”当成“必须对齐”。",
                 Create(mrect), FadeIn(mlab))
        self.hold()
        self.play(FadeOut(VGroup(strip, good, mrect, mlab)), run_time=0.5)

        # endianness: the same word, laid out both ways
        little = byte_boxes(["78", "56", "34", "12"], GREEN_C).move_to([0, 0.3, 0])
        big = byte_boxes(["12", "34", "56", "78"], GREY_B).move_to([0, -0.5, 0])
        ticks = VGroup(*[mono(f"+{k}", 18, GREY_B).next_to(little[k], UP, buff=0.12) for k in range(4)])
        base = mono("0x100", 18, GREY_B).next_to(ticks, LEFT, buff=0.3)
        word = mono("0x12345678", 30, YELLOW_D).next_to(ticks, UP, buff=0.45)
        l_lab = zh("小端（CS61C）", 24, GREEN_B).next_to(little, LEFT, buff=0.45)
        b_lab = zh("大端", 24, GREY_B).next_to(big, LEFT, buff=0.45)
        fig = VGroup(word, ticks, base, little, big, l_lab, b_lab)
        fig.shift(RIGHT * (-fig.get_center()[0]) + UP * (0.6 - fig.get_center()[1]))
        self.say("另外，规范允许小端和大端两种实现，CS61C 按小端讲。",
                 FadeIn(fig))
        self.play(Indicate(little[0], color=GREEN_B), Indicate(big[3], color=GREY_A))
        self.hold(0.5)
