# CS182 Discussion 5 · Newton–Schulz: where does a singular value go?

One episode (~8–9 min), written in Chinese, translated to English through `i18n/ep01.py`.
Source: EECS 182 Fall 2026 Discussion 5, problem 1 (solutions), plus a scene/correctness
brief for part (e).

**Question it answers:** a singular value starts at +σ and is repeatedly replaced by
p(σ) = 1.5σ − 0.5σ³. Does it end at +1, −1, 0, or blow up, and why?

**Aha beat:** p maps each piece (b(n−1), b(n)) of (√3, √5) onto the mirror image of the
previous piece, and p is odd, so the fates alternate −1, +1, −1, … The pieces shrink by
a factor 6 toward √5 because p′(√5) = −6.

## Story

1. Mystery: 2.00, 2.20, 2.23 end at −1, +1, −1.
2. Where p comes from: Newton–Schulz, SVD, p(W) = U p(Σ) Vᵀ, orthogonalization.
3. Graph of p and y = x, cobweb diagrams (0.3 and 1.2).
4. Fixed points −1, 0, 1; slopes 1.5 (unstable) and 0 (stable, error squares).
5. 0 < σ < √3 → +1 (sign kept, max p = 1, then monotone climb); σ = √3 → 0.
6. Two thresholds: √3 (sign flips) and √5 (|p(x)|/|x| < 1 iff |x| < √5).
7. The edge: √5 ↔ −√5 is a period-2 orbit; σ > √5 diverges with alternating signs.
8. Between √3 and √5: count flips on the |x| axis; odd → −1, even → +1.
9. b1 with p(b1) = −√3; (√3, b1) → (−√3, 0) → −1; p(2) = −1.
10. b_n with b_n³ − 3b_n = 2b_(n−1); mirror mapping; alternating basins; zoom toward √5.
11. Boundary points reach ±√3 exactly, then 0.
12. The full answer table.
13. Back to the matrix: normalize by the Frobenius norm, then all σ → 1 and W → UVᵀ.

## Coverage

| Source item | Where |
|---|---|
| (a) p(W) = U p(Σ) Vᵀ via WWᵀ = UΣ²Uᵀ | §2 |
| (b) fixed points 0, ±1 | §4 |
| (c) p′(x) = 3/2 − 3/2 x²; 0 unstable, ±1 stable | §4 |
| (d) cobweb diagram, the solution's x₀ = 0.3 example | §3 |
| (e) (0, √3) → +1; √3 → 0; flips past √3; √5 period 2; > √5 diverges | §5–7, §12 |
| (e) refinement: basins (b(n−1), b(n)) alternate −1/+1, b_n ↑ √5, b_n → 0 | §8–11 |
| (f) why this orthogonalizes, and what to ensure first | §2, §13 |

The solution's line for (e), "for σ > √3, σ will either converge to −1 or even diverge",
is too coarse: (b1, b2) ∋ 2.2 goes to +1. The video quotes it and corrects it (§8).
The Frobenius-norm scaling in §13 is standard practice, not stated in the solution.

All numbers on screen are computed in `ep01_newton_schulz.py`; the b_n values, flip
counts, basin fates and the ratio 6 are asserted at import time.
