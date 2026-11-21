"""Builds dataset.csv from dataset/<Category>/<files>. Folder name = label."""
import os
import sys

import pandas as pd

from features import build_text

ROOT = sys.argv[1] if len(sys.argv) > 1 else "dataset"

rows = []
for label in sorted(os.listdir(ROOT)):
    folder = os.path.join(ROOT, label)
    if not os.path.isdir(folder):
        continue
    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        print(f"[{len(rows) + 1}] {path}", flush=True)
        try:
            text, has_content = build_text(path)
        except Exception as e:  # one bad file must not stop the build
            print(f"  skipped content ({type(e).__name__}: {e})")
            text, has_content = "", False
        rows.append(dict(path=path, label=label, ext=os.path.splitext(name)[1].lower(),
                         text=text, has_content=has_content))

df = pd.DataFrame(rows)
df.to_csv("dataset.csv", index=False)
print(f"{len(df)} files, {df.label.nunique()} categories, {int(df.has_content.sum())} with readable content")
print(df.groupby("label").agg(files=("path", "count"), readable=("has_content", "sum")))
