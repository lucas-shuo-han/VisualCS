"""Pronunciations for the Newton–Schulz episode (read by tts.py).

Check with `python <skill>/scripts/captions.py cs182/newton-schulz 1 --spoken`.
"""

SAY_AS = {
    "Newton–Schulz": {"en": "Newton Schulz", "zh": "牛顿-舒尔茨"},
    "CS182": {"en": "C S 182", "zh": "C S 182"},
    "SVD": {"en": "S V D", "zh": "S V D"},
    "Frobenius": {"en": "Frobenius", "zh": "弗罗贝尼乌斯"},
}

REWRITES = [
    # ±√5, −√3, √3
    (r"±√(\d)", {"en": r"plus or minus root \1", "zh": r"正负根号\1"}),
    (r"[−-]√(\d)", {"en": r"negative root \1", "zh": r"负根号\1"}),
    (r"√(\d)", {"en": r"root \1", "zh": r"根号\1"}),
    # b1, b2 ... and bn
    (r"\bb(\d|n)\b", {"en": r"b \1", "zh": r"b \1"}),
    # p(x), p(σ), p(W)
    (r"\bp\((\w+)\)", {"en": r"p of \1", "zh": r"p \1"}),
    (r"\|p\(x\)\|", {"en": "the size of p of x", "zh": "p x 的绝对值"}),
    (r"\|x\|", {"en": "the size of x", "zh": "x 的绝对值"}),
    (r"σ", {"en": "sigma", "zh": "sigma"}),
    (r"Σ", {"en": "Sigma", "zh": "大 Sigma"}),
]
