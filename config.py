import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")

MODELS_DIR = os.path.join(BASE_DIR, "models")
DATABASE_DIR = os.path.join(BASE_DIR, "database")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

RAW_DATA_PATH = os.path.join(RAW_DATA_DIR, "urls.csv")
PROCESSED_DATA_PATH = os.path.join(PROCESSED_DATA_DIR, "cleaned_urls.csv")
TRAINING_REPORT_PATH = os.path.join(REPORTS_DIR, "training_report.txt")

MODEL_PATH = os.path.join(MODELS_DIR, "phishing_model.pkl")
FEATURE_COLUMNS_PATH = os.path.join(MODELS_DIR, "feature_columns.pkl")
MODEL_METRICS_PATH = os.path.join(MODELS_DIR, "model_metrics.json")

DB_PATH = os.path.join(DATABASE_DIR, "app.db")

APP_TITLE = "Advanced AI Phishing URL Detection System"