import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import RAW_DATA_PATH, PROCESSED_DATA_PATH
from src.utils import ensure_directories


def preprocess_dataset():
    ensure_directories()

    df = pd.read_csv(RAW_DATA_PATH)

    if "url" not in df.columns or "label" not in df.columns:
        raise ValueError("Dataset must contain 'url' and 'label' columns.")

    df = df.dropna(subset=["url", "label"]).copy()
    df["url"] = df["url"].astype(str).str.strip()
    df["label"] = df["label"].astype(int)

    df = df[df["url"] != ""]
    df = df.drop_duplicates(subset=["url"])

    df.to_csv(PROCESSED_DATA_PATH, index=False)

    print("Dataset preprocessing completed.")
    print(f"Cleaned rows: {len(df)}")
    print(f"Saved to: {PROCESSED_DATA_PATH}")


if __name__ == "__main__":
    preprocess_dataset()