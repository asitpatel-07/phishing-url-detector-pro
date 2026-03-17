import os
import sys
import json
import sqlite3
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DB_PATH


def ensure_directories():
    folders = [
        "data/raw",
        "data/processed",
        "data/reports",
        "models",
        "database",
        "templates",
        "assets",
        "pages",
        "auth",
        "src",
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)


def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_json(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn