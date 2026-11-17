"""Trains the classifier on dataset.csv and saves model.joblib for the watcher."""
import pandas as pd

from classifier import save, train

df = pd.read_csv("dataset.csv").fillna("")
save(train(df.text, df.label, calibrate=True))
print(f"Trained (calibrated) on {len(df)} files -> model.joblib")
