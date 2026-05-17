import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "model.pkl"
FEATURE_NAMES = [
    "age", "education_num", "hours_per_week",
    "capital_gain", "capital_diff"
]

def train_and_save():
    """Train a simple RF classifier on Adult Income data and persist it."""
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
    cols = [
        "age","workclass","fnlwgt","education","education_num",
        "marital_status","occupation","relationship","race","sex",
        "capital_gain","capital_loss","hours_per_week","native_country","income"
    ]
    df = pd.read_csv(url, names=cols, na_values=" ?", skipinitialspace=True)
    df.dropna(inplace=True)

    # Feature engineering — keep numeric + one derived feature
    df["capital_diff"] = df["capital_gain"] - df["capital_loss"]
    df["label"] = (df["income"].str.strip() == ">50K").astype(int)

    X = df[FEATURE_NAMES]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Model trained. Test accuracy: {acc:.3f}")

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"Model saved to {MODEL_PATH}")

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model not found. Run train_and_save() first.")
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

if __name__ == "__main__":
    train_and_save()