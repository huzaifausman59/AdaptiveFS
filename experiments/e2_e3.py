"""E2 calibration (ECE, reliability diagram) and E3 gate trade-off (risk-coverage).
Run from the repo root:  python -m experiments.e2_e3"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_predict

from sklearn.calibration import CalibratedClassifierCV

from classifier import make_model

os.makedirs("results", exist_ok=True)
df = pd.read_csv("dataset.csv").fillna("")
y = df.label.values
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)


def oof_confidence(model):
    """Out-of-fold predicted probabilities -> (confidence, correct) arrays."""
    proba = cross_val_predict(model, df.text, y, cv=cv, method="predict_proba")
    classes = np.unique(y)
    pred = classes[proba.argmax(1)]
    return proba.max(1), (pred == y).astype(float)


def ece(conf, correct, bins=10):
    idx = np.minimum((conf * bins).astype(int), bins - 1)
    return sum((idx == b).mean() * abs(correct[idx == b].mean() - conf[idx == b].mean())
               for b in range(bins) if (idx == b).any())


def reliability(ax, conf, correct, title, bins=10):
    idx = np.minimum((conf * bins).astype(int), bins - 1)
    xs = [conf[idx == b].mean() for b in range(bins) if (idx == b).any()]
    ys = [correct[idx == b].mean() for b in range(bins) if (idx == b).any()]
    ax.plot([0, 1], [0, 1], "k--", lw=1); ax.plot(xs, ys, "o-")
    ax.set(title=title, xlabel="Mean confidence", ylabel="Accuracy", xlim=(0, 1), ylim=(0, 1))


raw = oof_confidence(make_model())
cal = oof_confidence(CalibratedClassifierCV(make_model(), method="sigmoid", cv=3))

print(f"ECE  uncalibrated: {ece(*raw):.3f}   calibrated (sigmoid): {ece(*cal):.3f}")
fig, axs = plt.subplots(1, 2, figsize=(9, 4))
reliability(axs[0], *raw, f"Uncalibrated (ECE {ece(*raw):.3f})")
reliability(axs[1], *cal, f"Sigmoid-calibrated (ECE {ece(*cal):.3f})")
fig.tight_layout(); fig.savefig("results/e2_reliability.png", dpi=200)

rows = []
for tau in np.arange(0.3, 0.96, 0.05):
    for name, (conf, correct) in {"uncalibrated": raw, "calibrated": cal}.items():
        m = conf >= tau
        if m.any():
            rows.append(dict(model=name, tau=round(tau, 2), coverage=m.mean(), selective_risk=1 - correct[m].mean()))
rc = pd.DataFrame(rows).round(3)
print(rc.to_string(index=False)); rc.to_csv("results/e3_risk_coverage.csv", index=False)

fig, ax = plt.subplots(figsize=(5, 4))
for name, g in rc.groupby("model"):
    ax.plot(g.coverage, g.selective_risk, "o-", label=name)
ax.set(xlabel="Coverage (fraction auto-sorted)", ylabel="Selective risk (error rate)", title="Risk-coverage")
ax.legend(); fig.tight_layout(); fig.savefig("results/e3_risk_coverage.png", dpi=200)
print("Saved results/e2_reliability.png, e3_risk_coverage.png/.csv")
