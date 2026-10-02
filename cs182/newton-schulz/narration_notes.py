"""Seed text for a fresh narration.md (scene intros and the opening guide).
After the first `narration.py sync`, narration.md owns this text; edit it there."""

INTRO = """\
# Newton–Schulz: where does a singular value go? — narration script

> **How to use this file.** Everything here is plain text.
> - **Body** = the plain lines under each `###` heading. That text is the on-screen caption and what the voice says.
> - **`speak:`** (optional) = a different wording for the voice only, for math the voice would misread.
> - **Notes** = any line starting with `>` or `//`, and `<!-- ... -->`. Never rendered. Use them freely.
> - Do not edit the `### name NN <!-- #hash -->` heading lines: they tie each line to the code.
> - Keep each caption under ~105 characters (two lines). Check with `narration.py check`.
> - Preview: `render.py cs182/newton-schulz 1 --preview --voice` (only changed lines are re-voiced).
> - **Wording, tone and sentence order inside a scene** are edited here. **Which scene comes first, or
>   adding/removing a beat**, changes the animation code: write it in the scene's notes and ask Claude.

## The story in one paragraph

> A matrix W turns a circle into an ellipse; its singular values are the half-axes. Muon wants the
> update to be orthogonal (a circle, all stretches equal to 1), and the SVD is too slow. So we repeat one
> matrix-product-only step, and the SVD tells us each singular value just follows a number map p.
> The rest of the video is one question about p: where does a starting value σ end up? The answer is
> "+1" below √3, a flip past √3, a blow-up past √5, and in the thin gap between, a pattern of stripes.
> The video ends by turning that into a recipe: scale W first so every σ is below √3.

## The viewer, scene by scene (what they know, what they now want to ask)

> | # | Scene | Viewer already knows | Viewer now wants to know |
> |---|---|---|---|
> | 1 | ellipse | what a matrix does to a circle | why would anyone want W to be a circle? |
> | 2 | why_p | σ's are the half-axes; SVD is slow | where does the cubic come from? |
> | 3 | try_numbers | p(σ) = 1.5σ − 0.5σ³ and how to evaluate it | does it really go to 1? what stays put? |
> | 4 | cobweb | numbers 0.5, 1.3, 0.1 all go to 1 | can I see the whole iteration at once? |
> | 5 | slopes | the staircase picture; fixed points −1, 0, 1 | why do ±1 attract and 0 repel? |
> | 6 | how_big | small starts work; ±1 attract | how big can σ be before it breaks? |
> | 7 | too_big | 1.8 flipped to −1; the hump crosses at √3 | does everything past √3 go to −1? (3 explodes) |
> | 8 | the_gap | flips shrink up to √5, grow beyond | what happens between √3 and √5? |
> | 9 | first_boundary | a mysterious stripe pattern | where do the stripe edges come from? |
> | 10 | basins | the first edge b1 | all the edges, and the mirror argument |
> | 11 | boundary_points | the edges b_n climb to √5 | what are the edges exactly? ratio 6 |
> | 12 | summary | the complete picture | what is the one-line answer? |
> | 13 | back_to_matrix | the table of fates | so what do I do with my matrix? |
"""

_S = lambda title, *notes: [title, ""] + ["> " + n if n else ">" for n in notes]

SCENES = {
    "ellipse": _S(
        "## 01 · ellipse — Why would anyone iterate this? (motivation)",
        "**Purpose.** Give a reason to care before any formula. Muon wants an orthogonal update; the "
        "picture of 'orthogonal' is a circle.",
        "**Beats.** (1) W maps the unit circle to an ellipse. (2) SVD demo: rotate, stretch, rotate. "
        "(3) the stretches are σ1, σ2 = half-axes. (4) all stretches 1 means only rotations: orthogonal. "
        "(5) SVD is slow, so iterate with matrix products only; watch (1.3, 0.5) become a circle in 5 steps.",
        "**Tone.** Calm, concrete. No jargon before the picture.",
        "**Open choices.** Is the SVD demo too long before the viewer sees why? Would you start with the "
        "finished 5-step animation (the payoff) and then explain it?",
    ),
    "why_p": _S(
        "## 02 · why_p — You could have invented p (design)",
        "**Purpose.** Answer 'how could we possibly know this cubic?'. Matrix products give only odd powers "
        "of σ (σ, σ³, σ⁵), so the cheapest recipe is aσ + bσ³.",
        "**Beats.** SVD gives W_{k+1} = U p(Σ) Vᵀ, so each σ moves on its own. Powers: W→σ, WWᵀW→σ³. "
        "Two wishes, p(1)=1 and p′(1)=0, force a = 3/2, b = −1/2. Then the question that drives the "
        "rest: σ → p(σ) → p(p(σ)) → … → ?",
        "**Tone.** 'You could have done this yourself.' Slow on the two wishes; each is one sentence.",
        "**Open choices.** Is 'p′(1) = 0' motivated enough here, or should it wait until the slopes scene?",
    ),
    "try_numbers": _S(
        "## 03 · try_numbers — Just try numbers (easy cases first)",
        "**Purpose.** Build trust with starts that behave: 0.5, 1.3, 0.1 all go to 1, by hand arithmetic. "
        "Then ask what could stay put and solve p(x) = x step by step.",
        "**Beats.** p(0.5) arithmetic; the staircase of values; the algebra x(1−x)(1+x)=0 gives 0, 1, −1.",
        "**Tone.** Unhurried. Say each arithmetic step aloud; let the numbers appear one at a time.",
    ),
    "cobweb": _S(
        "## 04 · cobweb — The picture of the iteration",
        "**Purpose.** Turn the arithmetic into a graph: up to the curve, across to the diagonal, repeat.",
        "**Beats.** Axes with y=p(x) and y=x; one step with labelled points; why the diagonal; the "
        "staircase from 0.3; the same from 1.2.",
        "**Tone.** Explain the diagonal as 'height equals position', the one idea students trip on.",
    ),
    "slopes": _S(
        "## 05 · slopes — Why ±1 attract and 0 repels",
        "**Purpose.** Stability from the derivative. Linearize: p(x*+e) ≈ x* + p′(x*)·e.",
        "**Beats.** p′(0)=1.5 pushes away; p′(±1)=0 (the wish from scene 2) squares the error, so convergence "
        "is very fast.",
        "**Tone.** Connect back: 'this is exactly what we wished for'.",
    ),
    "how_big": _S(
        "## 06 · how_big — How big can σ be? (first failure)",
        "**Purpose.** Find the first threshold by trying a start that 'should' work.",
        "**Beats.** 1.5 works. Predict 1.8 (pause, let the viewer guess). It flips to −1. Factor "
        "p(x) = (x/2)(3−x²): the hump crosses the axis at √3. Shaded region shows (0, √3) → +1.",
        "**Tone.** A real pause before revealing 1.8. Ask the question and wait.",
    ),
    "too_big": _S(
        "## 07 · too_big — Try 3, and the line y = −x",
        "**Purpose.** Discover √5 as the boundary between shrinking and growing.",
        "**Beats.** 3 → −9 → 351. Compare 2.0 (lands at size 1) with 2.3 (lands at 2.63, bigger). "
        "Draw y=−x: flipped values shrink while the curve is above it; they meet at √5; √5 is a period-2 "
        "square. Beyond √5 diverges.",
        "**Tone.** The y = −x picture is the proof; keep the narration short while it draws.",
    ),
    "the_gap": _S(
        "## 08 · the_gap — The gap (√3, √5): show the mystery",
        "**Purpose.** Show the stripe pattern before explaining it. Starts in [0, 2.4] coloured by fate; zoom "
        "toward √5 shows stripes squeezed together. Then follow 2.0, 2.2, 2.23 and count flips.",
        "**Tone.** Curiosity, not authority. 'Why would that be?'",
        "**Open choices.** This is the hardest scene for a first-time viewer (your earlier feedback). "
        "Consider an easier warm-up start before the colour strip.",
    ),
    "first_boundary": _S(
        "## 09 · first_boundary — The first stripe edge b₁",
        "**Purpose.** Find where the first stripe starts: p(b₁) = −√3, so b₁³ − 3b₁ = 2√3, b₁ ≈ 2.148.",
        "**Tone.** Slow; this is where the algebra starts to feel heavy, so keep the picture on screen.",
    ),
    "basins": _S(
        "## 10 · basins — The mirror argument (the aha)",
        "**Purpose.** p maps each stripe onto the mirror image of the previous one, and p is odd, so the "
        "fates alternate −1, +1, −1, …  Check with 2.2.",
        "**Tone.** This is the payoff. Let the animation of piece 2 sliding onto piece 1 play in silence "
        "for a beat.",
    ),
    "boundary_points": _S(
        "## 11 · boundary_points — The edges converge to √5",
        "**Purpose.** b_n climb to √5; stripes shrink by a factor 6 each time because p′(√5) = −6; the "
        "edges reach ±√3 exactly, then 0.",
    ),
    "summary": _S(
        "## 12 · summary — The complete answer",
        "**Purpose.** One table of fates for every starting σ. Say it once, plainly.",
    ),
    "back_to_matrix": _S(
        "## 13 · back_to_matrix — So what do we do with W?",
        "**Purpose.** Close the loop: divide W by its Frobenius norm so every singular value is below √3, "
        "then iterate; all σ go to 1 and the ellipse becomes a circle.",
        "**Tone.** Practical and short. End on the picture of the circle.",
    ),
}
