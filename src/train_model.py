import os
import sys
import json
import joblib
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from config import (
    PROCESSED_DATA_PATH,
    MODEL_PATH,
    FEATURE_COLUMNS_PATH,
    MODEL_METRICS_PATH,
    TRAINING_REPORT_PATH,
)
from src.feature_extractor import extract_url_features
from src.utils import ensure_directories


def build_features(df):
    rows = []
    for url in df["url"]:
        rows.append(extract_url_features(url))
    return pd.DataFrame(rows)


def main():
    ensure_directories()

    print("Loading processed dataset...")
    df = pd.read_csv(PROCESSED_DATA_PATH)

    if "url" not in df.columns or "label" not in df.columns:
        raise ValueError("Processed dataset must contain 'url' and 'label' columns.")

    X = build_features(df)
    y = df["label"]

    feature_columns = X.columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=400,
        max_depth=18,
        min_samples_split=4,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    matrix = confusion_matrix(y_test, y_pred).tolist()

    metrics_data = {
        "accuracy": round(float(accuracy), 4),
        "precision_legitimate": round(report["0"]["precision"], 4),
        "recall_legitimate": round(report["0"]["recall"], 4),
        "precision_phishing": round(report["1"]["precision"], 4),
        "recall_phishing": round(report["1"]["recall"], 4),
        "f1_legitimate": round(report["0"]["f1-score"], 4),
        "f1_phishing": round(report["1"]["f1-score"], 4),
        "confusion_matrix": matrix,
        "total_rows": int(len(df)),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
    }

    joblib.dump(model, MODEL_PATH)
    joblib.dump(feature_columns, FEATURE_COLUMNS_PATH)

    with open(MODEL_METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=4)

    with open(TRAINING_REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("Training Report\n")
        f.write("====================\n")
        f.write(f"Total rows: {len(df)}\n")
        f.write(f"Train rows: {len(X_train)}\n")
        f.write(f"Test rows: {len(X_test)}\n")
        f.write(f"Accuracy: {accuracy:.4f}\n\n")
        f.write("Classification Report:\n")
        f.write(classification_report(y_test, y_pred))
        f.write("\nConfusion Matrix:\n")
        f.write(str(confusion_matrix(y_test, y_pred)))

    print("Model training completed.")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Feature columns saved to: {FEATURE_COLUMNS_PATH}")
    print(f"Metrics saved to: {MODEL_METRICS_PATH}")
    print(f"Training report saved to: {TRAINING_REPORT_PATH}")


if __name__ == "__main__":
    main()