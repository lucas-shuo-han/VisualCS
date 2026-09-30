"""Episode 7 — Damping and Stability of Momentum (Note 4, section 4.1: the scalar mode, Schur test, regimes, Nesterov)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

B = 0.5                                   # momentum coefficient used in the pictures
SB = np.sqrt(B)
S_LO, S_HI, S_EDGE = (1 - SB) ** 2, (1 + SB) ** 2, 2 * (1 + B)
assert abs(S_LO - 0.0858) < 1e-4 and abs(S_HI - 2.9142) < 1e-4 and S_EDGE == 3.0


def roots(s, b=B):
    """Roots of q^2 - a q + b with a = 1 + b - s, s = eta (1 - beta) lambda."""
    return np.roots([1.0, -(1 + b - s), b])


def rate(s, b=B):
    return float(np.abs(roots(s, b)).max())


# (a) the 2x2 recurrence and the scalar recurrence agree
LAM1, ETA1 = 2.0, 0.3
_s = ETA1 * (1 - B) * LAM1
A = np.array([[1 - ETA1 * (1 - B) * LAM1, -ETA1 * B], [(1 - B) * LAM1, B]])
assert np.allclose(sorted(np.linalg.eigvals(A).real), sorted(roots(_s).real))
_w, _z = 1.0, 0.0
_ws = [1.0]
for _ in range(20):
    _z = B * _z + (1 - B) * LAM1 * _w
    _w = _w - ETA1 * _z
    _ws.append(_w)
for _t in range(1, 19):                                  # w_{t+1} = a w_t - beta w_{t-1}
    assert abs(_ws[_t + 1] - ((1 + B - _s) * _ws[_t] - B * _ws[_t - 1])) < 1e-12

# (b) Schur test: stable exactly for 0 < s < 2 (1 + beta)
for _s in (0.001, 0.05, 1.0, 2.9, 2.999):
    assert rate(_s) < 1
for _s in (3.0001, 3.2, 5.0):
    assert rate(_s) > 1
assert abs(rate(3.0) - 1.0) < 1e-9
assert abs(rate(S_LO) - SB) < 1e-3
WIDEN = (1 + 0.9) / (1 - 0.9)
assert abs(WIDEN - 19) < 1e-9

# (c) the plateau: rate equals sqrt(beta) for s in [(1-sqrt b)^2, (1+sqrt b)^2]
for _s in np.linspace(S_LO, S_HI, 25):
    assert abs(rate(_s) - SB) < 2e-3
assert rate(0.5 * S_LO) > SB and rate(S_HI + 0.03) > SB + 0.02
SS = np.linspace(0.0, 3.15, 300)
RATES = np.array([rate(s) for s in SS])

# (d) three regimes on a time axis
S_OVER, S_CRIT, S_UNDER = 0.04, S_LO, 1.0


def regime(s, b=B):
    d = (1 + b - s) ** 2 - 4 * b
    return "over" if d > 1e-9 else "under" if d < -1e-9 else "crit"


assert regime(S_OVER) == "over" and regime(S_UNDER) == "under" and regime(S_CRIT + 0.02) == "under" and regime(S_CRIT - 0.01) == "over"
assert regime(S_CRIT, B) in ("crit", "over", "under")
assert np.isreal(roots(S_OVER)).all() and (roots(S_OVER) > 0).all()
assert (roots(2.95) < 0).all() and np.isreal(roots(2.95)).all()          # real NEGATIVE roots just below the edge
assert abs(np.abs(roots(S_UNDER)) - SB).max() < 1e-9


def traj(s, T=30, b=B):
    """w_t for f = w^2/2 with lambda = 1, eta = s/(1-b), w_0 = 1, z_0 = 0."""
    eta = s / (1 - b)
    w, z, out = 1.0, 0.0, [1.0]
    for _ in range(T):
        z = b * z + (1 - b) * w
        w = w - eta * z
        out.append(w)
    return np.array(out)


T_OVER, T_CRIT, T_UNDER = traj(S_OVER), traj(S_CRIT), traj(S_UNDER)
assert (T_OVER > 0).all() and (T_CRIT > 0).all()                # no sign change without oscillation
assert (T_UNDER < 0).any()                                       # overshoots
assert abs(T_OVER[-1]) > 10 * abs(T_CRIT[-1]) and abs(T_CRIT[-1]) < 0.02

# (e) minimax over the spectrum
LMIN, LMAX = 1.0, 20.0
KAPPA = LMAX / LMIN
R_GD = (KAPPA - 1) / (KAPPA + 1)
R_STAR = (np.sqrt(KAPPA) - 1) / (np.sqrt(KAPPA) + 1)
B_STAR = R_STAR ** 2
assert abs(R_GD - 0.9048) < 1e-4 and abs(R_STAR - 0.6345) < 1e-4 and abs(B_STAR - 0.4026) < 1e-3
# brute-force search over (eta, beta) confirms the closed form
_best = (9.0, 0, 0)
for _b in np.linspace(0.05, 0.9, 86):
    for _e in np.linspace(0.05, 3.0, 120):
        _r = max(rate(_e * (1 - _b) * l, _b) for l in (LMIN, LMAX))
        if _r < _best[0]:
            _best = (_r, _b, _e)
assert R_STAR - 0.003 < _best[0] < R_STAR + 0.02, _best
# the plateau covers the whole spectrum iff kappa <= ((1+r)/(1-r))^2 with r = sqrt(beta)
assert abs(((1 + np.sqrt(B_STAR)) / (1 - np.sqrt(B_STAR))) ** 2 - KAPPA) < 1e-9
ETA_STAR = (1 - np.sqrt(B_STAR)) ** 2 / ((1 - B_STAR) * LMIN)
assert abs(rate(ETA_STAR * (1 - B_STAR) * LMIN, B_STAR) - R_STAR) < 5e-3
assert abs(rate(ETA_STAR * (1 - B_STAR) * LMAX, B_STAR) - R_STAR) < 5e-3
STEPS = lambda r: float(np.log(0.01) / np.log(r))
N_GD_K, N_M_K = STEPS(R_GD), STEPS(R_STAR)
assert round(N_GD_K) == 46 and round(N_M_K) == 10
K100 = 100.0
assert round(STEPS((K100 - 1) / (K100 + 1))) == 230 and round(STEPS((np.sqrt(K100) - 1) / (np.sqrt(K100) + 1))) == 23

# (f) Nesterov agrees with a direct implementation on a quadratic (loop check of the stated recurrence)
ALPHA_N = 1 / LMAX
BN = 0.8
_w = np.array([-4.0, 1.0])
_v = np.zeros(2)
lam = np.array([1.0, 20.0])
for _ in range(60):
    _v = BN * _v + lam * (_w - ALPHA_N * BN * _v)
    _w = _w - ALPHA_N * _v
assert np.linalg.norm(_w) < 0.05


class Ep07Damping(NarratedScene):
    series = SERIES

    def construct(self):
        self.title_card()
        self.recurrence()
        self.stability()
        self.regimes()
        self.tuning()
        self.nesterov()
        self.end_card(
            ["On one curvature mode, momentum is a two-state linear system with a single number s, eta times one minus beta times lambda",
             "It is stable exactly when s lies between zero and two times one plus beta, a range wider by one plus beta over one minus beta",
             "Inside the underdamped band every root has the same size, square root of beta, so slow modes and fast modes converge together",
             "One learning rate must serve every eigenvalue: tuning is a minimax problem, and a tuned method pays square root of kappa",
             "Nesterov momentum measures the gradient at the look-ahead point"],
        )

    # ---------------------------------------------------------------- 1. recurrence
    def recurrence(self):
        head = self.heading("One mode of a quadratic")
        loss = mts([r"f(w)=\tfrac12\lambda w^2", r",\qquad \nabla f=\lambda w"], 0.8, {}).move_to([0, 2.5, 0])
        mat = mts([r"\begin{bmatrix}w_{t+1}\\ z_{t+1}\end{bmatrix}=", r"\begin{bmatrix}1-\eta(1-\beta)\lambda&-\eta\beta\\(1-\beta)\lambda&\beta\end{bmatrix}",
                   r"\begin{bmatrix}w_t\\ z_t\end{bmatrix}"], 0.8, {1: C_MOM}).move_to([0, 0.9, 0])
        sec = mts([r"w_{t+1}=a\,w_t-\beta\,w_{t-1}", r",\qquad a=1+\beta-s", r",\quad s=\eta(1-\beta)\lambda"], 0.8, {1: C_LOSS, 2: C_ETA}).move_to([0, -0.6, 0])
        poly = mts([r"p(q)=q^2-a\,q+\beta", r",\qquad q_\pm=\frac{a\pm\sqrt{a^2-4\beta}}{2}"], 0.8, {}).move_to([0, -1.9, 0])
        assert_on_screen(loss, mat, sec, poly)
        self.say("In the Hessian's eigenbasis a quadratic decouples, so study one scalar mode with curvature lambda.",
                 Write(head), Write(loss))
        self.say("Plugging in its gradient couples the weight and the average into a two-by-two linear system.",
                 Write(mat))
        self.say("Eliminating the average gives a second-order recurrence with one number: s, eta times one minus beta times lambda.",
                 Write(sec))
        self.say("Its polynomial has two roots. The mode mixes their powers, so both must lie inside the unit circle.",
                 Write(poly))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 2. stability
    def stability(self):
        head = self.heading("Exactly when is it stable?")
        p1 = mts([r"p(1)=s>0"], 0.8, {}).move_to([-3.6, 2.3, 0])
        p2 = mts([r"p(-1)=2(1+\beta)-s>0"], 0.8, {}).move_to([0.6, 2.3, 0])
        p3 = mts([r"|q_+q_-|=|\beta|<1"], 0.8, {}).move_to([4.7, 2.3, 0])
        assert_on_screen(p1, p2, p3)
        self.say("The Schur test needs three checks: no root at plus one, none at minus one, and a root product below one.",
                 Write(head), Write(p1), Write(p2), Write(p3))
        res = mts([r"0<\eta(1-\beta)\lambda<2(1+\beta)"], 1.0, {}).move_to([0, 0.9, 0])
        cmp_ = mts([r"\beta=0:\ \ 0<\eta\lambda<2", r"\qquad\beta=0.9:\ \ 0<\eta\lambda<38"], 0.8, {}).move_to([0, -0.4, 0])
        wide = mts([r"\text{stable range wider by }\frac{1+\beta}{1-\beta}=19\text{ for }\beta=0.9"], 0.8, {}).move_to([0, -1.5, 0])
        assert_on_screen(res, cmp_, wide)
        self.say("So it is stable exactly for s between zero and two times one plus beta. At beta zero, eta lambda is below two.",
                 Write(res), Write(cmp_))
        self.say("With beta of 0.9, the stable learning-rate range is nineteen times wider. The real gain is speed, not range.",
                 Write(wide))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. regimes
    def regimes(self):
        head = self.heading("Watching the roots move")
        cax = Axes(x_range=[-1.3, 1.3, 1], y_range=[-1.3, 1.3, 1], x_length=3.9, y_length=3.9,
                   axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([-4.3, 0.3, 0])
        unit = Circle(radius=cax.c2p(1, 0)[0] - cax.c2p(0, 0)[0], color=GREY_A, stroke_width=2).move_to(cax.c2p(0, 0))
        inner = DashedVMobject(Circle(radius=(cax.c2p(SB, 0)[0] - cax.c2p(0, 0)[0]), color=C_MOM, stroke_width=2).move_to(cax.c2p(0, 0)), num_dashes=40)
        clab = txt("roots q, unit circle", 20, GREY_B).next_to(cax, UP, buff=0.1)
        ilab = txt("radius √β", 20, C_MOM).next_to(cax.c2p(-SB, 0), DOWN, buff=0.05).shift(LEFT * 0.35 + DOWN * 0.05)
        rax = Axes(x_range=[0, 3.2, 1], y_range=[0, 1.2, 0.5], x_length=6.0, y_length=3.0,
                   axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([2.6, 0.5, 0])
        rx = VGroup(*[txt(f"{v}", 20, GREY_B).next_to(rax.c2p(v, 0), DOWN, buff=0.12) for v in (0, 1, 2, 3)])
        ry = VGroup(*[txt(f"{v:g}", 20, GREY_B).next_to(rax.c2p(0, v), LEFT, buff=0.12) for v in (0, 0.5, 1)])
        rxl = txt("s = η(1−β)λ", 22, C_ETA).next_to(rax.x_axis, DOWN, buff=0.45)
        ryl = txt("slower root size, β = 0.5", 22, GREY_B).next_to(rax, UP, buff=0.1).align_to(rax, LEFT)
        one = DashedLine(rax.c2p(0, 1), rax.c2p(3.2, 1), color=C_LOSS, stroke_width=2)
        rc = clipped(rax, SS, RATES, 0, 1.2, C_MOM, 4)
        tr_ = ValueTracker(0.003)
        dots_ = always_redraw(lambda: VGroup(*[Dot(cax.c2p(r.real, r.imag), radius=0.09, color=C_ITER) for r in roots(tr_.get_value())]))
        mark = always_redraw(lambda: Dot(rax.c2p(tr_.get_value(), min(rate(tr_.get_value()), 1.2)), radius=0.09, color=C_ITER))
        assert_on_screen(VGroup(cax, unit, clab), VGroup(rax, rx, ry, rxl, ryl))
        self.say("Fix beta at one half and slide s up from zero. The larger root's size sets the convergence rate.",
                 Write(head), Create(cax), Create(unit), Create(inner), FadeIn(clab), Create(rax), FadeIn(rx), FadeIn(ry), FadeIn(rxl), FadeIn(ryl), Create(one), Create(rc),
                 FadeIn(dots_), FadeIn(mark))
        b1 = txt("overdamped: two real roots, the slower one limits", 22, C_SOFT).move_to([2.6, -2.1, 0])
        assert_on_screen(b1)
        self.say("Small s: both roots are real and positive, and the slow one sits near one. Smooth, but slow.",
                 tr_.animate(run_time=0.3, rate_func=linear).set_value(S_LO * 0.5), FadeIn(b1))
        b2 = txt("critical: repeated root", 22, GREEN_C).move_to([2.6, -2.1, 0])
        self.say("The roots meet and merge at s equal to one minus root beta, squared: the fastest non-oscillating decay.",
                 tr_.animate(run_time=1.5).set_value(S_LO), FadeOut(b1), FadeIn(b2))
        b3 = txt("underdamped: complex pair, both of size √β", 22, C_MOM).move_to([2.6, -2.1, 0])
        self.say("Beyond that the roots split into a complex pair, both of size root beta. The rate stays flat: a plateau.",
                 tr_.animate(run_time=4, rate_func=linear).set_value(S_HI), FadeOut(b2), FadeIn(b3))
        b4 = txt("negative roots: rings, then leaves the circle at s = 2(1+β)", 22, C_LOSS).move_to([2.6, -2.1, 0])
        self.say("Near the far end both roots turn real and negative. At s equal to three one reaches minus one: unstable.",
                 tr_.animate(run_time=2.5, rate_func=linear).set_value(3.1), FadeOut(b3), FadeIn(b4))
        self.hold(0.4)
        self.clear_stage()
        # time-domain examples
        head = self.heading("The three regimes over time")
        ax = Axes(x_range=[0, 30, 10], y_range=[-0.4, 1.0, 0.5], x_length=8.0, y_length=3.4,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([-1.7, 0.3, 0])
        xt = VGroup(*[txt(f"{v}", 20, GREY_B).next_to(ax.c2p(v, -0.4), DOWN, buff=0.12) for v in (0, 10, 20, 30)])
        yt = VGroup(*[txt(f"{v:g}", 20, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12) for v in (0, 0.5, 1)])
        xl = txt("steps t", 22, GREY_B).next_to(ax.c2p(15, -0.4), DOWN, buff=0.5)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(30, 0), color=GREY_A, stroke_width=2)
        ts = np.arange(31)
        co, cc, cu = polyline(ax, ts, T_OVER, C_SOFT, 4), polyline(ax, ts, T_CRIT, GREEN_C, 4), polyline(ax, ts, T_UNDER, C_MOM, 4)
        lo = txt(f"overdamped, s = {S_OVER}", 22, C_SOFT).move_to([4.6, 1.5, 0])
        lc = txt(f"critical, s = {S_CRIT:.3f}", 22, GREEN_C).move_to([4.6, 0.8, 0])
        lu = txt(f"underdamped, s = {S_UNDER:g}", 22, C_MOM).move_to([4.6, 0.1, 0])
        assert_on_screen(VGroup(ax, xt, yt, xl), lo, lc, lu)
        self.say("Start the mode at one and watch. Overdamped creeps toward zero; critical gets there quickly without crossing.",
                 Write(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), Create(zero), Create(co), FadeIn(lo), Create(cc), FadeIn(lc))
        self.say("Underdamped overshoots and rings, but inside an envelope shrinking like root beta to the t. Still fast.",
                 Create(cu), FadeIn(lu))
        note = txt("Note: with β = 0 the two boundaries coincide and the distinction disappears.", 22, YELLOW_D).move_to([0, 2.6, 0])
        assert_on_screen(note)
        self.say("So oscillation is not the enemy; only the size of the roots counts. With beta zero, the regimes coincide.",
                 FadeIn(note))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. tuning
    def tuning(self):
        head = self.heading("One learning rate, many curvatures")
        ax = Axes(x_range=[0, 3.2, 1], y_range=[0, 1.2, 0.5], x_length=8.4, y_length=2.7,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([-1.7, 0.2, 0])
        rx = VGroup(*[txt(f"{v}", 20, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.12) for v in (0, 1, 2, 3)])
        ry = VGroup(*[txt(f"{v:g}", 20, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12) for v in (0, 0.5, 1)])
        rxl = txt("s = η(1−β)λ", 22, C_ETA).next_to(ax.x_axis, DOWN, buff=0.45)
        one = DashedLine(ax.c2p(0, 1), ax.c2p(3.2, 1), color=C_LOSS, stroke_width=2)
        curve = clipped(ax, SS, RATES, 0, 1.2, C_MOM, 4)
        s1, s2 = 0.1, 2.0
        d1 = Dot(ax.c2p(s1, rate(s1)), radius=0.11, color=C_SOFT)
        d2 = Dot(ax.c2p(s2, rate(s2)), radius=0.11, color=C_STIFF)
        t1 = txt("λ = 1: soft", 22, C_SOFT).next_to(d1, DOWN, buff=0.3).shift(RIGHT * 0.9)
        t2 = txt("λ = 20: stiff", 22, C_STIFF).next_to(d2, DOWN, buff=0.3)
        arr = DoubleArrow(ax.c2p(s1, 0.05), ax.c2p(s2, 0.05), buff=0, color=YELLOW_D, stroke_width=3)
        ratio = txt("s values differ by the condition number κ = 20", 22, YELLOW_D).next_to(ax, DOWN, buff=0.7)
        assert_on_screen(VGroup(ax, rx, ry, rxl), t1, t2, ratio)
        self.say("A single eta must serve every eigenvalue. Each mode lands at its own s, the same curve scaled by its curvature.",
                 Write(head), Create(ax), FadeIn(rx), FadeIn(ry), FadeIn(rxl), Create(one), Create(curve), FadeIn(d1), FadeIn(t1), FadeIn(d2), FadeIn(t2))
        self.say("A soft mode wants a big step to leave the overdamped zone; a stiff one nears the edge. Their s differ by kappa.",
                 Create(arr), FadeIn(ratio))
        self.play(FadeOut(ax), FadeOut(rx), FadeOut(ry), FadeOut(rxl), FadeOut(one), FadeOut(curve), FadeOut(d1), FadeOut(d2),
                  FadeOut(t1), FadeOut(t2), FadeOut(arr), FadeOut(ratio))
        rule = mts([r"\kappa\le\Big(\frac{1+\sqrt\beta}{1-\sqrt\beta}\Big)^2\ \Rightarrow\ \text{every mode has rate }\sqrt\beta"], 0.8, {}).move_to([0, 2.3, 0])
        best = mts([r"\sqrt\beta=\frac{\sqrt\kappa-1}{\sqrt\kappa+1}", r"\ \Rightarrow\ \text{rate }\frac{\sqrt\kappa-1}{\sqrt\kappa+1}"], 0.85, {1: C_MOM}).move_to([0, 1.0, 0])
        gd = mts([r"\text{plain gradient descent: }\frac{\kappa-1}{\kappa+1}"], 0.8, {}).move_to([0, 0.15, 0])
        assert_on_screen(rule, best, gd)
        self.say("Tuning is a minimax problem: make the worst rate over all modes as small as possible, using the plateau.",
                 Write(rule))
        self.say("This works below a kappa bound set by beta. At the limit, the rate is root kappa minus one over root kappa plus one.",
                 Write(best))
        self.say("Plain gradient descent pays kappa minus one over kappa plus one. This is the standard tuned heavy-ball result.",
                 Write(gd))
        tab = VGroup(*[VGroup(txt(f"κ = {int(k)}", 26, WHITE),
                              txt(f"gradient descent: {round(STEPS((k - 1) / (k + 1)))} steps", 26, C_LOSS),
                              txt(f"tuned momentum: {round(STEPS((np.sqrt(k) - 1) / (np.sqrt(k) + 1)))} steps", 26, C_MOM)).arrange(RIGHT, buff=0.6)
                       for k in (20.0, 100.0)]).arrange(DOWN, buff=0.35).move_to([0, -1.75, 0])
        sub = txt("steps to shrink the error 100×", 22, GREY_B).next_to(tab, UP, buff=0.3)
        assert_on_screen(tab, sub)
        self.say("To shrink the error a hundredfold: kappa 20 takes 46 steps against 10; kappa 100, 230 against 23.",
                 FadeIn(sub), FadeIn(tab))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 5. Nesterov
    def nesterov(self):
        head = self.heading("Nesterov: measure at the look-ahead")
        rec = mts([r"v_{t+1}=\beta v_t+\nabla f\big(w_t-\alpha\beta v_t\big)", r"\qquad w_{t+1}=w_t-\alpha v_{t+1}"], 0.8, {}).move_to([0, 2.2, 0])
        ln = NumberLine(x_range=[0, 10, 1], length=9.0, color=GREY_B, include_numbers=False).move_to([0, 0.2, 0])
        w = Dot(ln.n2p(6.5), radius=0.12, color=C_ITER)
        wl = mt(r"w_t", 0.7, C_ITER).next_to(w, UP, buff=0.25)
        la = Dot(ln.n2p(4.8), radius=0.12, color=C_MOM)
        lal = mt(r"w_t-\alpha\beta v_t", 0.7, C_MOM).next_to(la, UP, buff=0.25)
        arr = Arrow(w.get_center() + LEFT * 0.15, la.get_center() + RIGHT * 0.15, buff=0, color=C_MOM, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        gl = txt("gradient is evaluated here", 22, C_GRAD).next_to(la, DOWN, buff=0.35)
        nt = txt("Other forms flip the sign of v or fold constants into the rate: compare complete recurrences.", 22, YELLOW_D).move_to([0, -1.6, 0])
        assert_on_screen(rec, VGroup(ln, w, wl, la, lal, gl), nt)
        self.say("Nesterov evaluates the gradient where the momentum is about to carry the iterate, then steps from here.",
                 Write(head), Write(rec), Create(ln), FadeIn(w), FadeIn(wl))
        self.say("Look ahead, then measure the slope there. Tuned Nesterov provably needs about root kappa steps.",
                 GrowArrow(arr), FadeIn(la), FadeIn(lal), FadeIn(gl))
        self.say("Conventions differ between books and libraries. Never mix one line from one convention with another's update.",
                 FadeIn(nt))
        self.hold(0.6)
        self.clear_stage()
