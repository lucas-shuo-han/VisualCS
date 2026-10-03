"""Width-transfer experiment for episodes 5-6 (numpy only, cached in width_demo_cache.npz).

A 3-layer ReLU MLP (input 8 -> width -> width -> 1) trained with Adam on a small regression task.
"standard": one learning rate for every layer.
"scaled":   learning rate for layers whose fan-in is the width multiplied by BASE_W / width
            (the first layer keeps fan-in 8, so its rate is not scaled): eta ~ 1 / d_in per layer.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np

WIDTHS = [32, 64, 128, 256, 512]
LOG2_LRS = list(range(-11, -3))
BASE_W = 32
SEEDS = [1, 2]
STEPS = 200
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "width_demo_cache.npz")


def data(n=512, din=8):
    r = np.random.RandomState(0)
    X = r.randn(n, din)
    y = np.tanh(X @ r.randn(din, 3)).sum(1, keepdims=True) * 0.7
    return X, y


X, Y = data()


def train(width, lr, rule, seed, steps=STEPS, bs=32):
    r = np.random.RandomState(seed)
    din = X.shape[1]
    P = [r.randn(din, width) / np.sqrt(din), r.randn(width, width) / np.sqrt(width), np.zeros((width, 1))]
    k = BASE_W / width if rule == "scaled" else 1.0
    lrs = [lr, lr * k, lr * k]
    m = [np.zeros_like(p) for p in P]
    v = [np.zeros_like(p) for p in P]
    for t in range(1, steps + 1):
        idx = r.randint(0, len(X), bs)
        xb, yb = X[idx], Y[idx]
        z0 = xb @ P[0]; h0 = np.maximum(z0, 0)
        z1 = h0 @ P[1]; h1 = np.maximum(z1, 0)
        d = (h1 @ P[2] - yb) / bs
        g2 = h1.T @ d
        dh1 = (d @ P[2].T) * (z1 > 0); g1 = h0.T @ dh1
        dh0 = (dh1 @ P[1].T) * (z0 > 0); g0 = xb.T @ dh0
        for i, g in enumerate((g0, g1, g2)):
            m[i] = 0.9 * m[i] + 0.1 * g
            v[i] = 0.999 * v[i] + 0.001 * g * g
            P[i] -= lrs[i] * (m[i] / (1 - 0.9 ** t)) / (np.sqrt(v[i] / (1 - 0.999 ** t)) + 1e-8)
    out = np.maximum(np.maximum(X @ P[0], 0) @ P[1], 0) @ P[2]
    L = float(np.mean((out - Y) ** 2))
    return L if np.isfinite(L) else 1e3


def results():
    """dict rule -> array [len(WIDTHS), len(LOG2_LRS)] of mean final MSE."""
    if os.path.exists(CACHE):
        z = np.load(CACHE)
        return {"standard": z["standard"], "scaled": z["scaled"]}
    res = {}
    for rule in ("standard", "scaled"):
        res[rule] = np.array([[np.mean([train(w, 2.0 ** e, rule, s) for s in SEEDS]) for e in LOG2_LRS] for w in WIDTHS])
    np.savez(CACHE, **res)
    return res


if __name__ == "__main__":
    import time
    t = time.time()
    R = results()
    for rule, M in R.items():
        print(rule)
        for w, row in zip(WIDTHS, M):
            print(w, "best 2^%d" % LOG2_LRS[int(np.argmin(row))], " ".join("%.3f" % x for x in row))
    print("%.0fs" % (time.time() - t))
