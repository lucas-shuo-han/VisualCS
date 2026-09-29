import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F403

# ---------------------------------------------------------------- numbers from the notes (rv-intro)
PERIOD_NS = 1 / 4                         # 4 GHz clock
assert PERIOD_NS == 0.25
LIGHT_CM_PER_NS = 3.0e8 * 100 / 1e9       # c = 3.0e8 m/s -> 30 cm per ns
assert abs(LIGHT_CM_PER_NS * PERIOD_NS - 7.5) < 1e-9          # light covers 7.5 cm in one cycle
NS_10CM = 10 / LIGHT_CM_PER_NS
assert abs(NS_10CM - 1 / 3) < 1e-9 and NS_10CM > PERIOD_NS    # 10 cm: ~0.3 ns, more than a cycle
REG_BYTES = 32 * 4
assert REG_BYTES == 128                                       # RV32: 32 x 4 B
assert 100 / PERIOD_NS == 400                                 # ~100 ns memory access = 400 cycles
AREA = 64e9 / REG_BYTES                                       # 64 GB of DRAM vs 128 B of registers
assert AREA == 5e8 and 4.9e8 < 2 ** 36 / 2 ** 7 < 5.5e8       # "about 500 million" (GB or GiB)
SIDE = AREA ** 0.5
assert 20000 < SIDE < 30000 and 20000 < (2 ** 29) ** 0.5 < 30000   # "over 20,000 times wider"
ADD_FIELDS = ["0000000", "01100", "01011", "000", "01010", "0110011"]   # add x10, x11, x12
assert bits_to_hex("".join(ADD_FIELDS)) == "0x00C58533"

LAYERS = ["高级语言（C）", "汇编语言", "机器码", "硬件架构（框图）", "逻辑门", "晶体管"]
LAYER_Y = [2.3 - 0.76 * i for i in range(6)]

# California, roughly: (lat, lon) along the border, for Jim Gray's analogy
CA = [(42.0, -124.21), (42.0, -120.0), (39.0, -120.0), (35.0, -114.63), (34.3, -114.13),
      (33.4, -114.72), (32.72, -114.72), (32.53, -117.12), (33.2, -117.4), (33.75, -118.4),
      (34.03, -118.8), (34.4, -119.7), (34.45, -120.47), (35.2, -120.9), (35.67, -121.3),
      (36.3, -121.9), (36.6, -121.9), (36.95, -122.0), (37.5, -122.5), (37.8, -122.5),
      (38.0, -123.0), (38.3, -123.05), (38.95, -123.73), (39.8, -123.85), (40.44, -124.41),
      (40.8, -124.2), (41.75, -124.2)]
BERKELEY, SACRAMENTO, LOS_ANGELES = (37.87, -122.27), (38.58, -121.49), (34.05, -118.24)

TL_Y = 2.0                                # timeline height in the RISC / CISC part


def geo(lat, lon):
    return np.array([4.0 + (lon + 119.27) * 0.79 * 0.46, 0.15 + (lat - 37.27) * 0.46, 0])


def yx(year):
    return -6.2 + (year - 1970) * 12.4 / 55


def fit(m, w):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def clipped_square(center, side, color, fill_opacity, stroke_width=3, box=(-7.3, 7.3, -2.55, 3.15)):
    """An axis-aligned square cut to `box` (x0, x1, y0, y1), so a huge square
    never covers the heading or the caption band; cut edges get no stroke."""
    x0, x1, y0, y1 = box
    le, ri = center[0] - side / 2, center[0] + side / 2
    bo, to = center[1] - side / 2, center[1] + side / 2
    L, R, B, T = max(le, x0), min(ri, x1), max(bo, y0), min(to, y1)
    g = VGroup(VectorizedPoint(center))
    if L >= R or B >= T:
        return g
    g.add(Rectangle(width=R - L, height=T - B, stroke_width=0, fill_color=color,
                    fill_opacity=fill_opacity).move_to([(L + R) / 2, (B + T) / 2, 0]))
    edges = []
    if x0 <= le <= x1:
        edges.append(([le, B, 0], [le, T, 0]))
    if x0 <= ri <= x1:
        edges.append(([ri, B, 0], [ri, T, 0]))
    if y0 <= bo <= y1:
        edges.append(([L, bo, 0], [R, bo, 0]))
    if y0 <= to <= y1:
        edges.append(([L, to, 0], [R, to, 0]))
    for a, b in edges:
        g.add(Line(a, b, stroke_color=color, stroke_width=stroke_width))
    return g


def tag(text, color, w, h, size=24, font=CJK, fill=0.12, text_color=WHITE):
    r = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=color,
                         stroke_width=2.5, fill_color=color, fill_opacity=fill)
    t = (zh if font == CJK else mono)(text, size, text_color)
    fit(t, w - 0.3).move_to(r)
    return VGroup(r, t)


def alu_poly(width, height, color):
    w, h = width / 2, height / 2
    n = 0.18 * width
    return Polygon([-w, h, 0], [-n, h, 0], [0, h - n, 0], [n, h, 0], [w, h, 0],
                   [w * 0.55, -h, 0], [-w * 0.55, -h, 0],
                   stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.12)


def and_gate(center, h=1.1, color=TEAL_C):
    c = np.array([center[0], center[1], 0.0])
    r, w = h / 2, 0.55 * h
    p = VMobject(stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.12)
    p.start_new_path(c + [-w, -r, 0])
    p.add_line_to(c + [-w, r, 0])
    p.add_line_to(c + [0, r, 0])
    p.append_points(Arc(radius=r, start_angle=PI / 2, angle=-PI, arc_center=c).points)
    p.add_line_to(c + [-w, -r, 0])
    p.pin_in = [c + [-w, r / 2, 0], c + [-w, -r / 2, 0]]
    p.pin_out = c + [r, 0, 0]
    return p


def xor_gate(center, h=1.1, color=GOLD_C):
    c = np.array([center[0], center[1], 0.0])
    r, L, tip = h / 2, -0.55 * h, 0.5 * h
    p = VMobject(stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.12)
    p.start_new_path(c + [L, r, 0])
    p.add_cubic_bezier_curve_to(c + [L + 0.7 * h, r, 0], c + [tip - 0.15 * h, 0.45 * r, 0], c + [tip, 0, 0])
    p.add_cubic_bezier_curve_to(c + [tip - 0.15 * h, -0.45 * r, 0], c + [L + 0.7 * h, -r, 0], c + [L, -r, 0])
    p.add_cubic_bezier_curve_to(c + [L + 0.25 * h, -0.4 * r, 0], c + [L + 0.25 * h, 0.4 * r, 0], c + [L, r, 0])
    b = L - 0.14 * h
    back = VMobject(stroke_color=color, stroke_width=3.5)
    back.start_new_path(c + [b, -r, 0])
    back.add_cubic_bezier_curve_to(c + [b + 0.25 * h, -0.4 * r, 0], c + [b + 0.25 * h, 0.4 * r, 0], c + [b, r, 0])
    g = VGroup(p, back)
    g.pin_in = [c + [b + 0.12 * h, r / 2, 0], c + [b + 0.12 * h, -r / 2, 0]]
    g.pin_out = c + [tip, 0, 0]
    return g


def chip_icon(label, s, color=GREEN_C):
    body = Square(s, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.15)
    pins = VGroup()
    n = 4
    for k in range(n):
        t = (k + 0.5) / n - 0.5
        for d in (UP, DOWN, LEFT, RIGHT):
            along = RIGHT if d[1] != 0 else UP
            a = d * s / 2 + along * t * s
            pins.add(Line(a, a + d * 0.14, stroke_color=color, stroke_width=3))
    return VGroup(body, pins, mono(label, 20, WHITE))


class Ep01Intro(NarratedScene):
    def construct(self):
        self.title_card()
        self.abstraction()
        self.isa()
        self.why_assembly()
        self.von_neumann()
        self.clock_and_light()
        self.two_kinds()
        self.capacity()
        self.hierarchy()
        self.jim_gray()
        self.risc_cisc()
        self.why_riscv()
        self.rv32i()
        self.roadmap()
        self.end_card(
            [
                "抽象：高级语言 → 汇编 → 机器码 → 框图 → 逻辑门 → 晶体管",
                "ISA 是软件和硬件之间的接口",
                "五大部件：控制、数据通路、内存、输入、输出",
                "寄存器只有 128 字节，却比 DRAM 快 50–500 倍",
                "RISC：指令少而简单；RISC-V 开源、免授权费",
            ],
        )

    # ------------------------------------------------------------------ Great Idea #1
    def abstraction(self):
        head = self.heading("伟大思想 #1：抽象")
        self.head = head
        boxes = VGroup(*[tag(s, GREY_B, 4.5, 0.58, 24, fill=0.08).move_to([-4.35, y, 0])
                         for s, y in zip(LAYERS, LAYER_Y)])
        self.layers = boxes
        self.say("CS61C 的第一个伟大思想：抽象。计算机系统从上到下，分成一层又一层。",
                 Write(head), LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in boxes],
                                          lag_ratio=0.15, run_time=2))
        self.hold()

        ptr = Arrow(LEFT * 0.45, RIGHT * 0.45, buff=0, color=YELLOW_D, stroke_width=6,
                    max_tip_length_to_length_ratio=0.4).move_to([-1.7, LAYER_Y[0], 0])

        def focus(i, move=True):
            anims = [ptr.animate.move_to([-1.7, LAYER_Y[i], 0])] if move else []
            for k, b in enumerate(boxes):
                col = YELLOW_D if k == i else GREY_B
                anims.append(b[0].animate.set_stroke(col).set_fill(col, 0.2 if k == i else 0.08))
            return anims

        c = CodeListing(["a = b + c;"], lang="c", font_size=40).move_to([2.4, 2.3, 0])
        self.say("最上层是高级语言，比如 C。", FadeIn(ptr), *focus(0, move=False),
                 FadeIn(c, shift=LEFT * 0.2))
        asm = CodeListing(["add x10, x11, x12"], font_size=36).move_to([2.4, 0.85, 0])
        a1 = Arrow(c.get_bottom(), asm.get_top(), buff=0.15, color=GREY_B)
        l1 = zh("编译器", 22, GREY_A).next_to(a1, RIGHT, buff=0.2)
        self.say("编译器把它翻译成汇编语言……", *focus(1), GrowArrow(a1), FadeIn(l1),
                 FadeIn(asm, shift=DOWN * 0.2))
        cols = [FIELD_COLORS[k] for k in ("funct7", "rs2", "rs1", "funct3", "rd", "opcode")]
        mc = MarkupText(" ".join(span(b, col) for b, col in zip(ADD_FIELDS, cols)),
                        font=MONO, font_size=24).move_to([2.4, -0.6, 0])
        a2 = Arrow(asm.get_bottom(), mc.get_top(), buff=0.15, color=GREY_B)
        l2 = zh("汇编器", 22, GREY_A).next_to(a2, RIGHT, buff=0.2)
        self.say("……汇编器再把它变成机器码：机器能直接读懂的 0 和 1。", *focus(2), GrowArrow(a2),
                 FadeIn(l2), FadeIn(mc, lag_ratio=0.05))
        self.hold()

        # hardware: block diagram -> gates -> transistor, each a zoom into the one before
        bd = self.block_diagram()
        self.say("再往下是硬件：先是用框图描述的架构，比如两个寄存器的值送进一个加法器。",
                 *focus(3), FadeOut(VGroup(c, a1, l1, asm, a2, l2, mc), shift=UP * 0.3),
                 FadeIn(bd, shift=UP * 0.3))
        d1, d2 = Dot(bd.r1.get_bottom(), color=YELLOW_D), Dot(bd.r2.get_bottom(), color=YELLOW_D)
        self.play(d1.animate.move_to(bd.alu_in[0]), d2.animate.move_to(bd.alu_in[1]), run_time=0.8)
        d3 = Dot(bd.alu.get_bottom(), color=YELLOW_D)
        self.play(ReplacementTransform(VGroup(d1, d2), d3), run_time=0.4)
        self.play(d3.animate.move_to(bd.rd.get_top()), run_time=0.6)
        self.play(FadeOut(d3), Indicate(bd.rd, color=YELLOW_D))
        self.hold()

        gates = self.half_adder()
        gates.save_state()
        gates.scale(0.15).move_to(bd.alu.get_center()).set_opacity(0)
        self.say("放大加法器，里面是逻辑门：两个比特相加，异或门给出和，与门给出进位。",
                 *focus(4), bd.animate.scale(5, about_point=bd.alu.get_center()).set_opacity(0),
                 Restore(gates), run_time=1.6)
        self.remove(bd)
        self.hold()

        tr_pic = self.transistor()
        tr_pic.save_state()
        tr_pic.scale(0.15).move_to(gates.and_g.get_center()).set_opacity(0)
        self.say("再放大一个逻辑门：它由晶体管搭成。这是最底层。",
                 *focus(5), gates.animate.scale(5, about_point=gates.and_g.get_center()).set_opacity(0),
                 Restore(tr_pic), run_time=1.6)
        self.remove(gates)
        self.hold()

        ifaces = VGroup(*[
            Line([-6.55, (LAYER_Y[k] + LAYER_Y[k + 1]) / 2, 0], [-2.15, (LAYER_Y[k] + LAYER_Y[k + 1]) / 2, 0],
                 stroke_color=YELLOW_D, stroke_width=5)
            for k in range(5)
        ])
        self.ifaces = ifaces
        unfocus = [b[0].animate.set_stroke(GREY_B).set_fill(GREY_B, 0.08) for b in boxes]
        self.say("相邻两层之间都有定义清晰的接口：只要遵守接口，就不必关心下一层的细节。",
                 FadeOut(tr_pic), FadeOut(ptr), *unfocus,
                 LaggedStart(*[Create(l) for l in ifaces], lag_ratio=0.2, run_time=1.5))
        self.play(LaggedStart(*[Indicate(l, color=WHITE, scale_factor=1.05) for l in ifaces],
                              lag_ratio=0.15))
        self.hold()

    def block_diagram(self):
        def reg(name):
            r = RoundedRectangle(corner_radius=0.06, width=1.3, height=0.55, stroke_color=C_REG,
                                 stroke_width=2.5, fill_color=C_REG, fill_opacity=0.12)
            return VGroup(r, mono(name, 24, C_REG).move_to(r))

        r1, r2 = reg("x11").move_to([1.3, 2.2, 0]), reg("x12").move_to([3.5, 2.2, 0])
        alu = VGroup(alu_poly(2.0, 1.2, BLUE_C), mono("+", 32, BLUE_B)).move_to([2.4, 0.6, 0])
        alu[1].shift(DOWN * 0.1)
        rd = reg("x10").move_to([2.4, -1.2, 0])
        c = alu.get_center()
        ins = [c + [-0.55, 0.6, 0], c + [0.55, 0.6, 0]]
        arrows = VGroup(
            Arrow(r1.get_bottom(), ins[0], buff=0.05, color=GREY_B, stroke_width=3),
            Arrow(r2.get_bottom(), ins[1], buff=0.05, color=GREY_B, stroke_width=3),
            Arrow(alu.get_bottom(), rd.get_top(), buff=0.05, color=GREY_B, stroke_width=3),
        )
        g = VGroup(arrows, r1, r2, alu, rd)
        g.r1, g.r2, g.alu, g.rd, g.alu_in = r1, r2, alu, rd, ins
        return g

    def half_adder(self):
        xg = xor_gate([2.9, 1.35])
        ag = and_gate([2.9, -0.45], color=TEAL_C)
        ya, yb = xg.pin_in[0][1], xg.pin_in[1][1]
        x0 = 0.3
        wires = VGroup(
            Line([x0, ya, 0], xg.pin_in[0]), Line([x0, yb, 0], xg.pin_in[1]),
            Line([0.9, ya, 0], [0.9, ag.pin_in[0][1], 0]), Line([0.9, ag.pin_in[0][1], 0], ag.pin_in[0]),
            Line([1.4, yb, 0], [1.4, ag.pin_in[1][1], 0]), Line([1.4, ag.pin_in[1][1], 0], ag.pin_in[1]),
            Line(xg.pin_out, xg.pin_out + RIGHT * 0.9), Line(ag.pin_out, ag.pin_out + RIGHT * 0.9),
        ).set_stroke(GREY_A, 2.5)
        joints = VGroup(Dot([0.9, ya, 0], radius=0.06, color=GREY_A), Dot([1.4, yb, 0], radius=0.06, color=GREY_A))
        la = mono("a", 28, WHITE).next_to([x0, ya, 0], LEFT, buff=0.15)
        lb = mono("b", 28, WHITE).next_to([x0, yb, 0], LEFT, buff=0.15)
        ls = zh("和", 26, GOLD_B).next_to(xg.pin_out + RIGHT * 0.9, RIGHT, buff=0.15)
        lc = zh("进位", 26, TEAL_B).next_to(ag.pin_out + RIGHT * 0.9, RIGHT, buff=0.15)
        nx = mono("XOR", 18, GOLD_B).next_to(xg, DOWN, buff=0.08)
        na = mono("AND", 18, TEAL_B).next_to(ag, DOWN, buff=0.08)
        title = zh("1 位半加器", 24, GREY_A).move_to([2.6, 2.5, 0])
        g = VGroup(wires, joints, xg, ag, la, lb, ls, lc, nx, na, title)
        g.and_g = ag
        return g

    def transistor(self):
        s, c = 1.3, np.array([2.4, 0.6, 0])

        def P(x, y):
            return c + s * np.array([x, y, 0])

        sym = VGroup(
            Line(P(-1.1, 0), P(-0.3, 0)), Line(P(-0.3, -0.55), P(-0.3, 0.55)),
            Line(P(-0.12, -0.7), P(-0.12, 0.7)),
            Line(P(-0.12, 0.45), P(0.5, 0.45)), Line(P(0.5, 0.45), P(0.5, 1.2)),
            Line(P(-0.12, -0.45), P(0.5, -0.45)), Line(P(0.5, -0.45), P(0.5, -1.2)),
        ).set_stroke(GREEN_C, 5)
        lab = zh("晶体管", 28, GREEN_B).next_to(sym, RIGHT, buff=0.5)
        return VGroup(sym, lab)

    # ------------------------------------------------------------------ the ISA
    def isa(self):
        boxes, ifaces = self.layers, self.ifaces
        y = ifaces[2].get_y()
        isa_line = DashedLine([-6.75, y, 0], [-1.3, y, 0], dash_length=0.14,
                              stroke_color=YELLOW_D, stroke_width=5)
        isa_lab = mono("ISA", 30, YELLOW_D).next_to(isa_line, RIGHT, buff=0.15)
        sw = Brace(VGroup(*boxes[:3]), RIGHT, buff=0.15, color=BLUE_B)
        hw = Brace(VGroup(*boxes[3:]), RIGHT, buff=0.15, color=GREEN_B)
        sw_l = zh("软件", 26, BLUE_B).next_to(sw, RIGHT, buff=0.12)
        hw_l = zh("硬件", 26, GREEN_B).next_to(hw, RIGHT, buff=0.12)
        new_head = self.heading("指令集架构（ISA）")
        tint = [b[0].animate.set_stroke(BLUE_C if k < 3 else GREEN_C).set_fill(BLUE_C if k < 3 else GREEN_C, 0.12)
                for k, b in enumerate(boxes)]
        self.say("本系列关注软件和硬件之间的接口：指令集架构（ISA）。",
                 Transform(self.head, new_head), *[FadeOut(l) for k, l in enumerate(ifaces) if k != 2],
                 ReplacementTransform(ifaces[2], isa_line), FadeIn(isa_lab), *tint,
                 GrowFromCenter(sw), GrowFromCenter(hw), FadeIn(sw_l), FadeIn(hw_l))
        self.hold()

        title = zh("ISA 规定了：", 28, YELLOW_D)
        items = ["汇编语言：有哪些指令", "机器语言：指令如何用比特表示", "寄存器", "数据类型",
                 "内存寻址方式", "输入输出模型"]
        rows = VGroup(*[VGroup(Dot(radius=0.05, color=YELLOW_D), zh(s, 26)).arrange(RIGHT, buff=0.2)
                        for s in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        spec = VGroup(title, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        fit(spec, 5.9).move_to([3.4, 0.55, 0])
        self.say("ISA 规定了汇编语言有哪些指令、它们怎样编码成比特，以及寄存器、数据类型、内存寻址、输入输出等架构特性。",
                 FadeIn(title), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5,
                                            run_time=4))
        self.hold()
        self.clear_stage(self.head)

        progs = VGroup(*[tag(s, BLUE_C, 2.6, 0.7, 24) for s in ["应用程序", "操作系统", "编译器"]])
        progs.arrange(RIGHT, buff=1.4).move_to(UP * 1.9)
        bar = tag("指令集架构（ISA）", YELLOW_D, 11.0, 0.75, 28, fill=0.18).move_to(UP * 0.25)
        chips = VGroup(*[chip_icon(n, s) for n, s in [("CPU A", 0.8), ("CPU B", 1.0), ("CPU C", 1.2)]])
        for ch, p in zip(chips, progs):
            ch.move_to([p.get_x(), -1.5, 0])
        up = VGroup(*[Line(p.get_bottom(), [p.get_x(), bar.get_top()[1], 0], stroke_color=BLUE_B, stroke_width=3)
                      for p in progs])
        down = VGroup(*[Line([ch.get_x(), bar.get_bottom()[1], 0], ch[0].get_top() + UP * 0.14,
                             stroke_color=GREEN_B, stroke_width=3) for ch in chips])
        wl = zh("按 ISA 编写", 22, BLUE_B).move_to([-2.0, (progs.get_bottom()[1] + bar.get_top()[1]) / 2, 0])
        dl = zh("按 ISA 设计", 22, GREEN_B).move_to([-2.0, (bar.get_bottom()[1] + chips.get_top()[1]) / 2, 0])
        self.say("程序和编译器以 ISA 为标准来编写；CPU 等硬件也以同一个 ISA 为标准来设计。",
                 FadeIn(bar), LaggedStart(*[FadeIn(p, shift=DOWN * 0.2) for p in progs], lag_ratio=0.2),
                 *[Create(l) for l in up], FadeIn(wl),
                 LaggedStart(*[FadeIn(ch, shift=UP * 0.2) for ch in chips], lag_ratio=0.2),
                 *[Create(l) for l in down], FadeIn(dl))
        self.hold()

        src = progs[0].get_bottom()
        dots = [Dot(src, color=YELLOW_D, radius=0.09) for _ in chips]
        self.say("所以，程序能在任何遵循同一 ISA 的 CPU 上运行。本系列要学的 ISA，叫作 RISC-V。",
                 *[FadeIn(d) for d in dots])
        self.play(*[d.animate.move_to([progs[0].get_x(), bar.get_y(), 0]) for d in dots], run_time=0.7)
        self.play(*[d.animate.move_to([ch.get_x(), bar.get_y(), 0]) for d, ch in zip(dots, chips)], run_time=0.8)
        self.play(*[d.animate.move_to(ch[0].get_center()) for d, ch in zip(dots, chips)], run_time=0.7)
        self.play(*[FadeOut(d, scale=2) for d in dots], *[Indicate(ch[0], color=YELLOW_D) for ch in chips])
        rv = zh("RISC-V", 30, WHITE).move_to(bar[1])
        self.play(Transform(bar[1], rv))
        self.play(Indicate(bar, color=YELLOW_D, scale_factor=1.03))
        self.hold()
        self.clear_stage(self.head)

    # ------------------------------------------------------------------ why assembly?
    def why_assembly(self):
        new_head = self.heading("为什么要学汇编？")
        c = tag("C 代码", BLUE_C, 2.2, 0.8, 26)
        a = tag("汇编", YELLOW_D, 2.2, 0.8, 26)
        m = tag("机器码", GREEN_C, 2.2, 0.8, 26)
        row = VGroup(c, a, m).arrange(RIGHT, buff=2.2).move_to(UP * 1.5)
        arr = VGroup(Arrow(c.get_right(), a.get_left(), buff=0.12, color=GREY_B),
                     Arrow(a.get_right(), m.get_left(), buff=0.12, color=GREY_B))
        tools = VGroup(zh("编译器", 22, GREY_A).next_to(arr[0], UP, buff=0.12),
                       zh("汇编器", 22, GREY_A).next_to(arr[1], UP, buff=0.12))
        rare = zh("很少手写", 22, GREY_A).next_to(a, DOWN, buff=0.2)
        self.say("汇编大多由编译器生成，很少有人手写。那为什么还要学它？",
                 Transform(self.head, new_head), FadeIn(row, lag_ratio=0.3), GrowArrow(arr[0]),
                 GrowArrow(arr[1]), FadeIn(tools), FadeIn(rare))
        self.play(Circumscribe(a, color=YELLOW_D))

        card = RoundedRectangle(corner_radius=0.15, width=10.4, height=1.5, stroke_color=GREY_B,
                                stroke_width=2, fill_color=GREY_E, fill_opacity=0.35).move_to(DOWN * 0.75)
        src = mono("Slashdot · 2004", 22, GREY_B).next_to(card.get_corner(UL), DR, buff=0.18)
        body = fit(zh("程序员平庸还是优秀，就看懂不懂汇编", 30), 9.6)
        body.move_to(card.get_center() + DOWN * 0.18)
        self.say("2004 年 Slashdot 上有篇帖子甚至说：程序员平庸还是优秀，就看懂不懂汇编。",
                 FadeIn(card), FadeIn(src), FadeIn(body, shift=UP * 0.15))
        self.hold()

        key = zh("懂汇编 → 懂计算机怎样执行指令", 30, YELLOW_D).move_to(DOWN * 0.35)
        badges = VGroup(*[tag(s, GOLD_C, 2.4, 0.7, 26) for s in ["更快", "更省资源", "成本更低"]])
        badges.arrange(RIGHT, buff=0.6).move_to(DOWN * 1.55)
        self.say("懂汇编，就懂计算机怎样执行指令；用高级语言也能写出更快、更省资源、成本更低的程序。",
                 FadeOut(VGroup(card, src, body)), FadeIn(key, shift=UP * 0.15),
                 LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in badges], lag_ratio=0.3))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ five components
    def von_neumann(self):
        head = self.heading("冯·诺依曼结构")
        cpu = RoundedRectangle(corner_radius=0.15, width=4.2, height=4.5, stroke_color=BLUE_C,
                               stroke_width=3, fill_color=BLUE_C, fill_opacity=0.05).move_to([-4.35, -0.1, 0])
        cpu_l = zh("处理器（CPU）", 26, BLUE_B).next_to(cpu.get_top(), DOWN, buff=0.15)
        ctrl = tag("控制单元", PURPLE_B, 3.6, 0.8, 24).move_to([-4.35, 1.15, 0])
        dp = RoundedRectangle(corner_radius=0.1, width=3.6, height=2.55, stroke_color=TEAL_C,
                              stroke_width=2.5, fill_color=TEAL_C, fill_opacity=0.08).move_to([-4.35, -0.9, 0])
        dp_l = zh("数据通路", 24, TEAL_B).next_to(dp.get_top(), DOWN, buff=0.12)
        regs = VGroup(*[Rectangle(width=1.1, height=0.2, stroke_color=YELLOW_D, stroke_width=2,
                                  fill_color=YELLOW_D, fill_opacity=0.25) for _ in range(5)])
        regs.arrange(DOWN, buff=0.06).move_to([-5.2, -1.05, 0])
        regs_l = zh("寄存器", 20, YELLOW_D).next_to(regs, DOWN, buff=0.12)
        alu = alu_poly(1.3, 0.95, BLUE_C).move_to([-3.45, -1.0, 0])
        alu_l = mono("ALU", 20, BLUE_B).move_to(alu.get_center() + DOWN * 0.12)
        alu_g = VGroup(alu, alu_l)

        mem = RoundedRectangle(corner_radius=0.15, width=2.8, height=4.5, stroke_color=GREEN_C,
                               stroke_width=3, fill_color=GREEN_C, fill_opacity=0.05).move_to([1.05, -0.1, 0])
        mem_l = zh("内存", 26, GREEN_B).next_to(mem.get_top(), DOWN, buff=0.15)
        prog = tag("程序", PURPLE_B, 2.2, 1.45, 24).move_to([1.05, 0.75, 0])
        data = tag("数据", GOLD_C, 2.2, 1.45, 24).move_to([1.05, -1.05, 0])

        io = RoundedRectangle(corner_radius=0.15, width=2.5, height=4.5, stroke_color=RED_C,
                              stroke_width=3, fill_color=RED_C, fill_opacity=0.05).move_to([5.25, -0.1, 0])
        io_l = zh("输入输出（I/O）", 24, RED_B).next_to(io.get_top(), DOWN, buff=0.15)
        fit(io_l, 2.3)
        inp = VGroup(zh("输入", 26, WHITE), zh("键盘等", 20, GREY_A)).arrange(DOWN, buff=0.12)
        out = VGroup(zh("输出", 26, WHITE), zh("显示器等", 20, GREY_A)).arrange(DOWN, buff=0.12)
        inp_b, out_b = [RoundedRectangle(corner_radius=0.1, width=2.0, height=1.45, stroke_color=RED_C,
                                         stroke_width=2.5, fill_color=RED_C, fill_opacity=0.12).move_to([5.25, y, 0])
                        for y in (0.75, -1.05)]
        inp.move_to(inp_b)
        out.move_to(out_b)

        x_a, x_b = cpu.get_right()[0] + 0.05, mem.get_left()[0] - 0.05
        bus_specs = [("地址", 1.25, RIGHT), ("写入数据", 0.45, RIGHT), ("读出数据", -0.35, LEFT), ("使能", -1.15, RIGHT)]
        buses, bus_l = VGroup(), VGroup()
        for name, yy, d in bus_specs:
            s, e = ([x_a, yy, 0], [x_b, yy, 0]) if d is RIGHT else ([x_b, yy, 0], [x_a, yy, 0])
            buses.add(Arrow(s, e, buff=0, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.12))
            bus_l.add(fit(zh(name, 18, GREY_A), 1.8).next_to(buses[-1], UP, buff=0.05))
        link = DoubleArrow([mem.get_right()[0] + 0.05, -0.1, 0], [io.get_left()[0] - 0.05, -0.1, 0], buff=0,
                           color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.2)

        self.say("学 ISA 之前，先来看计算机的基本布局：冯·诺依曼结构。",
                 Write(head), Create(cpu), Create(mem), Create(io), FadeIn(cpu_l), FadeIn(mem_l), FadeIn(io_l))
        self.say("处理器（CPU）负责计算，由两部分组成：控制单元（control）和数据通路（datapath）。",
                 FadeIn(ctrl, shift=DOWN * 0.15), Create(dp), FadeIn(dp_l))
        self.say("数据通路的主角，是寄存器和负责运算的算术逻辑单元（ALU）。",
                 FadeIn(regs, lag_ratio=0.2), FadeIn(regs_l), FadeIn(alu_g, shift=UP * 0.15))
        self.say("处理器之外，是存放程序和数据的内存（memory），以及键盘、显示器这样的输入输出设备（I/O）。",
                 FadeIn(prog, shift=DOWN * 0.15), FadeIn(data, shift=UP * 0.15))
        self.play(FadeIn(inp_b), FadeIn(out_b), FadeIn(inp), FadeIn(out), GrowFromCenter(link))
        self.hold()

        parts = [ctrl, dp, VGroup(mem, prog, data), inp_b, out_b]
        badges = VGroup()
        for k, p in enumerate(parts):
            b = VGroup(Circle(radius=0.2, stroke_color=YELLOW_D, fill_color=BG, fill_opacity=1, stroke_width=2.5),
                       mono(str(k + 1), 22, YELLOW_D))
            b[1].move_to(b[0])
            b.move_to(p.get_corner(UL) + np.array([0.05, -0.05, 0]))
            badges.add(b)
        self.say("控制、数据通路、内存、输入、输出：这就是计算机的五大部件。",
                 LaggedStart(*[AnimationGroup(FadeIn(b, scale=1.5), Indicate(p, color=YELLOW_D, scale_factor=1.03))
                               for b, p in zip(badges, parts)], lag_ratio=0.35, run_time=3))
        self.hold()

        self.say("处理器发出地址来读写内存；“使能”信号保证只读的时候不会误改内存。",
                 LaggedStart(*[GrowArrow(b) for b in buses], lag_ratio=0.15), FadeIn(bus_l))
        addr = Dot([x_a, 1.25, 0], color=YELLOW_D, radius=0.09)
        self.play(FadeIn(addr), Indicate(bus_l[0], color=YELLOW_D))
        self.play(addr.animate.move_to([x_b, 1.25, 0]), run_time=0.7)
        self.play(addr.animate.move_to(data.get_center()), run_time=0.6)
        self.play(FadeOut(addr), Indicate(data, color=GOLD_B))
        val = Dot([x_b, -0.35, 0], color=GOLD_B, radius=0.09)
        self.play(FadeIn(val), Indicate(bus_l[2], color=GOLD_B))
        self.play(val.animate.move_to([x_a, -0.35, 0]), run_time=0.8)
        self.play(val.animate.move_to(regs.get_center()), run_time=0.5)
        self.play(FadeOut(val), Indicate(regs, color=YELLOW_D), Indicate(bus_l[3], color=RED_B, scale_factor=1.3))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 4 GHz and the speed of light
    def clock_and_light(self):
        head = self.heading("寄存器与内存")
        self.head = head
        P, x0, lo, hi = 2.4, -6.0, 1.3, 2.0
        pts = []
        for k in range(5):
            xs = x0 + k * P
            pts += [[xs, lo, 0], [xs, hi, 0], [xs + P / 2, hi, 0], [xs + P / 2, lo, 0]]
        pts.append([x0 + 5 * P, lo, 0])
        wave = VMobject(stroke_color=BLUE_B, stroke_width=3).set_points_as_corners(pts)
        br = Brace(Line([x0, hi, 0], [x0 + P, hi, 0]), UP, buff=0.08, color=YELLOW_D)
        br_l = mono("0.25 ns", 24, YELLOW_D).next_to(br, UP, buff=0.06)
        ghz = zh("4 GHz：每秒 40 亿个周期", 24, BLUE_B).move_to([3.4, 2.6, 0])
        self.say("处理器非常快：4 GHz 的处理器，一个时钟周期只有 0.25 纳秒。",
                 Write(head), Create(wave, run_time=1.5), FadeIn(ghz))
        self.play(GrowFromCenter(br), FadeIn(br_l))

        ry, cm = -0.7, 1.0
        rx0 = -5.0
        ruler = VGroup(Line([rx0, ry, 0], [rx0 + 10 * cm, ry, 0], stroke_color=GREY_A, stroke_width=3))
        for k in range(11):
            h = 0.25 if k % 5 == 0 else 0.14
            ruler.add(Line([rx0 + k * cm, ry, 0], [rx0 + k * cm, ry - h, 0], stroke_color=GREY_A, stroke_width=2))
        nums = VGroup(*[mono(f"{k} cm" if k == 10 else str(k), 22, GREY_A).next_to([rx0 + k * cm, ry - 0.25, 0], DOWN, buff=0.1)
                        for k in (0, 5, 10)])
        light = zh("光速 ≈ 30 万公里/秒", 24, YELLOW_D).next_to([rx0, ry, 0], UP, buff=0.9).align_to([rx0, 0, 0], LEFT)
        t = ValueTracker(0.0)
        sweep = always_redraw(lambda: Line([x0 + t.get_value() / PERIOD_NS * P, lo - 0.2, 0],
                                           [x0 + t.get_value() / PERIOD_NS * P, hi + 0.2, 0],
                                           stroke_color=YELLOW_D, stroke_width=4))
        trail = always_redraw(lambda: Line([rx0, ry, 0], [rx0 + t.get_value() * LIGHT_CM_PER_NS * cm + 1e-4, ry, 0],
                                           stroke_color=YELLOW_D, stroke_width=7))
        photon = always_redraw(lambda: VGroup(
            Dot([rx0 + t.get_value() * LIGHT_CM_PER_NS * cm, ry, 0], radius=0.22, color=YELLOW_D).set_opacity(0.3),
            Dot([rx0 + t.get_value() * LIGHT_CM_PER_NS * cm, ry, 0], radius=0.1, color=YELLOW_A)))
        tl = always_redraw(lambda: mono(f"t = {t.get_value():.2f} ns", 26, WHITE).move_to([4.6, 0.35, 0]))
        self.say("这有多短？光速约每秒 30 万公里，而 0.25 纳秒只够光走 7.5 厘米。",
                 FadeIn(ruler), FadeIn(nums), FadeIn(light))
        self.add(sweep, trail, photon, tl)
        self.play(t.animate.set_value(PERIOD_NS), run_time=2.5, rate_func=linear)
        m75 = VGroup(Line([rx0 + 7.5 * cm, ry + 0.1, 0], [rx0 + 7.5 * cm, ry + 0.5, 0], stroke_color=YELLOW_D, stroke_width=3),
                     mono("7.5 cm", 24, YELLOW_D))
        m75[1].next_to(m75[0], UP, buff=0.08)
        self.play(FadeIn(m75), Indicate(br_l))
        self.hold()

        over = Rectangle(width=(NS_10CM - PERIOD_NS) / PERIOD_NS * P, height=hi - lo + 0.4, stroke_width=0,
                         fill_color=RED_C, fill_opacity=0.35)
        over.move_to([x0 + P + over.width / 2, (lo + hi) / 2, 0])
        self.say("数据哪怕只在 10 厘米外，光也要跑约 0.3 纳秒，超过一个周期。所以数据必须离处理器很近。")
        self.play(t.animate.set_value(NS_10CM), run_time=1.0, rate_func=linear)
        over_l = zh("超过一个周期", 22, RED_B).next_to(over, DOWN, buff=0.1)
        chip = zh("好在芯片本身远小于 10 厘米", 20, GREY_A).move_to([0, -1.85, 0])
        self.play(FadeIn(over), FadeIn(over_l))
        self.play(FadeIn(chip))
        self.hold()
        sweep.clear_updaters()
        trail.clear_updaters()
        photon.clear_updaters()
        tl.clear_updaters()
        self.clear_stage(self.head)

    # ------------------------------------------------------------------ registers vs memory
    def chip_diagram(self):
        cpu = RoundedRectangle(corner_radius=0.15, width=3.6, height=3.1, stroke_color=BLUE_C, stroke_width=3,
                               fill_color=BLUE_C, fill_opacity=0.06).move_to([-4.0, 0.3, 0])
        cpu_l = zh("处理器", 26, BLUE_B).next_to(cpu.get_top(), DOWN, buff=0.18)
        regs = VGroup(*[Rectangle(width=1.0, height=0.22, stroke_color=YELLOW_D, stroke_width=2,
                                  fill_color=YELLOW_D, fill_opacity=0.25) for _ in range(5)])
        regs.arrange(DOWN, buff=0.06).move_to([-4.75, 0.05, 0])
        regs_l = zh("寄存器", 22, YELLOW_D).next_to(regs, DOWN, buff=0.15)
        alu = VGroup(alu_poly(1.2, 0.9, BLUE_C), mono("ALU", 20, BLUE_B))
        alu[1].shift(DOWN * 0.1)
        alu.move_to([-3.2, 0.05, 0])
        mem = RoundedRectangle(corner_radius=0.15, width=3.0, height=3.1, stroke_color=GREEN_C, stroke_width=3,
                               fill_color=GREEN_C, fill_opacity=0.06).move_to([4.0, 0.3, 0])
        mem_l = zh("内存（DRAM）", 26, GREEN_B).next_to(mem.get_top(), DOWN, buff=0.18)
        grid = VGroup(*[Square(0.36, stroke_color=GREEN_C, stroke_width=1.5, fill_color=GREEN_C, fill_opacity=0.12)
                        for _ in range(20)]).arrange_in_grid(4, 5, buff=0.08).move_to(mem.get_center() + DOWN * 0.3)
        bus = Line(cpu.get_right(), mem.get_left(), stroke_color=GREY_B, stroke_width=6)
        g = VGroup(cpu, cpu_l, regs, regs_l, alu, mem, mem_l, grid, bus)
        g.cpu, g.regs, g.alu, g.mem, g.grid, g.bus = cpu, regs, alu, mem, grid, bus
        g.core = VGroup(cpu, cpu_l, regs, regs_l, alu)
        g.far = VGroup(mem, mem_l, grid, bus)
        return g

    def quick_trips(self, d, n, rt=0.28):
        for k in range(n):
            a, b = d.regs[k % 5].get_center(), d.alu.get_left() + RIGHT * 0.2
            dot = Dot(a, radius=0.07, color=YELLOW_D)
            self.add(dot)
            self.play(dot.animate.move_to(b), run_time=rt, rate_func=linear)
            self.play(dot.animate.move_to(d.regs[(k + 2) % 5].get_center()), run_time=rt, rate_func=linear)
            self.remove(dot)

    def two_kinds(self):
        d = self.chip_diagram()
        self.say("因此，现代计算机至少有两种存数据的硬件。一是寄存器：在处理器内部，空间小，但快如闪电。",
                 FadeIn(d.core))
        self.quick_trips(d, 3)
        fast = zh("极快，但空间有限", 22, YELLOW_D).next_to(d.cpu, DOWN, buff=0.2)
        self.play(FadeIn(fast))
        lat = zh("约 100 ns ≈ 400 个周期", 24, GREEN_B).next_to(d.bus, UP, buff=0.15)
        big = zh("大得多，但慢", 22, GREEN_B).next_to(d.mem, DOWN, buff=0.2)
        self.say("二是内存：在处理器之外，大得多，但访问一次约 100 纳秒，相当于 400 个周期。",
                 FadeIn(d.far, shift=LEFT * 0.2), FadeIn(big))
        dot = Dot(d.cpu.get_right(), radius=0.09, color=GREEN_B)
        self.play(FadeIn(dot), FadeIn(lat))
        self.play(dot.animate.move_to(d.grid[7].get_center()), run_time=1.8, rate_func=linear)
        self.play(Indicate(d.grid[7], color=GREEN_B))
        self.play(dot.animate.move_to(d.regs[0].get_center()), run_time=1.8, rate_func=linear)
        self.play(FadeOut(dot), Indicate(d.regs[0], color=YELLOW_D))
        self.hold()
        self.clear_stage(self.head)

    def capacity(self):
        cw = 0.2
        cells = VGroup()
        for r in range(8):
            for c in range(4):
                cells.add(VGroup(*[
                    Square(cw, stroke_color=YELLOW_D, stroke_width=1.2, fill_color=YELLOW_D, fill_opacity=0.3)
                    .move_to([c * (4 * cw + 0.12) + b * cw, -r * (cw + 0.08), 0]) for b in range(4)]))
        cells.move_to([-3.8, 0.2, 0])
        lab = zh("32 个寄存器 × 4 字节 = 128 字节", 24, YELLOW_D).next_to(cells, UP, buff=0.3)
        fit(lab, 6.0)
        m1 = zh("笔记本：2–64 GB", 32, GREEN_B)
        m2 = zh("服务器：可达 1 TB", 32, GREEN_B)
        mems = VGroup(m1, m2).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.3, 0.3, 0])
        self.say("再比容量：32 个寄存器各 4 字节，总共才 128 字节；笔记本却有 2 到 64 GB 内存，服务器可达 1 TB。",
                 LaggedStart(*[FadeIn(c, scale=0.6) for c in cells], lag_ratio=0.03, run_time=1.6), FadeIn(lab),
                 FadeIn(mems, shift=LEFT * 0.2))
        self.hold()

        # zoom out: 128 B as a unit square vs 64 GB at the same scale
        R = np.array([-4.3, 0.7, 0])           # shared top-left corner (world coordinates)
        S = SIDE                               # memory side, in register-square units
        C = np.array([0.6, 0.15, 0])           # where the memory square ends up
        Z = S / 4.4
        M = R + np.array([S / 2, -S / 2, 0])
        F = (C - M / Z) / (1 - 1 / Z)
        z = ValueTracker(0.0)

        def k():
            return 10 ** z.get_value()

        def scr(p):
            return F + (p - F) / k()

        sq = Square(1.0, stroke_width=0, fill_color=YELLOW_D, fill_opacity=0.9).move_to(R + [0.5, -0.5, 0])
        sq_l = mono("128 B", 26, YELLOW_D).next_to(sq, UP, buff=0.15)
        self.say("把 128 字节画成小方块；同样比例下，64 GB 内存的面积约是它的 5 亿倍，小方块连一个像素都不到。",
                 FadeOut(lab), FadeOut(mems), ReplacementTransform(cells, sq), FadeIn(sq_l))
        mem_sq = always_redraw(lambda: clipped_square(scr(M), S / k(), GREEN_C,
                                                      0.2 * min(1.0, z.get_value() / 0.8)))
        reg_sq = always_redraw(lambda: Square(1.0 / k(), stroke_width=0, fill_color=YELLOW_D,
                                              fill_opacity=0.9).move_to(scr(R + np.array([0.5, -0.5, 0]))))
        zl = zh("缩小倍数", 22, GREY_A).move_to([5.3, 2.7, 0])
        zn = always_redraw(lambda: mono(f"×{k():,.0f}", 28, WHITE).next_to(zl, DOWN, buff=0.12))
        self.remove(sq)
        self.add(mem_sq, reg_sq, zl, zn)
        self.play(FadeOut(sq_l), run_time=0.4)
        self.play(z.animate.set_value(math.log10(Z)), run_time=5, rate_func=smooth)
        for m in (mem_sq, reg_sq, zn):
            m.clear_updaters()
        mem_l = zh("64 GB 内存", 34, GREEN_B).move_to(C)
        spot = scr(R + np.array([0.5, -0.5, 0]))
        ring = Circle(radius=0.22, stroke_color=YELLOW_D, stroke_width=3).move_to(spot)
        reg_l = zh("128 B 寄存器", 24, YELLOW_D).move_to(spot + np.array([-2.4, -0.55, 0]))
        ptr = Arrow(reg_l.get_right(), ring.get_left(), buff=0.08, color=YELLOW_D, stroke_width=3)
        self.play(FadeIn(mem_l), Create(ring), FadeIn(reg_l), GrowArrow(ptr))
        self.play(Indicate(ring, color=YELLOW_D, scale_factor=1.5))
        self.hold()
        self.clear_stage(self.head)

    def hierarchy(self):
        apex, base_y, half = np.array([-3.1, 2.4, 0]), -2.1, 3.5

        def hw(y):
            return half * (apex[1] - y) / (apex[1] - base_y)

        def band(y0, y1, col):
            pts = [[apex[0] - hw(y0), y0, 0], [apex[0] + hw(y0), y0, 0],
                   [apex[0] + hw(y1), y1, 0], [apex[0] - hw(y1), y1, 0]]
            if hw(y0) < 1e-6:
                pts = pts[1:]
            return Polygon(*pts, stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.2)

        ys = [2.4, 1.0, -0.55, -2.1]
        cols = [YELLOW_D, GREEN_C, BLUE_C]
        bands = VGroup(*[band(ys[i], ys[i + 1], cols[i]) for i in range(3)])
        names = VGroup(fit(zh("寄存器", 24, WHITE), 1.2), zh("DRAM 主存", 26, WHITE), zh("磁盘", 26, WHITE))
        for n, b, i in zip(names, bands, range(3)):
            n.move_to([apex[0], (ys[i] + ys[i + 1]) / 2 - (0.35 if i == 0 else 0), 0])
        gi = fit(zh("伟大思想 #3：局部性原理 / 存储层次", 22, GREY_A), 5.4).move_to([3.9, 2.75, 0])
        d_reg = zh("在处理器核心里 · 约 128 字节", 22, YELLOW_D)
        d_dram = VGroup(zh("在另一块芯片上 · DDR3/4/5、HBM", 22, GREEN_B),
                        zh("几十美元就能买到好几 GB", 22, GREEN_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        d_disk = zh("更大，也更慢", 22, BLUE_B)
        for d, y in zip((d_reg, d_dram, d_disk), (1.75, 0.2, -1.35)):
            fit(d, 5.5).move_to([1.2, y, 0], aligned_edge=LEFT)
        self.say("主存通常是另一块芯片上的 DRAM（如 DDR3/4/5、HBM），几十美元就能买好几 GB。",
                 LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in bands], lag_ratio=0.2), FadeIn(names),
                 FadeIn(gi), FadeIn(d_reg), FadeIn(d_dram, shift=LEFT * 0.15), FadeIn(d_disk))
        self.hold()
        speed = fit(zh("寄存器快 50–500 倍", 26, YELLOW_D), 5.5).move_to([1.2, 1.0, 0], aligned_edge=LEFT)
        rule = fit(zh("越小，越快", 30, YELLOW_D), 2.5).move_to([-5.4, 2.1, 0])
        self.say("但物理规律决定了：越小，越快。寄存器比 DRAM 快大约 50 到 500 倍。",
                 FadeIn(rule, shift=RIGHT * 0.2), FadeIn(speed, shift=LEFT * 0.2),
                 Indicate(bands[0], color=YELLOW_D, scale_factor=1.05))
        self.hold()
        self.clear_stage(self.head)

    def jim_gray(self):
        outline = Polygon(*[geo(*p) for p in CA], stroke_color=GREY_B, stroke_width=2,
                          fill_color=GREY_E, fill_opacity=0.4)
        cities = [(BERKELEY, "伯克利", LEFT), (SACRAMENTO, "萨克拉门托", RIGHT), (LOS_ANGELES, "洛杉矶", RIGHT)]
        marks = VGroup()
        for (lat, lon), name, side in cities:
            p = geo(lat, lon)
            marks.add(VGroup(Dot(p, radius=0.07, color=WHITE), zh(name, 20, GREY_A).next_to(p, side, buff=0.12)))
        B, Sa, LA = geo(*BERKELEY), geo(*SACRAMENTO), geo(*LOS_ANGELES)
        rows = [("寄存器：1 分钟（在脑子里）", YELLOW_D, 1), ("内存慢 100 倍：开车去萨克拉门托", GREEN_B, 100),
                ("内存慢 500 倍：去洛杉矶再回来", RED_B, 500)]
        x0, per = -6.4, 5.0 / 500
        labels, bars = VGroup(), VGroup()
        for i, (s, col, mins) in enumerate(rows):
            y = 2.2 - 1.35 * i
            labels.add(fit(zh(s, 24, col), 7.6).move_to([x0, y, 0], aligned_edge=LEFT))
            bars.add(Rectangle(width=max(mins * per, 0.04), height=0.3, stroke_width=0, fill_color=col,
                               fill_opacity=0.8).move_to([x0, y - 0.45, 0], aligned_edge=LEFT))
        car = Dot(B, radius=0.1, color=YELLOW_A)
        self.say("借用 Jim Gray 的比喻：从寄存器取数据，好比在脑子里回想一件事，花 1 分钟……",
                 FadeIn(outline), FadeIn(marks), FadeIn(labels[0]), GrowFromEdge(bars[0], LEFT))
        self.play(Indicate(marks[0][0], color=YELLOW_D, scale_factor=2))
        self.say("……那么慢 100 倍的内存，就像为了一张忘带的纸，开车去萨克拉门托取回来。",
                 FadeIn(labels[1]), FadeIn(car))
        bars[1].stretch(0.001, 0, about_edge=LEFT)
        self.add(bars[1])
        self.play(car.animate.move_to(Sa), bars[1].animate.stretch(500, 0, about_edge=LEFT), run_time=1.2,
                  rate_func=linear)
        self.play(car.animate.move_to(B), bars[1].animate.stretch(2, 0, about_edge=LEFT), run_time=1.2,
                  rate_func=linear)
        self.say("要是慢 500 倍，就得开车去洛杉矶再回来，只为了取一个数据！",
                 FadeIn(labels[2]))
        bars[2].stretch(0.001, 0, about_edge=LEFT)
        self.add(bars[2])
        self.play(car.animate.move_to(LA), bars[2].animate.stretch(500, 0, about_edge=LEFT), run_time=2.2,
                  rate_func=linear)
        self.play(car.animate.move_to(B), bars[2].animate.stretch(2, 0, about_edge=LEFT), run_time=2.2,
                  rate_func=linear)
        self.play(Indicate(bars[2], color=RED_B, scale_factor=1.05))
        self.hold()
        self.clear_stage(self.head)

        d = self.chip_diagram()
        self.say("寄存器数量很少，和处理器核心共用宝贵的芯片面积，非常昂贵。所以设计 ISA 像跳一支探戈：尽量在寄存器里算，少跑内存和磁盘。",
                 FadeIn(d))
        self.play(Indicate(d.regs, color=YELLOW_D, scale_factor=1.1))
        self.quick_trips(d, 4, rt=0.22)
        dot = Dot(d.cpu.get_right(), radius=0.09, color=GREEN_B)
        self.add(dot)
        self.play(dot.animate.move_to(d.grid[12].get_center()), run_time=1.4, rate_func=linear)
        self.play(dot.animate.move_to(d.regs[2].get_center()), run_time=1.4, rate_func=linear)
        self.remove(dot)
        self.quick_trips(d, 3, rt=0.22)
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ RISC vs CISC
    def event(self, year, label, h, color, align="center", star=False):
        x = yx(year)
        stem = Line([x, TL_Y, 0], [x, TL_Y + h, 0], stroke_color=color, stroke_width=2)
        mark = (Star(n=5, outer_radius=0.16, color=GOLD_B, fill_opacity=1).move_to([x, TL_Y, 0]) if star
                else Dot([x, TL_Y, 0], radius=0.08, color=color))
        lab = zh(label, 20, color).next_to(stem.get_end(), UP, buff=0.06)
        if align == "right":
            lab.align_to(np.array([x + 0.12, 0, 0]), RIGHT)
        elif align == "left":
            lab.align_to(np.array([x - 0.12, 0, 0]), LEFT)
        return VGroup(stem, mark, lab)

    def risc_cisc(self):
        axis = Line([-6.5, TL_Y, 0], [6.6, TL_Y, 0], stroke_color=GREY_B, stroke_width=3)
        ticks = VGroup(*[VGroup(Line([yx(y), TL_Y, 0], [yx(y), TL_Y - 0.12, 0], stroke_color=GREY_B, stroke_width=2),
                                mono(str(y), 18, GREY_B).move_to([yx(y), TL_Y - 0.3, 0]))
                         for y in range(1970, 2030, 10)])
        band = Rectangle(width=yx(1985) - yx(1970), height=0.26, stroke_width=0, fill_color=RED_C,
                         fill_opacity=0.45).move_to([(yx(1970) + yx(1985)) / 2, TL_Y, 0])
        band_l = zh("指令越来越复杂", 20, RED_B).next_to(band, UP, buff=0.12)
        self.timeline = VGroup(axis, ticks)
        seg_names = ["读内存", "相加", "写回内存"]
        cisc = VGroup(*[tag(s, RED_C, 2.3, 0.8, 26) for s in seg_names]).arrange(RIGHT, buff=0).move_to(UP * 0.25)
        cisc_l = zh("一条复杂指令", 22, RED_B).next_to(cisc, UP, buff=0.15)
        self.say("ISA 该怎样设计？七八十年代的潮流是让指令越来越复杂：一条指令同时读内存、运算、写回。",
                 Create(axis), FadeIn(ticks), GrowFromEdge(band, LEFT), FadeIn(band_l))
        self.play(FadeIn(cisc, shift=UP * 0.2), FadeIn(cisc_l))
        self.hold()

        rng = np.random.default_rng(7)
        hw_box = RoundedRectangle(corner_radius=0.1, width=2.8, height=1.2, stroke_color=RED_C, stroke_width=2.5,
                                  fill_color=RED_C, fill_opacity=0.08).move_to([-1.6, -1.5, 0])
        tangle = VGroup(*[
            CubicBezier(*[hw_box.get_center() + np.array([rng.uniform(-1.2, 1.2), rng.uniform(-0.45, 0.45), 0])
                          for _ in range(4)], stroke_color=RED_B, stroke_width=1.5)
            for _ in range(14)])
        hw_l = zh("硬件：复杂、昂贵", 24, RED_B).next_to(hw_box, RIGHT, buff=0.35)
        cisc_name = zh("CISC：复杂指令集计算机", 24, RED_B).next_to(hw_l, DOWN, buff=0.2).align_to(hw_l, LEFT)
        cisc_tag = mono("CISC", 18, WHITE).move_to(band)
        self.say("程序更短，访存也可能更少；代价是硬件复杂、造价高。这类架构后来被称为 CISC：复杂指令集计算机。",
                 Create(hw_box), Create(tangle, lag_ratio=0.1), FadeIn(hw_l))
        self.play(FadeIn(cisc_name), ReplacementTransform(band_l, cisc_tag))
        self.hold()

        ev801 = self.event(1980, "IBM 801 · John Cocke", 0.65, BLUE_B, align="right")
        self.say("80 年代初，IBM 的 John Cocke 设计出 IBM 801：第一台精简指令集计算机（RISC）。",
                 FadeIn(ev801, shift=DOWN * 0.1))
        self.hold()

        risc = VGroup(*[tag(m, BLUE_C, 2.0, 0.8, 30, font=MONO) for m in ("lw", "add", "sw")])
        risc.arrange(RIGHT, buff=0.45).move_to(UP * 0.35)
        subs = VGroup(*[zh(s, 20, GREY_A).next_to(r, DOWN, buff=0.1) for s, r in zip(seg_names, risc)])
        risc_l = zh("三条简单指令，每条只做一件事", 22, BLUE_B).next_to(risc, UP, buff=0.15)
        simple = VGroup(*[Line(hw_box.get_left() + RIGHT * 0.25 + UP * dy, hw_box.get_right() + LEFT * 0.25 + UP * dy,
                               stroke_color=BLUE_B, stroke_width=2) for dy in (-0.3, 0, 0.3)])
        hw_l2 = zh("硬件：简单、快", 24, BLUE_B).move_to(hw_l, aligned_edge=LEFT)
        self.say("思路正相反：指令集小而简单，复杂操作交给软件和编译器，用简单指令拼出来。",
                 *[ReplacementTransform(c[0], r[0]) for c, r in zip(cisc, risc)],
                 *[ReplacementTransform(c[1], s) for c, s in zip(cisc, subs)],
                 *[FadeIn(r[1]) for r in risc], ReplacementTransform(cisc_l, risc_l),
                 FadeOut(cisc_name))
        self.play(hw_box.animate.set_stroke(BLUE_C).set_fill(BLUE_C, 0.08), ReplacementTransform(tangle, simple),
                  ReplacementTransform(hw_l, hw_l2))
        self.hold()

        self.play(FadeOut(VGroup(risc, subs, risc_l, hw_box, simple, hw_l2)))
        unit, bx = 1.15, -2.3
        rc = fit(zh("CISC：1 条复杂指令", 24, RED_B), 3.7).move_to([-6.3, 0.6, 0], aligned_edge=LEFT)
        rr = fit(zh("RISC：3 条简单指令", 24, BLUE_B), 3.7).move_to([-6.3, -0.65, 0], aligned_edge=LEFT)
        cbar = Rectangle(width=4 * unit, height=0.5, stroke_color=RED_C, stroke_width=2, fill_color=RED_C,
                         fill_opacity=0.5).move_to([bx, 0.6, 0], aligned_edge=LEFT)
        rbars = VGroup(*[Rectangle(width=unit, height=0.5, stroke_color=BLUE_C, stroke_width=2, fill_color=BLUE_C,
                                   fill_opacity=0.5) for _ in range(3)]).arrange(RIGHT, buff=0)
        rbars.move_to([bx, -0.65, 0], aligned_edge=LEFT)
        for b, m in zip(rbars, ["lw", "add", "sw"]):
            b.add(mono(m, 20, WHITE).move_to(b))
        tax = Arrow([bx, -1.35, 0], [bx + 5.2, -1.35, 0], buff=0, color=GREY_B, stroke_width=3,
                    max_tip_length_to_length_ratio=0.05)
        tax_l = zh("时间", 22, GREY_A).next_to(tax, RIGHT, buff=0.12)
        note = zh("（示意）", 20, GREY).next_to(tax, DOWN, buff=0.1).align_to(tax, RIGHT)
        self.say("指令条数变多了，但简单的硬件每秒能执行多得多的指令，整体反而更快。",
                 FadeIn(rc), FadeIn(rr), GrowArrow(tax), FadeIn(tax_l), FadeIn(note))
        self.play(GrowFromEdge(cbar, LEFT, run_time=3.2, rate_func=linear),
                  Succession(*[GrowFromEdge(b, LEFT, run_time=0.8, rate_func=linear) for b in rbars]))
        done = zh("先完成", 22, BLUE_B).next_to(rbars, RIGHT, buff=0.2)
        self.play(FadeIn(done, shift=LEFT * 0.1), Indicate(rbars, color=BLUE_B, scale_factor=1.04))
        self.hold()
        self.play(FadeOut(VGroup(rc, rr, cbar, rbars, tax, tax_l, note, done)))

        ev_bm = self.event(1983, "伯克利 RISC · 斯坦福 MIPS", 1.2, GOLD_B, align="left")
        c1 = VGroup(zh("UC Berkeley · Dave Patterson", 26, GOLD_B), zh("RISC 项目", 24, GREY_A)).arrange(DOWN, buff=0.15)
        c2 = VGroup(zh("Stanford · John Hennessy", 26, RED_B), zh("MIPS 项目", 24, GREY_A)).arrange(DOWN, buff=0.15)
        cards = VGroup(c1, c2).arrange(RIGHT, buff=1.2).move_to(DOWN * 0.1)
        frames = VGroup(*[SurroundingRectangle(c, buff=0.25, corner_radius=0.12, color=col, stroke_width=2)
                          for c, col in zip(cards, (GOLD_C, RED_C))])
        self.say("伯克利的 Dave Patterson 和斯坦福的 John Hennessy 把它推向极致，同时做出了 RISC 和 MIPS 项目。",
                 FadeIn(ev_bm, shift=DOWN * 0.1), FadeIn(cards, shift=UP * 0.2), Create(frames))
        self.hold()

        st87 = self.event(1987, "图灵奖", 0.65, GOLD_B, align="left", star=True)
        st17 = self.event(2017, "图灵奖", 0.65, GOLD_B, align="right", star=True)
        people = VGroup(*[
            VGroup(Star(n=5, outer_radius=0.15, color=GOLD_B, fill_opacity=1), zh(n, 24, WHITE)).arrange(RIGHT, buff=0.18)
            for n in ["John Cocke · 1987", "Dave Patterson · 2017", "John Hennessy · 2017"]
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.35)
        self.say("三位先驱后来都获得了图灵奖：Cocke 在 1987 年，Patterson 和 Hennessy 在 2017 年。",
                 FadeOut(VGroup(cards, frames)), FadeIn(st87, shift=DOWN * 0.1), FadeIn(st17, shift=DOWN * 0.1),
                 LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in people], lag_ratio=0.3))
        self.hold()

        x86 = VGroup(zh("CISC", 28, RED_B), tag("x86", RED_C, 2.6, 0.8, 30, font=MONO),
                     zh("Intel i3/i5/i7/i9、许多 AMD 处理器", 20, GREY_A),
                     zh("许多 Windows 电脑", 20, GREY_A)).arrange(DOWN, buff=0.18)
        arm = VGroup(zh("RISC", 28, BLUE_B), tag("ARM", BLUE_C, 2.6, 0.8, 30, font=MONO),
                     zh("很多手机", 20, GREY_A), zh("苹果自研芯片（Apple silicon）", 20, GREY_A)).arrange(DOWN, buff=0.18)
        today = VGroup(x86, arm).arrange(RIGHT, buff=2.0, aligned_edge=UP).move_to(DOWN * 0.3)
        race = DoubleArrow(x86[0].get_right(), arm[0].get_left(), buff=0.3, color=GREY_B, stroke_width=3,
                           max_tip_length_to_length_ratio=0.08)
        race_l = zh("都在快速发展", 20, GREY_A).next_to(race, UP, buff=0.08)
        self.say("如今 RISC 和 CISC 都很流行、都在快速发展：许多 Windows 电脑用 x86，很多手机和苹果自研芯片用 ARM。",
                 FadeOut(people), FadeIn(x86[0], shift=UP * 0.2), FadeIn(arm[0], shift=UP * 0.2),
                 GrowFromCenter(race), FadeIn(race_l))
        self.play(FadeIn(x86[1:], shift=UP * 0.2), FadeIn(arm[1:], shift=UP * 0.2))
        self.hold()
        self.play(FadeOut(today), FadeOut(race), FadeOut(race_l))

    # ------------------------------------------------------------------ why RISC-V
    def why_riscv(self):
        def card(title, sub, col, font=MONO):
            t = tag(title, col, 3.6, 0.8, 28, font=font)
            s = fit(zh(sub, 22, GREY_A), 3.8).next_to(t, DOWN, buff=0.2)
            return VGroup(t, s)

        c_x86 = card("x86", "太复杂", RED_C)
        c_toy = card("老旧或“自创”的 ISA", "缺少真正的编译器和软件", GREY_B, font=CJK)
        c_rv = card("RISC-V", "?", YELLOW_D)
        cards = VGroup(c_x86, c_toy, c_rv).arrange(RIGHT, buff=0.55).move_to(DOWN * 0.2)
        self.say("教学总得选一个 ISA：x86 太复杂；老旧或“自创”的 ISA，又缺少真正的编译器和软件。",
                 LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards[:2]], lag_ratio=0.3))
        self.play(c_x86.animate.fade(0.65), c_toy.animate.fade(0.65), FadeIn(c_rv, shift=UP * 0.2))

        ev10 = self.event(2010, "RISC-V 诞生", 1.2, YELLOW_D, align="right")
        ev20 = self.event(2020, "MIPS → RISC-V", 1.2, GREY_A, align="right")
        born = VGroup(zh("2010 · UC Berkeley · Par Lab", 30, YELLOW_D),
                      zh("Dave Patterson · Krste Asanovic", 26, GREY_A)).arrange(DOWN, buff=0.15)
        born.next_to(c_rv[0], DOWN, buff=0.35)
        fit(born, 4.2)
        born.set_x(min(born.get_x(), 6.7 - born.width / 2))
        self.say("RISC-V 于 2010 年诞生在 UC Berkeley 的 Par Lab，由 Patterson 和 Krste Asanovic 发起；到 2020 年前后，连 MIPS 都转向了它。",
                 FadeIn(ev10, shift=DOWN * 0.1), FadeOut(c_rv[1]), FadeIn(born, shift=UP * 0.1))
        self.play(FadeIn(ev20, shift=DOWN * 0.1))
        self.hold()

        self.play(FadeOut(VGroup(c_x86, c_toy, born)), c_rv[0].animate.move_to(UP * 0.7))
        b1 = tag("开源", GREEN_C, 2.6, 0.8, 28)
        b2 = tag("免授权费", GREEN_C, 2.6, 0.8, 28)
        uses = VGroup(*[tag(s, GREY_B, 1.9, 0.6, 24, fill=0.06) for s in ["教学", "研究", "商用"]])
        VGroup(b1, b2).arrange(RIGHT, buff=0.6).move_to(DOWN * 0.45)
        uses.arrange(RIGHT, buff=0.4).move_to(DOWN * 1.55)
        self.say("它受欢迎有两大原因：开源、免授权费。谁都能免费用，教学、研究、商用都行。",
                 FadeIn(b1, shift=UP * 0.2), FadeIn(b2, shift=UP * 0.2),
                 LaggedStart(*[FadeIn(u) for u in uses], lag_ratio=0.3))
        self.hold()

        self.play(FadeOut(VGroup(b1, b2, uses)))
        small = chip_icon("MCU", 0.6, TEAL_C).move_to([-4.6, -0.8, 0])
        rack = VGroup(*[RoundedRectangle(corner_radius=0.05, width=1.2, height=0.28, stroke_color=BLUE_C, stroke_width=2,
                                         fill_color=BLUE_C, fill_opacity=0.2) for _ in range(6)]).arrange(DOWN, buff=0.05)
        racks = VGroup(*[rack.copy() for _ in range(3)]).arrange(RIGHT, buff=0.15).move_to([4.3, -0.8, 0])
        s_l = zh("嵌入式微控制器", 22, TEAL_B).next_to(small, DOWN, buff=0.25)
        r_l = zh("仓库级超级计算机", 22, BLUE_B).next_to(racks, DOWN, buff=0.2)
        span_ = DoubleArrow(small.get_right() + RIGHT * 0.3, racks.get_left() + LEFT * 0.3, buff=0,
                            color=YELLOW_D, stroke_width=3, max_tip_length_to_length_ratio=0.06)
        world = VGroup(zh("全球学术界与产业界共同推动", 22, GREY_A),
                       mono("RISC-V International", 20, GREY_B)).arrange(DOWN, buff=0.1)
        fit(world, span_.width).next_to(span_, UP, buff=0.2)
        self.say("全球学界和业界共同推动它。从嵌入式微控制器，到仓库级超级计算机，都已经有人用它来打造。",
                 FadeIn(small), FadeIn(s_l), GrowArrow(span_), FadeIn(world), FadeIn(racks, lag_ratio=0.2), FadeIn(r_l))
        self.hold()
        self.clear_stage()

    def rv32i(self):
        head = self.heading("RV32I 与“绿卡”")
        name = VGroup(mono("RV", 80, YELLOW_D), mono("32", 80, BLUE_B), mono("I", 80, GREEN_B)).arrange(RIGHT, buff=0.08)
        name.move_to([-3.4, 1.7, 0])
        notes = VGroup(
            zh("RISC-V", 22, YELLOW_D).next_to(name[0], DOWN, buff=0.3),
            zh("32 位", 22, BLUE_B).next_to(name[1], DOWN, buff=0.3),
            zh("基础整数指令集", 22, GREEN_B).next_to(name[2], DOWN, buff=0.3),
        )
        notes[2].shift(RIGHT * 0.6)
        gap = notes[1].get_right()[0] + 0.3 - notes[2].get_left()[0]
        if gap > 0:                            # English "32-bit" is wider than "32 位"
            notes[2].shift(RIGHT * gap)
        var = VGroup(*[mono(s, 26, GREY_A) for s in ("RV32", "RV64", "RV128")]).arrange(RIGHT, buff=0.5)
        var.next_to(name, UP, buff=0.35)
        self.say("RISC-V 有 32、64、128 位等变体。本系列学 RV32I：32 位基础整数指令集；乘法等功能则放在 M 等扩展里。",
                 Write(head), FadeIn(var, lag_ratio=0.2), FadeIn(name, shift=UP * 0.2))
        self.play(var[0].animate.set_color(BLUE_B), var[1:].animate.set_opacity(0.4),
                  LaggedStart(*[FadeIn(n, shift=UP * 0.1) for n in notes], lag_ratio=0.3))

        base = tag("RV32I 基础指令集", GREEN_C, 5.0, 0.8, 26).move_to([-3.4, -1.55, 0])
        ext_m = tag("M：乘除法", GOLD_C, 2.35, 0.7, 24)
        ext_f = tag("F：浮点", PURPLE_B, 2.35, 0.7, 24)
        exts = VGroup(ext_m, ext_f).arrange(RIGHT, buff=0.3).next_to(base, UP, buff=0.12)
        ext_l = zh("可选扩展", 20, GREY_A).next_to(exts, UP, buff=0.1)
        self.play(FadeIn(base, shift=UP * 0.2))
        self.play(FadeIn(ext_m, shift=DOWN * 0.4), FadeIn(ext_f, shift=DOWN * 0.4), FadeIn(ext_l))
        self.play(Indicate(ext_m, color=GOLD_B))
        self.hold()

        card = RoundedRectangle(corner_radius=0.1, width=3.8, height=4.4, stroke_color=GREEN_C, stroke_width=3,
                                fill_color=GREEN_E, fill_opacity=0.6).move_to([4.2, 0.2, 0])
        card_t = zh("RISC-V 绿卡", 24, WHITE).next_to(card.get_top(), DOWN, buff=0.18)
        ops = ["add", "sub", "xor", "or", "and", "sll", "srl", "sra", "slt", "sltu",
               "addi", "xori", "ori", "andi", "slli", "srli", "srai", "slti", "sltiu",
               "lb", "lh", "lw", "lbu", "lhu", "sb", "sh", "sw",
               "beq", "bne", "blt", "bge", "bltu", "bgeu", "jal", "jalr", "lui", "auipc", "fence", "ecall", "ebreak"]
        assert len(ops) == 40                     # the RV32I base instructions
        table = VGroup(*[mono(o, 16, GREEN_A) for o in ops]).arrange_in_grid(cols=4, buff=(0.25, 0.12),
                                                                              col_alignments="llll")
        fit(table, 3.3).next_to(card_t, DOWN, buff=0.2)
        ibm = zh("名字来自 1960 年代的 IBM 360 绿卡", 20, GREY_A).next_to(card, DOWN, buff=0.1)
        fit(ibm, 4.2)
        self.say("整个架构的定义一页纸就能装下，叫作“绿卡”，名字来自 1960 年代著名的 IBM 360 绿卡。",
                 FadeIn(card, shift=LEFT * 0.3), FadeIn(card_t), FadeIn(table, lag_ratio=0.02), FadeIn(ibm))
        self.hold()
        bears = zh("Go Bears!", 30, GOLD_B).move_to([-3.4, 0.45, 0])
        self.say("简洁、优雅，学汇编、学设计计算机都合适：这正是 CS61C 教它的原因。Go Bears！",
                 Circumscribe(card, color=YELLOW_D), FadeIn(bears, scale=1.3))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ roadmap
    def roadmap(self):
        tiles = VGroup()
        for i, ep in enumerate(series.SERIES):
            r = RoundedRectangle(corner_radius=0.1, width=6.3, height=0.52, stroke_color=GREY_B, stroke_width=2,
                                 fill_color=GREY_E, fill_opacity=0.3)
            num = mono(f"{i + 1:02d}", 22, YELLOW_D).move_to(r.get_left() + RIGHT * 0.45)
            t = fit(zh(series.title(ep, LANG), 24, WHITE), 5.1)
            t.next_to(num, RIGHT, buff=0.3)
            tiles.add(VGroup(r, num, t))
        for i, tl in enumerate(tiles):
            col, row = divmod(i, 7)
            tl.move_to([-3.3 + 6.6 * col, 2.55 - 0.66 * row, 0])
        self.say("全系列共 14 集。下一集，从一行 C 代码出发，看它怎样变成汇编，并认识 RISC-V 的寄存器。",
                 LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.08, run_time=2.5))
        self.play(tiles[0][0].animate.set_stroke(YELLOW_D).set_fill(YELLOW_D, 0.15))
        self.play(tiles[1][0].animate.set_stroke(GREEN_C, 3).set_fill(GREEN_C, 0.25),
                  tiles[0][0].animate.set_stroke(GREY_B).set_fill(GREY_E, 0.3))
        self.play(Indicate(tiles[1], color=GREEN_B, scale_factor=1.05))
        self.hold()
