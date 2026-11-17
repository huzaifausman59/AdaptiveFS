"""E1: content classifier vs extension-only baseline, plus a small model comparison.
Run from the repo root:  python -m experiments.e1"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, f1_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.svm import LinearSVC

os.makedirs("results", exist_ok=True)
df = pd.read_csv("dataset.csv").fillna("")
df["has_content"] = df.has_content.astype(bool)

MODELS = {
    "TFIDF+LogReg": lambda: LogisticRegression(max_iter=1000, class_weight="balanced"),
    "TFIDF+LinearSVM": lambda: LinearSVC(class_weight="balanced"),
    "TFIDF+NaiveBayes": lambda: MultinomialNB(),
}
vec = lambda: TfidfVectorizer(sublinear_tf=True, ngram_range=(1, 2), min_df=2)

cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)
rows, y_true, y_pred = [], [], []
for tr, te in cv.split(df, df.label):
    a, b = df.iloc[tr], df.iloc[te]
    ext_map, default = a.groupby("ext").label.agg(lambda s: s.mode()[0]), a.label.mode()[0]
    preds = {"ext-baseline": b.ext.map(ext_map).fillna(default)}
    for name, clf in MODELS.items():
        preds[name] = pd.Series(make_pipeline(vec(), clf()).fit(a.text, a.label).predict(b.text), index=b.index)
    y_true += list(b.label); y_pred += list(preds["TFIDF+LogReg"])
    for name, pr in preds.items():
        for subset, mask in [("all", pd.Series(True, index=b.index)),
                             ("content-accessible", b.has_content),
                             ("metadata-only", ~b.has_content)]:
            d = b[mask]
            if len(d):
                rows.append(dict(model=name, subset=subset, acc=accuracy_score(d.label, pr[d.index]),
                                 macro_f1=f1_score(d.label, pr[d.index], average="macro", zero_division=0)))

res = (pd.DataFrame(rows).groupby(["subset", "model"])
       .agg(acc=("acc", "mean"), acc_std=("acc", "std"), macro_f1=("macro_f1", "mean"), f1_std=("macro_f1", "std"))
       .round(3))
print(res)
res.to_csv("results/e1_results.csv")

fig, ax = plt.subplots(figsize=(7, 6))
ConfusionMatrixDisplay.from_predictions(y_true, y_pred, normalize="true", xticks_rotation=45,
                                        ax=ax, colorbar=False, values_format=".2f")
ax.set_title("TF-IDF + LogReg (all folds, row-normalised)")
fig.tight_layout(); fig.savefig("results/e1_confusion_matrix.png", dpi=200)
print("Saved results/e1_results.csv and results/e1_confusion_matrix.png")
