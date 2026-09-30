"""Newton–Schulz iteration, EECS 182 Fall 2026 Discussion 5, focused on part (e):
a singular value that starts at +σ, where does it end up, and why?

Every number on screen is computed below; the key ones are asserted.
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---------------------------------------------------------------- the math


def p(x):
    return 1.5 * x - 0.5 * x ** 3


def dp(x):
    return 1.5 - 1.5 * x ** 2


S3, S5 = math.sqrt(3), math.sqrt(5)


def _next_b(prev):
    """The unique b in (√3, √5) with p(b) = −prev, i.e. b³ − 3b = 2·prev."""
    lo, hi = S3, S5
    for _ in range(200):
        m = (lo + hi) / 2
        if m ** 3 - 3 * m < 2 * prev:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


B = [S3]
for _ in range(14):
    B.append(_next_b(B[-1]))


def orbit(x, n):
    out = [x]
    for _ in range(n):
        x = p(x)
        out.append(x)
    return out


def fate(x, n=400):
    """(limit, number of sign flips) of the orbit of x."""
    flips = 0
    for _ in range(n):
        y = p(x)
        if abs(y) > 1e6:
            return "diverges", flips
        flips += y * x < 0
        x = y
    return round(x, 9), flips


def _root(c, lo, hi):
    """x in [lo, hi] with p(x) = c, p decreasing there."""
    for _ in range(200):
        m = (lo + hi) / 2
        if p(m) > c:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


# fixed points and their slopes
assert p(0) == 0 and p(1) == 1 and p(-1) == -1
assert dp(0) == 1.5 and dp(1) == 0 and dp(-1) == 0
# the two thresholds
assert abs(p(S3)) < 1e-12 and abs(p(-S3)) < 1e-12
assert abs(p(S5) + S5) < 1e-12 and abs(p(-S5) - S5) < 1e-12
assert abs(dp(S5) + 6) < 1e-12
# the boundary points (values from the brief)
for b, want in zip(B[1:4], (2.14776346, 2.22122772, 2.23359117)):
    assert abs(b - want) < 1e-8, (b, want)
for k in range(1, 12):
    assert abs(p(B[k]) + B[k - 1]) < 1e-12 and B[k - 1] < B[k] < S5
# √5 − b_n shrinks by ~6 each time
assert abs((S5 - B[6]) / (S5 - B[7]) - 6) < 0.01
# the three neighbours of the opening
assert fate(2.0) == (-1.0, 1) and fate(2.2) == (1.0, 2) and fate(2.23) == (-1.0, 3)
assert p(2.0) == -1.0
# every point of (b_{n-1}, b_n) flips exactly n times and ends at (−1)^n
for n in range(1, 7):
    for s in (0.1, 0.5, 0.9):
        x = B[n - 1] + s * (B[n] - B[n - 1])
        assert fate(x) == ((-1.0) ** n, n), (n, s, fate(x))
assert fate(1.6) == (1.0, 0) and fate(0.3) == (1.0, 0) and fate(0.05) == (1.0, 0)
assert fate(2.3)[0] == "diverges"

# ---------------------------------------------------------------- colors (one per concept)

C_P = BLUE_C        # the curve y = p(x)
C_DIAG = GREY_B     # y = x
C_PLUS = TEAL_C     # positive values, fate +1
C_MINUS = GOLD_C    # negative values, fate −1
C_ZERO = PURPLE_B   # √3, 0 and the boundary points that fall into it
C_S5 = RED_C        # √5 and divergence
C_SIG = YELLOW_D    # Σ, singular values

PANEL_X = 3.65      # centre of the right-hand panel next to the graph


def sign_color(x):
    return C_PLUS if x > 0 else C_MINUS


def num(v, d=2):
    """A number for MathTex, with a real minus sign."""
    return f"{v:.{d}f}"


def mt(s, size=36, color=C_TEXT):
    return MathTex(s, font_size=size, color=color)


def neg(s):
    return s.replace("-", "−")


class Ep01NewtonSchulz(NarratedScene):
    # Latin captions: Pango wraps a single over-long line on its own (and the
    # wrapped lines overlap), so keep each caption line short
    caption_units = 30

    def construct(self):
        self.title_card()
        self.hook()
        self.origin()
        self.graph()
        self.fixed_points()
        self.below_sqrt3()
        self.two_thresholds()
        self.edge_sqrt5()
        self.flip_zone()
        self.first_boundary()
        self.basins()
        self.boundary_points()
        self.summary()
        self.back_to_matrix()
        self.end_card([
            "Newton–Schulz 只改变奇异值：每个 σ 各自迭代 p(x)",
            "不动点 −1、0、1：±1 稳定（斜率 0），0 不稳定（斜率 1.5）",
            "√3 决定翻不翻号，√5 决定变小还是变大",
            "√3 到 √5 之间：翻号次数的奇偶决定去 −1 还是 +1",
            "分界点 bn 挤向 √5，自身落到 0；√5 周期为 2，更大的发散",
            "所以迭代前先缩放 W，让所有奇异值小于 √3",
        ])

    # ------------------------------------------------------------ helpers
    def number_row(self, y, lo=-2.5, hi=2.5, length=10.2, x=0.7, marks=(-2, -1, 0, 1, 2)):
        nl = NumberLine(x_range=[lo, hi, 0.5], length=length, color=GREY_B, stroke_width=2,
                        tick_size=0.05, include_tip=False)
        nl.move_to([x, y, 0])
        labels = VGroup(*[
            mono(neg(str(v)), 18, GREY_B).next_to(nl.n2p(v), DOWN, buff=0.14) for v in marks
        ])
        return VGroup(nl, labels)

    def hop(self, dot, line, x_old, x_new, color=None):
        a = 0.55 * PI if x_new < x_old else -0.55 * PI
        anim = dot.animate(path_arc=a).move_to(line.n2p(x_new))
        return anim.set_color(color or sign_color(x_new))

    def make_graph(self):
        ax = Axes(x_range=[-2.5, 2.5, 0.5], y_range=[-2.5, 2.5, 0.5], x_length=5.4, y_length=5.4,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2,
                               "tick_size": 0.04})
        ax.move_to([-3.45, 0.3, 0])
        nums = VGroup()
        for v in (-2, -1, 1, 2):
            nums.add(mono(neg(str(v)), 18, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.12))
            nums.add(mono(neg(str(v)), 18, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12))
        xc = _root(-2.5, 1.0, 2.5)
        curve = ax.plot(p, x_range=[-xc, xc], color=C_P, stroke_width=4)
        diag = ax.plot(lambda x: x, x_range=[-2.5, 2.5], color=C_DIAG, stroke_width=2.5)
        lab_p = mt("y=p(x)", 32, C_P).move_to(ax.c2p(-1.1, 1.55))
        lab_d = mt("y=x", 32, C_DIAG).move_to(ax.c2p(2.15, 1.45))
        self.ax, self.curve, self.diag = ax, curve, diag
        self.graph_group = VGroup(ax, nums, curve, diag, lab_p, lab_d)
        return self.graph_group

    def web(self, x0, n, color, width=3.0):
        ax = self.ax
        pts = [ax.c2p(x0, 0)]
        x = x0
        for _ in range(n):
            y = p(x)
            if abs(y) > 2.45:
                break
            pts += [ax.c2p(x, y), ax.c2p(y, y)]
            x = y
        segs = VGroup()
        for a, b in zip(pts, pts[1:]):
            if np.linalg.norm(b - a) > 0.012:
                segs.add(Line(a, b, color=color, stroke_width=width))
        return segs

    def draw(self, segs, per=0.35):
        return Succession(*[Create(s, rate_func=linear) for s in segs], run_time=per * len(segs))

    def start_mark(self, x0, color, label=None):
        d = Dot(self.ax.c2p(x0, 0), radius=0.06, color=color)
        lab = mt(label or num(x0, 1), 26, color).next_to(d, DOWN, buff=0.42)
        return VGroup(d, lab)

    def panel(self, *mobs, y=2.4, buff=0.35):
        g = VGroup(*mobs).arrange(DOWN, buff=buff)
        g.move_to([PANEL_X, 0, 0]).set_y(y - g.height / 2)
        return g

    # ------------------------------------------------------------ 1. the mystery
    def hook(self):
        f = MathTex(r"x", r"\;\longmapsto\;", r"\tfrac32\,x-\tfrac12\,x^3", font_size=50)
        f[2].set_color(C_P)
        f.to_edge(UP, buff=0.55)
        self.say("取一个数，反复把它代入同一个三次多项式。", Write(f))

        starts = [2.0, 2.2, 2.23]
        rows, dots, names = VGroup(), VGroup(), VGroup()
        for i, x0 in enumerate(starts):
            row = self.number_row(1.35 - 1.45 * i)
            nl = row[0]
            for v, c in ((1, C_PLUS), (-1, C_MINUS)):
                row.add(Line(nl.n2p(v) + DOWN * 0.1, nl.n2p(v) + UP * 0.1, color=c, stroke_width=4))
            names.add(mt(r"x_0=" + num(x0), 32).next_to(nl, LEFT, buff=0.3))
            dots.add(Dot(nl.n2p(x0), radius=0.1, color=sign_color(x0)))
            rows.add(row)
        self.say("从三个挨得很近的数出发：2.00、2.20 和 2.23。",
                 LaggedStart(*[FadeIn(VGroup(r, n)) for r, n in zip(rows, names)], lag_ratio=0.2),
                 LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.2))

        orbs = [orbit(x0, 6) for x0 in starts]
        trails = VGroup()
        self.add(trails)

        def step(k):
            anims = []
            for i in range(3):
                nl = rows[i][0]
                t = Dot(nl.n2p(orbs[i][k - 1]), radius=0.045, color=GREY_B, fill_opacity=0.6)
                trails.add(t)
                anims.append(self.hop(dots[i], nl, orbs[i][k - 1], orbs[i][k]))
            return anims

        self.say("每迭代一步，它们都在正负之间来回跳……", *step(1), run_time=1.1)
        for k in range(2, 7):
            self.play(*step(k), run_time=0.9)
        fates = VGroup()
        for i, x0 in enumerate(starts):
            lim, _ = fate(x0)
            fates.add(mt(("+" if lim > 0 else "") + str(int(lim)), 34, sign_color(lim))
                      .next_to(rows[i][0], RIGHT, buff=0.3))
        self.say("最后，2.00 停在 −1，2.20 停在 +1，2.23 又回到了 −1。",
                 LaggedStart(*[FadeIn(f_, shift=LEFT * 0.2) for f_ in fates], lag_ratio=0.3),
                 LaggedStart(*[Flash(d, color=d.get_color()) for d in dots], lag_ratio=0.3))
        self.say("起点只差一点点，终点却正负交替。为什么？这就是这支视频要解开的谜。")
        self.hold(0.5)
        self.clear_stage()

    # ------------------------------------------------------------ 2. where p comes from
    def origin(self):
        it = MathTex(r"W_{k+1}", r"=", r"\tfrac12\left(3I-W_kW_k^{\top}\right)W_k", font_size=44)
        it.to_edge(UP, buff=0.7)
        tag = txt("Newton–Schulz 迭代", 30, GREY_A).next_to(it, DOWN, buff=0.3)
        self.say("Newton–Schulz 迭代来自 CS182 第五次讨论课：它反复改写一个矩阵 W，这个多项式就藏在里面。",
                 Write(it), FadeIn(tag))

        svd = MathTex(r"W", r"=", r"U", r"\;\;\Sigma\;\;", r"V^{\top}", font_size=52)
        svd[3].set_color(C_SIG)
        svd.move_to(UP * 0.7)
        rot_u = txt("旋转", 22, GREY_B).next_to(svd[2], DOWN, buff=0.25)
        rot_v = txt("旋转", 22, GREY_B).next_to(svd[4], DOWN, buff=0.25)
        stretch = txt("拉伸", 22, C_SIG).next_to(svd[3], DOWN, buff=0.7)
        self.say("把 W 做奇异值分解：U 和 V 只负责旋转，拉伸的大小全在中间的 Σ 里。",
                 FadeOut(tag), Write(svd), FadeIn(VGroup(rot_u, rot_v, stretch), shift=UP * 0.1))

        d1 = MathTex(r"WW^{\top}", r"=U\Sigma V^{\top}V\Sigma U^{\top}", r"=U\Sigma^2U^{\top}", font_size=38)
        d2 = MathTex(r"p(W)", r"=U\,\tfrac12\left(3I-\Sigma^2\right)\Sigma\,V^{\top}", r"=U\,p(\Sigma)\,V^{\top}",
                     font_size=38)
        derive = VGroup(d1, d2).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 1.2)
        self.say("代进去一算，U 和 V 原封不动地留在两边，p 只作用在中间的 Σ 上。",
                 VGroup(rot_u, rot_v, stretch).animate.set_opacity(0),
                 Write(d1), run_time=1.6)
        self.play(Write(d2), run_time=1.6)
        self.play(Circumscribe(d2[2], color=C_SIG))
        self.hold()
        self.remove(rot_u, rot_v, stretch)

        sig = Matrix([[r"\sigma_1", "0", "0"], ["0", r"\sigma_2", "0"], ["0", "0", r"\sigma_3"]],
                     h_buff=1.5).scale(0.8)
        psig = Matrix([[r"p(\sigma_1)", "0", "0"], ["0", r"p(\sigma_2)", "0"], ["0", "0", r"p(\sigma_3)"]],
                      h_buff=1.5).scale(0.8)
        for m in (sig, psig):
            for k in (0, 4, 8):
                m.get_entries()[k].set_color(C_SIG)
        lhs = mt(r"\Sigma=", 44, C_SIG)
        grp = VGroup(lhs, sig).arrange(RIGHT, buff=0.25).move_to(DOWN * 0.4)
        self.play(FadeOut(VGroup(d1, d2)), svd.animate.shift(UP * 0.5))
        self.say("Σ 是对角矩阵，所以每个奇异值各自独立地变成 p(σ)，互不干扰。", FadeIn(grp))
        lhs2 = mt(r"p(\Sigma)=", 44, C_SIG).move_to(lhs, aligned_edge=RIGHT)
        psig.move_to(sig, aligned_edge=LEFT)
        self.play(ReplacementTransform(sig, psig), ReplacementTransform(lhs, lhs2), run_time=1.4)
        self.hold()

        goal = MathTex(r"U\,I\,V^{\top}", r"=", r"UV^{\top}", font_size=48).move_to(DOWN * 0.4)
        ortho = txt("正交矩阵", 26, C_PLUS).next_to(goal[2], DOWN, buff=0.3)
        self.say("如果所有奇异值都被推到 1，W 就只剩下 U 乘 V 的转置：一个正交矩阵。这就是“正交化”。",
                 FadeOut(VGroup(lhs2, psig), shift=DOWN * 0.2), FadeIn(goal), FadeIn(ortho))
        self.hold()

        px = MathTex(r"p(x)", r"=", r"\tfrac32\,x-\tfrac12\,x^3", font_size=60)
        px[2].set_color(C_P)
        box = SurroundingRectangle(px, color=C_P, buff=0.25, corner_radius=0.1)
        self.play(FadeOut(VGroup(it, svd, goal, ortho)))
        self.say("所以可以先忘掉矩阵，只盯着一个数 x，看它在 p 的反复作用下去哪。",
                 Write(px), Create(box))
        q = VGroup(*[mt(s, 44, c) for s, c in
                     ((r"+1", C_PLUS), (r"-1", C_MINUS), (r"0", C_ZERO), (r"\infty", C_S5))])
        q.arrange(RIGHT, buff=1.2).next_to(box, DOWN, buff=0.8)
        self.say("第 (e) 问正是：奇异值从正数 σ 出发，最后去 +1、−1、0，还是发散？",
                 LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in q], lag_ratio=0.2))
        self.hold()
        corner = MathTex(r"p(x)=\tfrac32x-\tfrac12x^3", font_size=34).to_corner(UR, buff=0.35)
        corner[0][5:].set_color(C_P)
        self.play(FadeOut(q), FadeOut(box), ReplacementTransform(px, corner))
        self.corner = corner

    # ------------------------------------------------------------ 3. graph and cobweb
    def graph(self):
        g = self.make_graph()
        ax, curve, diag = self.ax, self.curve, self.diag
        self.say("画出 y = p(x)，再画出对角线 y = x。",
                 Create(ax), FadeIn(g[1]), Create(curve), Create(diag), FadeIn(g[4]), FadeIn(g[5]),
                 run_time=2.0)
        rule = VGroup(
            txt("1. 竖直走到曲线：得到 p(x)", 24),
            txt("2. 水平走到对角线：把 p(x) 当作新的 x", 24),
            txt("3. 重复", 24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rule.move_to([PANEL_X, 1.2, 0])
        if rule.width > 6.2:
            rule.scale_to_fit_width(6.2)
        w = self.web(0.3, 8, WHITE)
        m = self.start_mark(0.3, WHITE)
        self.say("这叫蛛网图。从起点竖直走到曲线，到达的高度就是下一个值 p(x)；",
                 FadeIn(m), FadeIn(rule[0]), Create(w[0]))
        self.say("再水平走到对角线，把这个高度搬回横轴的位置，作为新的 x。",
                 FadeIn(rule[1]), Create(w[1]))
        self.say("讨论课的例子从 0.3 出发：重复这两步，台阶一级一级爬向 1。",
                 FadeIn(rule[2]), self.draw(w[2:], 0.3))
        self.hold()
        w2 = self.web(1.2, 5, WHITE)
        m2 = self.start_mark(1.2, WHITE)
        self.say("从 1.2 出发，先落到 1 的下方，然后同样贴上 1。",
                 FadeOut(VGroup(w, m)), FadeIn(m2), self.draw(w2, 0.4))
        self.hold()
        self.play(FadeOut(VGroup(w2, m2, rule)))

    # ------------------------------------------------------------ 4. fixed points and stability
    def fixed_points(self):
        ax = self.ax
        fps = VGroup(*[Dot(ax.c2p(v, v), radius=0.09, color=c)
                       for v, c in ((-1, C_MINUS), (0, C_ZERO), (1, C_PLUS))])
        eqs = self.panel(
            mt(r"x=\tfrac32x-\tfrac12x^3", 38),
            mt(r"\Longleftrightarrow\; x^3=x", 38),
            mt(r"\Longleftrightarrow\; x\in\{-1,\,0,\,1\}", 38),
            y=2.7, buff=0.25)
        self.say("曲线和对角线的交点满足 p(x) = x，叫作不动点：一旦落在上面，就永远不动。",
                 LaggedStart(*[GrowFromCenter(d) for d in fps], lag_ratio=0.25))
        self.say("解这个方程，化简后是 x 的立方等于 x，所以不动点是 −1、0 和 1。",
                 Write(eqs), run_time=2.0)
        self.hold()

        der = mt(r"p'(x)=\tfrac32-\tfrac32x^2", 38).move_to([PANEL_X, 0.6, 0])
        self.say("但不动点分两种：吸引的和排斥的。区别在于 p 在那里的斜率。",
                 eqs.animate.set_opacity(0.35), Write(der))
        tan0 = ax.plot(lambda x: 1.5 * x, x_range=[-0.9, 0.9], color=C_ZERO, stroke_width=3)
        near0 = orbit(0.05, 4)
        s0 = mt(r"p'(0)=\tfrac32>1", 36, C_ZERO)
        seq0 = mt(r"\to ".join(num(v, 3) for v in near0) + r"\to\cdots", 30)
        g0 = VGroup(s0, seq0).arrange(DOWN, buff=0.25).next_to(der, DOWN, buff=0.45)
        if g0.width > 6.2:
            g0.scale_to_fit_width(6.2)
        w0 = self.web(0.05, 10, C_ZERO, width=2.5)
        self.say("在 0 处斜率是 1.5：偏差每步放大 1.5 倍。从 0.05 出发，很快就被推开。",
                 Create(tan0), FadeIn(s0))
        self.play(FadeIn(seq0), self.draw(w0, 0.22))
        self.hold()

        near1 = orbit(1.2, 3)
        errs = [abs(v - 1) for v in near1]
        assert errs[1] < errs[0] ** 2 * 1.7 and errs[2] < errs[1] ** 2 * 1.7
        s1 = mt(r"p'(\pm1)=0", 36, C_PLUS)
        seq1 = mt(r"|x-1|:\ " + r"\to ".join(f"{e:.2g}" for e in errs[:3]) + r"\to\cdots", 30)
        g1 = VGroup(s1, seq1).arrange(DOWN, buff=0.25).next_to(der, DOWN, buff=0.45)
        tan1 = VGroup(ax.plot(lambda x: 1, x_range=[0.5, 1.5], color=C_PLUS, stroke_width=3),
                      ax.plot(lambda x: -1, x_range=[-1.5, -0.5], color=C_MINUS, stroke_width=3))
        self.say("在 ±1 处斜率是 0：偏差每一步差不多被平方。从 1.2 出发，误差是 0.2、0.064、0.006……",
                 FadeOut(VGroup(g0, w0, tan0)), Create(tan1), FadeIn(g1))
        self.hold()
        lab0 = txt("不稳定", 22, C_ZERO).next_to(fps[1], RIGHT, buff=0.3).shift(DOWN * 0.45)
        lab1 = txt("稳定", 22, C_PLUS).next_to(fps[2], DOWN, buff=0.25).shift(RIGHT * 0.2)
        lab_1 = txt("稳定", 22, C_MINUS).next_to(fps[0], UP, buff=0.25).shift(LEFT * 0.2)
        self.say("所以 0 是不稳定的不动点，像山顶；±1 是稳定的，像谷底。",
                 FadeIn(VGroup(lab0, lab1, lab_1)))
        self.hold()
        self.play(FadeOut(VGroup(eqs, der, g1, tan1, lab0, lab1, lab_1)))
        self.fps = fps

    # ------------------------------------------------------------ 5. 0 < σ < √3
    def below_sqrt3(self):
        ax = self.ax
        fac = MathTex(r"p(x)", r"=", r"\frac{x}{2}", r"\,(3-x^2)", font_size=42)
        fac.move_to([PANEL_X, 2.2, 0])
        self.say("现在回答第 (e) 问。先把 p 分解：p(x) 等于 x 乘以 3 减 x 的平方，再除以 2。", Write(fac))

        tick = Line(ax.c2p(S3, -0.08), ax.c2p(S3, 0.08), color=C_ZERO, stroke_width=4)
        lab = mt(r"\sqrt3", 30, C_ZERO).move_to(ax.c2p(S3 - 0.3, 0.25))
        seg = ax.plot(p, x_range=[0, S3], color=C_PLUS, stroke_width=7)
        pos = mt(r"0<x<\sqrt3\ \Rightarrow\ p(x)>0", 36).next_to(fac, DOWN, buff=0.45)
        self.say("当 0 < x < √3 时，两个因子都是正的，所以 p(x) 也是正的：不会翻号。",
                 Create(tick), FadeIn(lab), Create(seg), FadeIn(pos))
        top = DashedLine(ax.c2p(0, 1), ax.c2p(S3, 1), color=GREY_B, dash_length=0.08)
        mx = mt(r"\max_{0<x<\sqrt3}p(x)=p(1)=1", 36).next_to(pos, DOWN, buff=0.4)
        self.say("而且这一段上 p 最高只到 1，在 x = 1 处取到。所以一步之后，x 就落在 0 和 1 之间。",
                 Create(top), FadeIn(mx), Indicate(self.fps[2], color=C_PLUS))
        up = mt(r"0<x<1:\ \ p(x)-x=\frac{x}{2}(1-x^2)>0", 36).next_to(mx, DOWN, buff=0.4)
        self.say("在 0 和 1 之间，p(x) − x = x(1 − x 的平方)/2 大于 0：每步都往上走，又越不过 1，只能收敛到 1。",
                 FadeIn(up))
        self.hold()
        o = orbit(1.6, 1)
        w = self.web(1.6, 8, C_PLUS)
        m = self.start_mark(1.6, C_PLUS)
        self.say(f"比如从 1.6 出发：先掉到 {o[1]:.2f}，再一级级爬回 1。0 < σ < √3 全都去 +1。",
                 FadeIn(m), self.draw(w, 0.3))
        self.hold()
        arrow = CurvedArrow(ax.c2p(S3, 0) + UP * 0.12, ax.c2p(0, 0) + UP * 0.12, angle=PI / 3,
                            color=C_ZERO, stroke_width=4)
        s3 = mt(r"p(\sqrt3)=\frac{\sqrt3}{2}(3-3)=0", 36, C_ZERO).next_to(up, DOWN, buff=0.4)
        self.say("恰好 σ = √3 时，p(√3) = 0：一步掉进 0，然后永远停在这个不稳定的不动点上。",
                 FadeOut(VGroup(w, m)), Create(arrow), FadeIn(s3), Flash(self.fps[1], color=C_ZERO))
        self.hold()
        self.play(FadeOut(VGroup(pos, mx, up, s3, arrow, top, seg)))
        self.s3_mark = VGroup(tick, lab)
        self.fac = fac

    # ------------------------------------------------------------ 6. √3 and √5
    def two_thresholds(self):
        ax = self.ax
        xc = _root(-2.5, 1.0, 2.5)
        flip_r = ax.plot(p, x_range=[S3, xc], color=C_MINUS, stroke_width=7)
        flip_l = ax.plot(p, x_range=[-xc, -S3], color=C_PLUS, stroke_width=7)
        sg = mt(r"|x|>\sqrt3\ \Rightarrow\ \operatorname{sign}p(x)=-\operatorname{sign}x", 36)
        sg.next_to(self.fac, DOWN, buff=0.45)
        self.say("越过 √3，因子 3 − x 的平方变成负的：p(x) 和 x 异号。每迭代一次，符号就翻一次。",
                 Create(flip_r), Create(flip_l), FadeIn(sg))
        self.hold()
        ratio = mt(r"\frac{|p(x)|}{|x|}=\frac{|3-x^2|}{2}", 38).next_to(sg, DOWN, buff=0.4)
        self.say("那大小呢？比较 |p(x)| 和 |x|：两者的比值是 |3 − x 的平方| 除以 2。", FadeIn(ratio))
        chain = mt(r"\frac{x^2-3}{2}<1\iff x^2<5\iff |x|<\sqrt5", 36).next_to(ratio, DOWN, buff=0.4)
        self.say("在 |x| > √3 时，这个比值小于 1，当且仅当 x 的平方小于 5，也就是 |x| < √5。",
                 FadeIn(chain))
        self.hold()

        # the |x| axis split into three zones
        nl = NumberLine(x_range=[0, 3.0, 0.5], length=5.6, color=GREY_B, stroke_width=2,
                        include_tip=False, tick_size=0.04).move_to([PANEL_X - 0.25, -1.5, 0])
        zones = VGroup()
        for (a, b, c, s) in ((0, S3, BLUE_D, "同号"), (S3, S5, C_ZERO, "翻号\n变小"), (S5, 3.0, C_S5, "翻号\n变大")):
            r = Rectangle(width=nl.n2p(b)[0] - nl.n2p(a)[0], height=0.34, stroke_width=0,
                          fill_color=c, fill_opacity=0.45)
            r.move_to((nl.n2p(a) + nl.n2p(b)) / 2)
            zones.add(VGroup(r, txt(s, 20, c, line_spacing=0.8).next_to(r, DOWN, buff=0.12)))
        ticks = VGroup(
            mt(r"0", 24, GREY_B).next_to(nl.n2p(0), UP, buff=0.28),
            mt(r"\sqrt3", 24, C_ZERO).next_to(nl.n2p(S3), UP, buff=0.28),
            mt(r"\sqrt5", 24, C_S5).next_to(nl.n2p(S5), UP, buff=0.28),
            mt(r"|x|", 26, GREY_B).next_to(nl, RIGHT, buff=0.15),
        )
        s5 = Line(ax.c2p(S5, -0.08), ax.c2p(S5, 0.08), color=C_S5, stroke_width=4)
        s5l = mt(r"\sqrt5", 30, C_S5).next_to(s5, UP, buff=0.1)
        self.play(FadeOut(VGroup(sg, ratio)), chain.animate.next_to(self.fac, DOWN, buff=0.45))
        self.say("于是有了第二个关键数 √5。√3 管会不会翻号，√5 管翻号的同时是变小还是变大。",
                 Create(nl), FadeIn(zones), FadeIn(ticks), Create(s5), FadeIn(s5l))
        self.hold(0.5)
        self.zone_bar = VGroup(nl, zones, ticks)
        self.play(FadeOut(VGroup(flip_r, flip_l, chain)))
        self.s5_mark = VGroup(s5, s5l)

    # ------------------------------------------------------------ 7. the edge at √5
    def edge_sqrt5(self):
        ax = self.ax
        pts = [ax.c2p(S5, 0)]
        x = S5
        for _ in range(4):
            y = p(x)
            pts += [ax.c2p(x, y), ax.c2p(y, y)]
            x = y
        sq = VGroup(*[Line(a, b, color=C_S5, stroke_width=3.5) for a, b in zip(pts, pts[1:])])
        eq = VGroup(mt(r"p(\sqrt5)=\frac{\sqrt5}{2}(3-5)=-\sqrt5", 36, C_S5),
                    mt(r"p(-\sqrt5)=\sqrt5", 36, C_S5)).arrange(DOWN, buff=0.3)
        eq.next_to(self.fac, DOWN, buff=0.45)
        self.say("先看边缘。p(√5) = −√5，p(−√5) = √5：蛛网变成一个正方形，永远绕下去。",
                 FadeIn(eq), self.draw(sq[:5], 0.5))
        self.play(self.draw(sq[5:], 0.35))
        per = txt("周期为 2 的轨道", 26, C_S5).next_to(eq, DOWN, buff=0.35)
        self.say("所以 σ = √5 既不收敛也不发散：它在 ±√5 之间来回，是周期为 2 的轨道，不是不动点。",
                 FadeIn(per))
        self.hold()
        o = orbit(2.3, 3)
        seq = mt(r"\to ".join(num(v, 2 if abs(v) < 10 else 1) for v in o) + r"\to\cdots", 34, C_S5)
        seq.next_to(per, DOWN, buff=0.45)
        self.play(FadeOut(self.zone_bar))
        self.say(f"再大一点，比如 2.3：每步翻号，还越来越大：{neg(num(o[1]))}、{num(o[2])}、{neg(num(o[3], 1))}……发散。",
                 FadeIn(seq))
        self.hold(0.5)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 8. between √3 and √5
    def flip_zone(self):
        quote = txt("讨论课解答：σ > √3 时，“要么收敛到 −1，要么发散”", 28, GREY_A).to_edge(UP, buff=0.9)
        self.say("剩下的就是 √3 和 √5 之间。讨论课的解答说：这里要么收敛到 −1，要么发散。",
                 FadeIn(quote))
        cross = Line(quote.get_left(), quote.get_right(), color=C_S5, stroke_width=3)
        self.say("可开头的 2.2 明明去了 +1。这一段里到底发生了什么？", Create(cross))
        self.hold()

        starts = [2.0, 2.2, 2.23]
        rows, dots, names, counters = VGroup(), VGroup(), VGroup(), VGroup()
        L = NumberLine(x_range=[0, 2.4, 0.5], length=9.0, include_tip=False)
        for i, x0 in enumerate(starts):
            nl = NumberLine(x_range=[0, 2.4, 0.5], length=9.0, color=GREY_B, stroke_width=2,
                            include_tip=False, tick_size=0.04).move_to([-0.2, 1.3 - 1.4 * i, 0])
            rows.add(nl)
            names.add(mt(r"x_0=" + num(x0), 30).next_to(nl, LEFT, buff=0.3))
            dots.add(Dot(nl.n2p(x0), radius=0.1, color=sign_color(x0)))
            counters.add(txt("翻号 0 次", 24, GREY_A).next_to(nl, RIGHT, buff=0.35))
        L.move_to([-0.2, 0, 0])
        top, bot = 2.05, -1.55
        band = Rectangle(width=L.n2p(S5)[0] - L.n2p(S3)[0], height=top - bot, stroke_width=0,
                         fill_color=C_ZERO, fill_opacity=0.14)
        band.move_to([(L.n2p(S3)[0] + L.n2p(S5)[0]) / 2, (top + bot) / 2, 0])
        guides = VGroup()
        for v, c, s in ((1, C_PLUS, r"1"), (S3, C_ZERO, r"\sqrt3"), (S5, C_S5, r"\sqrt5")):
            xx = L.n2p(v)[0]
            guides.add(DashedLine([xx, bot, 0], [xx, top, 0], color=c, stroke_width=2, dash_length=0.08))
            guides.add(mt(s, 28, c).move_to([xx, top + 0.25, 0]))
        zero = mt(r"|x|=0", 24, GREY_B).next_to(rows[-1].n2p(0), DOWN, buff=0.2)
        legend = VGroup(
            VGroup(Dot(radius=0.08, color=C_PLUS), txt("正", 22, C_PLUS)).arrange(RIGHT, buff=0.12),
            VGroup(Dot(radius=0.08, color=C_MINUS), txt("负", 22, C_MINUS)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.4).next_to(rows[-1], DOWN, buff=0.3).align_to(rows[-1], RIGHT)
        self.play(FadeOut(VGroup(quote, cross)))
        self.say("这一段里每步都翻号，同时绝对值变小。我们只画绝对值，用颜色记正负，再数翻号的次数。",
                 FadeIn(band), FadeIn(guides), FadeIn(rows), FadeIn(names), FadeIn(zero),
                 FadeIn(legend), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.2),
                 FadeIn(counters))

        orbs = [orbit(x0, 5) for x0 in starts]
        flips = [0, 0, 0]

        def step(k):
            anims = []
            for i in range(3):
                a, b = orbs[i][k - 1], orbs[i][k]
                if a * b < 0:
                    flips[i] += 1
                    new = txt(f"翻号 {flips[i]} 次", 24, sign_color(b)).move_to(counters[i], aligned_edge=LEFT)
                    anims.append(Transform(counters[i], new))
                anims.append(dots[i].animate.move_to(rows[i].n2p(abs(b))).set_color(sign_color(b)))
            return anims

        self.say("一步一步看：绝对值不断往左走，颜色正负交替。", *step(1), run_time=1.2)
        for k in range(2, 6):
            self.play(*step(k), run_time=1.0)
        assert flips == [1, 2, 3], flips
        self.say("2.00 翻一次号就跌到了 √3 以下；2.20 翻了两次，2.23 翻了三次。",
                 LaggedStart(*[Indicate(c) for c in counters], lag_ratio=0.3))
        self.hold()
        self.say("绝对值一直变小，却不可能永远停在 √3 右边：能让它停住的只有 √5。所以它迟早跌进 √3 以内。",
                 Indicate(band, color=C_ZERO, scale_factor=1.02))
        self.say("一旦跌进去，就不再翻号，被同号的 ±1 吸走。")
        fates = VGroup()
        for i, x0 in enumerate(starts):
            lim = fate(x0)[0]
            fates.add(mt(("+" if lim > 0 else "") + str(int(lim)), 34, sign_color(lim))
                      .next_to(counters[i], RIGHT, buff=0.3))
        rule = VGroup(txt("奇数次 → −1", 30, C_MINUS), txt("偶数次 → +1", 30, C_PLUS))
        rule.arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.9)
        self.say("从正数出发：翻了奇数次，最后是 −1；翻了偶数次，最后是 +1。",
                 FadeIn(fates), FadeIn(rule))
        self.hold(0.5)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 9. the first boundary b1
    def first_boundary(self):
        g = self.make_graph()
        ax = self.ax
        s3 = VGroup(Line(ax.c2p(S3, -0.08), ax.c2p(S3, 0.08), color=C_ZERO, stroke_width=4),
                    mt(r"\sqrt3", 28, C_ZERO).move_to(ax.c2p(S3 - 0.3, 0.25)))
        self.play(FadeIn(g), FadeIn(s3))
        b1 = B[1]
        h = DashedLine(ax.c2p(-0.3, -S3), ax.c2p(2.4, -S3), color=C_ZERO, dash_length=0.08)
        hl = mt(r"y=-\sqrt3", 28, C_ZERO).next_to(ax.c2p(-0.3, -S3), LEFT, buff=0.1)
        dot = Dot(ax.c2p(b1, -S3), radius=0.08, color=C_ZERO)
        drop = DashedLine(ax.c2p(b1, -S3), ax.c2p(b1, 0), color=C_ZERO, dash_length=0.06)
        bl = mt(r"b_1", 28, C_ZERO).next_to(ax.c2p(b1, 0), UP, buff=0.2)
        defn = mt(r"p(b_1)=-\sqrt3", 38, C_ZERO).move_to([PANEL_X, 2.2, 0])
        val = mt(r"b_1\approx" + num(b1, 4), 36, C_ZERO).next_to(defn, DOWN, buff=0.3)
        self.say("翻一次和翻两次的分界在哪？就在 p(x) 恰好等于 −√3 的地方。把这个点叫作 b1。",
                 Create(h), FadeIn(hl), GrowFromCenter(dot), Create(drop), FadeIn(bl), FadeIn(defn),
                 FadeIn(val))
        self.hold()
        xin = Line(ax.c2p(S3, 0), ax.c2p(b1, 0), color=C_MINUS, stroke_width=9)
        yin = Line(ax.c2p(0, 0), ax.c2p(0, -S3), color=C_MINUS, stroke_width=9)
        piece = ax.plot(p, x_range=[S3, b1], color=C_MINUS, stroke_width=7)
        mapto = mt(r"p\big((\sqrt3,\,b_1)\big)=(-\sqrt3,\,0)", 36, C_MINUS).next_to(val, DOWN, buff=0.45)
        self.say("p 在这里单调递减，所以 √3 和 b1 之间的点，一步落到 −√3 和 0 之间：只翻一次号，然后去 −1。",
                 Create(xin), Create(piece), FadeIn(mapto))
        self.play(TransformFromCopy(xin, yin), run_time=1.2)
        self.hold()
        two = Dot(ax.c2p(2, -1), radius=0.08, color=C_MINUS)
        twol = mt(r"p(2)=-1", 36, C_MINUS).next_to(mapto, DOWN, buff=0.4)
        self.say("2 就在这一段：p(2) 正好等于 −1，一步到位。", GrowFromCenter(two), FadeIn(twol),
                 Flash(two, color=C_MINUS))
        self.hold(0.5)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 10. the alternating basins
    def basin_bar(self, lo, colored=True, n=12):
        X0, W, Y = -4.7, 11.3, 0.45
        span = S5 - lo

        def X(v):
            return X0 + (v - lo) / span * W

        bar = VGroup()
        rects, ticks, labels, fates = VGroup(), VGroup(), VGroup(), VGroup()
        for k in range(1, n + 1):
            a, b = max(B[k - 1], lo), max(B[k], lo)
            w = max(X(b) - X(a), 1e-4)
            c = (C_MINUS if k % 2 else C_PLUS) if colored else GREY_D
            r = Rectangle(width=w, height=0.62, stroke_width=0, fill_color=c, fill_opacity=0.75)
            r.move_to([(X(a) + X(b)) / 2, Y, 0])
            rects.add(r)
            f = mt("-1" if k % 2 else "+1", 30, BLACK).move_to(r)
            f.set_opacity(1 if (colored and w > 0.75) else 0)
            fates.add(f)
        for k in range(1, n + 1):
            x = X(B[k])
            gap = X(B[k + 1]) - x if k + 1 < len(B) else 0
            t = Line([x, Y - 0.36, 0], [x, Y + 0.36, 0], color=WHITE, stroke_width=2)
            t.set_opacity(1 if B[k] >= lo else 0)
            ticks.add(t)
            lab = mt(f"b_{{{k}}}", 28).next_to(t, DOWN, buff=0.12)
            lab.set_opacity(1 if (B[k] >= lo - 1e-12 and gap > 0.42) else 0)
            labels.add(lab)
        edge = Line([X(S5), Y - 0.5, 0], [X(S5), Y + 0.5, 0], color=C_S5, stroke_width=4)
        edge_l = mt(r"\sqrt5", 30, C_S5).next_to(edge, DOWN, buff=0.12)
        bar.add(rects, fates, ticks, labels, edge, edge_l)
        bar.rects, bar.fates, bar.X = rects, fates, X
        return bar

    def basins(self):
        defn = mt(r"b_0=\sqrt3,\qquad p(b_n)=-b_{n-1}\ \iff\ b_n^3-3b_n=2b_{n-1}", 36)
        defn.to_edge(UP, buff=0.4).to_edge(LEFT, buff=0.5)
        self.say("依此类推，让 p(b2) = −b1，p(b3) = −b2，一直下去：每个 b 都由上一个唯一确定。", Write(defn))
        vals = mt(r",\ ".join(f"b_{{{k}}}\\approx{B[k]:.4f}" for k in (1, 2, 3)) + r",\ \ldots\ \nearrow\sqrt5", 34)
        vals.move_to([0, -0.9, 0])
        self.say(f"算出来：b1 ≈ {B[1]:.4f}，b2 ≈ {B[2]:.4f}，b3 ≈ {B[3]:.4f}……它们越来越靠近 √5。",
                 FadeIn(vals))

        bar = self.basin_bar(S3, colored=False)
        X = bar.X
        s3l = mt(r"\sqrt3", 30, C_ZERO).next_to([X(S3), 0.45 - 0.31, 0], DOWN, buff=0.18)
        core = Rectangle(width=1.55, height=0.62, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9)
        core.move_to([-5.85, 0.45, 0])
        core_l = mt(r"|x|<\sqrt3", 26).move_to(core)
        self.say("把 √3 到 √5 这一段按这些点切开，只看绝对值。关键在于：p 把每一段翻到上一段的镜像上。",
                 FadeIn(bar), FadeIn(s3l), FadeIn(core), FadeIn(core_l))
        centers = [X((B[k - 1] + B[k]) / 2) for k in (1, 2, 3)]
        arrows = VGroup()
        for k in (3, 2, 1):
            a = [centers[k - 1], 0.8, 0]
            b = [centers[k - 2] if k > 1 else -5.85, 0.8, 0]
            arrows.add(CurvedArrow(a, b, angle=PI / 2.4 if k > 1 else PI / 3, color=GREY_A,
                                   stroke_width=3, tip_length=0.18))
        arrows.submobjects.reverse()   # arrows[0]: I1 -> core, arrows[1]: I2 -> I1, arrows[2]: I3 -> I2
        plab = mt(r"p", 30, GREY_A).next_to(arrows[0], UP, buff=0.05)
        maps = mt(r"p\big((b_{n-1},\,b_n)\big)=(-b_{n-1},\,-b_{n-2})", 34).move_to([0, -1.75, 0])
        self.play(Create(arrows[2]), Create(arrows[1]), Create(arrows[0]), FadeIn(plab), FadeIn(maps),
                  run_time=1.6)
        self.hold()

        colors = [C_MINUS, C_PLUS, C_MINUS]
        self.say("第一段一步落进 √3 以内的负半边，去 −1。",
                 bar.rects[0].animate.set_fill(colors[0], 0.75), Indicate(arrows[0], color=C_MINUS))
        f1 = mt("-1", 30, BLACK).move_to(bar.rects[0])
        self.play(FadeIn(f1))
        self.say("p 是奇函数，镜像的命运正好相反：第二段翻一次号，就变成了第一段的镜像，所以去 +1。",
                 bar.rects[1].animate.set_fill(colors[1], 0.75), Indicate(arrows[1], color=C_PLUS))
        f2 = mt("+1", 30, BLACK).move_to(bar.rects[1])
        self.play(FadeIn(f2))
        self.say("第三段变成第二段的镜像，又去 −1。就这样一段一段交替下去。",
                 bar.rects[2].animate.set_fill(colors[2], 0.75), Indicate(arrows[2], color=C_MINUS),
                 *[bar.rects[k].animate.set_fill(C_MINUS if k % 2 == 0 else C_PLUS, 0.75)
                   for k in range(3, 12)])
        rule = MathTex(r"b_{n-1}<\sigma<b_n", r"\ \Longrightarrow\ ", r"x_k\to(-1)^n", font_size=38)
        rule[2].set_color(YELLOW_D)
        rule.move_to([0, -1.75, 0])
        self.say("结论：第 n 段里的点恰好翻 n 次号。n 为奇数去 −1，n 为偶数去 +1。",
                 FadeOut(maps), FadeIn(rule))
        self.hold()

        # zoom towards √5: the picture repeats
        live = self.basin_bar(S3)
        self.remove(bar, f1, f2)
        self.add(live)
        t = ValueTracker(0.0)
        zoomed = always_redraw(lambda: self.basin_bar(S5 - (S5 - S3) * 6 ** (-t.get_value())))
        self.remove(live)
        self.add(zoomed)
        self.say("这些分界点越来越挤向 √5。放大去看，同样的图案一遍又一遍地重复。",
                 FadeOut(VGroup(arrows, plab, core, core_l, s3l, vals)))
        self.play(t.animate.set_value(2.0), run_time=6.0, rate_func=smooth)
        zoomed.clear_updaters()
        self.hold()
        slope = mt(r"p'(\sqrt5)=\tfrac32-\tfrac32\cdot5=-6", 36, C_S5)
        ratios = mt(r"\frac{\sqrt5-b_{n-1}}{\sqrt5-b_n}\ \to\ 6", 36)
        sr = VGroup(slope, ratios).arrange(RIGHT, buff=1.0).move_to([0, -0.85, 0])
        r_now = (S5 - B[5]) / (S5 - B[6])
        assert abs(r_now - 6) < 0.05
        self.say("每一段大约只有上一段的六分之一：p 在 √5 处的斜率是 −6，离 √5 的距离每步放大 6 倍。",
                 FadeIn(sr))
        self.hold()
        self.say("所以在 √3 和 √5 之间，有无穷多个吸引区，交替通向 −1、+1、−1、+1……",
                 Indicate(rule[2]))
        self.hold(0.5)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 11. the boundary points themselves
    def boundary_points(self):
        rows, dots, names, chains = VGroup(), VGroup(), VGroup(), VGroup()
        paths = []
        for i, n in enumerate((1, 2, 3)):
            row = self.number_row(1.7 - 1.55 * i, lo=-2.4, hi=2.4, length=10.0, x=0.6, marks=(0,))
            nl = row[0]
            for v in (S3, -S3):
                row.add(Line(nl.n2p(v) + DOWN * 0.1, nl.n2p(v) + UP * 0.1, color=C_ZERO, stroke_width=4))
                row.add(mt(r"\sqrt3" if v > 0 else r"-\sqrt3", 22, C_ZERO).next_to(nl.n2p(v), DOWN, buff=0.14))
            rows.add(row)
            names.add(mt(f"b_{{{n}}}", 34, C_ZERO).next_to(nl, LEFT, buff=0.35))
            # b_n -> -b_{n-1} -> ... -> ±√3 -> 0, exactly
            path = [(+1, n)]
            s = 1
            for k in range(n - 1, -1, -1):
                s = -s
                path.append((s, k))
            vals = [sg * B[k] for sg, k in path] + [0.0]
            assert all(abs(p(a) - b) < 1e-9 for a, b in zip(vals, vals[1:]))
            paths.append(vals)
            terms = [("-" if sg < 0 else "") + (r"\sqrt3" if k == 0 else f"b_{{{k}}}") for sg, k in path] + ["0"]
            chains.add(mt(r"\to ".join(terms), 30, C_ZERO).next_to(nl, UP, buff=0.18).align_to(nl, RIGHT))
            dots.add(Dot(nl.n2p(vals[0]), radius=0.09, color=C_ZERO))
        self.say("那分界点本身呢？b1 一步到 −√3，再一步到 0。",
                 FadeIn(rows[0]), FadeIn(names[0]), GrowFromCenter(dots[0]))
        nl = rows[0][0]
        for a, b in zip(paths[0], paths[0][1:]):
            self.play(self.hop(dots[0], nl, a, b, C_ZERO), run_time=0.9)
        self.play(FadeIn(chains[0]))
        self.say("b2 → −b1 → √3 → 0，b3 → −b2 → b1 → −√3 → 0。",
                 FadeIn(rows[1:]), FadeIn(names[1:]), *[GrowFromCenter(d) for d in dots[1:]])
        for j in range(max(len(q) for q in paths[1:]) - 1):
            anims = []
            for i in (1, 2):
                if j + 1 < len(paths[i]):
                    anims.append(self.hop(dots[i], rows[i][0], paths[i][j], paths[i][j + 1], C_ZERO))
            self.play(*anims, run_time=0.9)
        self.play(FadeIn(chains[1:]))
        self.say("每个分界点经过有限步都精确撞上 ±√3，然后落在不稳定的不动点 0 上：既不去 +1，也不去 −1。",
                 LaggedStart(*[Flash(d, color=C_ZERO) for d in dots], lag_ratio=0.2))
        self.hold()
        self.say("不过它们都是孤立的点：稍微推一下，就会掉进两边的某个吸引区。")
        self.hold(0.5)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 12. the answer to (e)
    def summary(self):
        head = [txt("初值 σ", 26, GREY_B), txt("过程", 26, GREY_B), txt("结局", 26, GREY_B)]
        rows = [
            (mt(r"0<\sigma<\sqrt3", 34), txt("不翻号，爬向 1", 26), mt(r"+1", 34, C_PLUS)),
            (mt(r"\sigma=\sqrt3", 34), txt("一步到 0", 26), mt(r"0", 34, C_ZERO)),
            (mt(r"b_{n-1}<\sigma<b_n", 34), txt("翻号 n 次，同时变小", 26), mt(r"(-1)^n", 34, YELLOW_D)),
            (mt(r"\sigma=b_n", 34), txt("有限步撞上 ±√3", 26), mt(r"0", 34, C_ZERO)),
            (mt(r"\sigma=\sqrt5", 34), txt("在 ±√5 之间来回", 26), txt("周期为 2", 26, C_S5)),
            (mt(r"\sigma>\sqrt5", 34), txt("翻号，同时变大", 26), txt("发散", 26, C_S5)),
        ]
        xs = (-3.9, 0.7, 4.6)
        table = VGroup()
        for r, cells in enumerate([head] + rows):
            y = 2.55 - 0.72 * r
            line = VGroup(*[c.move_to([x, y, 0]) for c, x in zip(cells, xs)])
            table.add(line)
        rule = Line([-6.2, 2.2, 0], [6.2, 2.2, 0], color=GREY_C, stroke_width=1.5)
        self.say("把第 (e) 问的答案整理一下。", FadeIn(table[0]), Create(rule))
        self.say("0 到 √3 之间去 +1；√3 本身一步到 0。",
                 FadeIn(table[1], shift=UP * 0.1), FadeIn(table[2], shift=UP * 0.1))
        self.say("√3 到 √5 之间按翻号次数交替去 −1、+1；分界点 bn 落到 0。",
                 FadeIn(table[3], shift=UP * 0.1), FadeIn(table[4], shift=UP * 0.1))
        self.say("√5 在 ±√5 之间来回；再大就一边翻号一边发散。",
                 FadeIn(table[5], shift=UP * 0.1), FadeIn(table[6], shift=UP * 0.1))
        self.hold(0.8)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 13. back to the matrix
    def back_to_matrix(self):
        sig0 = [2.9, 1.6, 0.9, 0.35]
        nl = NumberLine(x_range=[0, 3.2, 0.5], length=11.0, color=GREY_B, stroke_width=2,
                        include_tip=False, tick_size=0.04).move_to([0.3, -0.2, 0])
        marks = VGroup()
        for v, c, s in ((0, GREY_B, "0"), (1, C_PLUS, "1"), (S3, C_ZERO, r"\sqrt3"), (S5, C_S5, r"\sqrt5")):
            marks.add(Line(nl.n2p(v) + DOWN * 0.12, nl.n2p(v) + UP * 0.12, color=c, stroke_width=4))
            marks.add(mt(s, 28, c).next_to(nl.n2p(v), DOWN, buff=0.2))
        lab = mt(r"\sigma_i", 32, C_SIG).next_to(nl, LEFT, buff=0.3)
        dots = VGroup(*[Dot(nl.n2p(s), radius=0.1, color=C_SIG) for s in sig0])
        self.say("回到矩阵。一个奇异值若被推到 −1，矩阵依然正交，只是那个方向被翻转了；但大于 √5 的奇异值会发散。",
                 Create(nl), FadeIn(marks), FadeIn(lab), LaggedStart(*[GrowFromCenter(d) for d in dots]))
        bad = SurroundingRectangle(dots[0], color=C_S5, buff=0.12)
        blow = mt(r"p(2.9)=" + num(p(2.9)), 32, C_S5).next_to(dots[0], UP, buff=0.35)
        self.play(Create(bad), FadeIn(blow))
        self.hold()

        fro = math.sqrt(sum(s * s for s in sig0))
        sig1 = [s / fro for s in sig0]
        assert max(sig1) < 1 < S3
        norm = MathTex(r"W\ \leftarrow\ \frac{W}{\|W\|_F}", r",\qquad", r"\sigma_{\max}\le\|W\|_F=\sqrt{\textstyle\sum_i\sigma_i^2}",
                       font_size=38).to_edge(UP, buff=0.8)
        self.say("所以迭代之前要先把 W 缩小。常见做法是除以 Frobenius 范数：它不小于最大的奇异值。",
                 FadeOut(VGroup(bad, blow)), Write(norm))
        self.say("缩放之后，所有奇异值都落进 0 和 1 之间，远离 √3。",
                 *[d.animate.move_to(nl.n2p(s)) for d, s in zip(dots, sig1)], run_time=1.6)
        steps = 8
        orbs = [orbit(s, steps) for s in sig1]
        assert all(abs(o[-1] - 1) < 0.01 for o in orbs)
        k_lab = mt(r"k=0", 34).next_to(nl, UP, buff=1.1).align_to(nl, LEFT)
        self.say("接下来每个奇异值都走上通往 +1 的路；小的要多走几步，但最终都到 1，W 趋向 U 乘 V 的转置。",
                 FadeIn(k_lab))
        for k in range(1, steps + 1):
            new_k = mt(f"k={k}", 34).move_to(k_lab, aligned_edge=LEFT)
            self.play(*[d.animate.move_to(nl.n2p(o[k])).set_color(C_PLUS if abs(o[k] - 1) < 0.02 else C_SIG)
                        for d, o in zip(dots, orbs)], Transform(k_lab, new_k), run_time=0.55)
        res = mt(r"W_k\ \to\ UV^{\top}", 40, C_PLUS).next_to(nl, UP, buff=1.1).align_to(nl, RIGHT)
        self.play(FadeIn(res))
        self.say("一个矩阵问题，就这样变成了一维动力系统：不动点、稳定性、两个关键数，和它们之间无穷交替的吸引区。")
        self.hold(0.8)
