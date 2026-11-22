import glob, os, re
import numpy as np, pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from classifier import make_model

df = pd.read_csv("dataset.csv").fillna("")
df["file"] = df.path.str.replace("\\", "/").str.split("/").str[-1]
df["has_content"] = df.has_content.astype(bool)

GENERATED = {"ds_assignment1_stack.py", "ds_assignment3_linkedlist.py", "db_lab3_sqlite.py"}
src = {}
for f in sorted(glob.glob("logs/sources_log*.csv")):
    for r in pd.read_csv(f).itertuples(): src[(r.category, r.file)] = r.source
def origin(r):
    s = src.get((r.label, r.file))
    if s is not None: return "generated" if s.startswith("generated") else "public"
    if r.file in GENERATED: return "generated"
    return "public" if r.label == "Research" else "own"
df["origin"] = df.apply(origin, axis=1)

t = df.groupby("label").agg(files=("path", "count"), readable=("has_content", "sum"))
t["metadata_only"] = t.files - t.readable
o = pd.crosstab(df.label, df.origin)
print("== files / readable / metadata-only\n", t, f"\ntotal {len(df)}, metadata-only {int((~df.has_content).sum())}")
print("\n== origin per category\n", o)
print("\n== extensions per category\n", pd.crosstab(df.label, df.ext))
print("\n== metadata-only files\n", df[~df.has_content][["label", "file"]].to_string(index=False))
os.makedirs("results", exist_ok=True); t.join(o).to_csv("results/dataset_summary.csv")

y = df.label.values
p = cross_val_predict(make_model(), df.text, y, cv=StratifiedKFold(5, shuffle=True, random_state=42), method="predict_proba")
pred = np.unique(y)[p.argmax(1)]
print(f"\n== misclassified files: {int((pred != y).sum())} of {len(y)}")
for i in np.where(pred != y)[0]: print(f"  {y[i]:12s} -> {pred[i]:12s} conf={p[i].max():.2f}  {df.file[i]}")