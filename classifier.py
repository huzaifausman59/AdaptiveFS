"""TF-IDF + Logistic Regression classifier with probability output."""
import joblib
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline


def make_model():
    return make_pipeline(
        TfidfVectorizer(sublinear_tf=True, ngram_range=(1, 2), min_df=2),
        LogisticRegression(max_iter=1000, class_weight="balanced"),
    )


def train(texts, labels, calibrate=False):
    model = CalibratedClassifierCV(make_model(), method="sigmoid", cv=3) if calibrate else make_model()
    return model.fit(texts, labels)


def predict(model, text):
    """Returns (label, confidence) for one text."""
    p = model.predict_proba([text])[0]
    i = p.argmax()
    return model.classes_[i], float(p[i])


def save(model, path="model.joblib"):
    joblib.dump(model, path)


def load(path="model.joblib"):
    return joblib.load(path)
