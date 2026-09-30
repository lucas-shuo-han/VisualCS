# CS182 Discussion 5 · Newton–Schulz: where does a singular value go?

One episode (~11 min), written and voiced in English (Kokoro-82M neural voice, offline;
edge-tts when its host is reachable). Source: EECS 182 Fall 2026
Discussion 5, problem 1 (solutions), plus a scene/correctness brief for part (e).

**Question it answers:** a singular value starts at +σ and is repeatedly replaced by
p(σ) = 1.5σ − 0.5σ³. Does it end at +1, −1, 0, or blow up, and why?

**Principle:** nothing appears before the viewer has a reason to ask for it. Each key
number is discovered by trying a start that "should" work and seeing it fail.

**Aha beat:** p maps each piece (b(n−1), b(n)) of (√3, √5) onto the mirror image of the
previous piece, and p is odd, so the fates alternate −1, +1, −1, … The pieces shrink by
a factor 6 toward √5 because p′(√5) = −6.

## Story

1. Motivation: W turns the unit circle into an ellipse with half-axes σ1, σ2. Orthogonal
   means every stretch is 1 (Muon wants this per update). SVD is slow; Newton–Schulz
   uses matrix products only. Watch (1.3, 0.5) become a circle in 5 steps.
2. Why it works: SVD, W_{k+1} = U p(Σ) Vᵀ, so each σ follows p on its own. Part (e).
3. Just try numbers: 0.5, 1.3, 0.1 all go to 1. p(1) = 1 → fixed points −1, 0, 1.
4. Graph and cobweb (0.3 and 1.2); fixed points are where the curve meets y = x.
5. Slopes: p′(0) = 1.5 pushes away, p′(±1) = 0 squares the error.
6. "How big can σ be?" 1.5 works, 1.8 goes to −1. Factoring finds √3; proof that
   (0, √3) → +1; √3 → 0.
7. "What about 3?" It explodes. The ratio |p(x)|/|x| finds √5; √5 is period 2; 2.3 diverges.
8. The gap (√3, √5): flips while shrinking, so it falls below √3 eventually. Test 2.0,
   2.2, 2.23: −1, +1, −1. Odd flips → −1, even → +1.
9. b1 with p(b1) = −√3; (√3, b1) → (−√3, 0) → −1; 1.8 and 2 live here, p(2) = −1.
10. b_n with b_n³ − 3b_n = 2b_(n−1); mirror mapping; alternating basins; zoom toward √5.
11. Boundary points reach ±√3 exactly, then 0.
12. The full answer table.
13. Back to the matrix: normalize by the Frobenius norm, all σ → 1, the ellipse is a circle.

## Coverage

| Source item | Where |
|---|---|
| (a) p(W) = U p(Σ) Vᵀ via WWᵀ = UΣ²Uᵀ | §2 |
| (b) fixed points 0, ±1 | §3 |
| (c) p′(x) = 3/2 − 3/2 x²; 0 unstable, ±1 stable | §5 |
| (d) cobweb diagram, the solution's x₀ = 0.3 example | §4 |
| (e) (0, √3) → +1; √3 → 0; flips past √3; √5 period 2; > √5 diverges | §6–7, §12 |
| (e) refinement: basins (b(n−1), b(n)) alternate −1/+1, b_n ↑ √5, b_n → 0 | §8–11 |
| (f) why this orthogonalizes, and what to ensure first | §1–2, §13 |

The solution's line for (e), "for σ > √3, σ will either converge to −1 or even diverge",
is too coarse: (b1, b2) ∋ 2.2 goes to +1 (§8).
The Frobenius-norm scaling in §13 is standard practice, not stated in the solution.

All numbers on screen are computed in `ep01_newton_schulz.py`; the b_n values, flip
counts, basin fates, the easy starts and the ratio 6 are asserted at import time.
