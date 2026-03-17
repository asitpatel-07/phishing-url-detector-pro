import os
import sys
import json
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import require_login
from config import MODEL_METRICS_PATH, TRAINING_REPORT_PATH

st.set_page_config(page_title="Model Insights", page_icon="🧠", layout="wide")
require_login()

if st.session_state.get("role") != "admin":
    st.error("Access denied. Admin only page.")
    st.stop()

st.title("🧠 Model Insights")

if not os.path.exists(MODEL_METRICS_PATH):
    st.error("Model metrics file not found. Pehle train model run karo.")
    st.stop()

with open(MODEL_METRICS_PATH, "r", encoding="utf-8") as f:
    metrics = json.load(f)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Accuracy", metrics.get("accuracy", 0))
with c2:
    st.metric("Phishing Precision", metrics.get("precision_phishing", 0))
with c3:
    st.metric("Phishing Recall", metrics.get("recall_phishing", 0))
with c4:
    st.metric("Phishing F1", metrics.get("f1_phishing", 0))

st.write("")

st.subheader("Dataset Summary")
st.write(f"- Total rows: {metrics.get('total_rows', 0)}")
st.write(f"- Train rows: {metrics.get('train_rows', 0)}")
st.write(f"- Test rows: {metrics.get('test_rows', 0)}")

st.subheader("Confusion Matrix")
cm = metrics.get("confusion_matrix", [[0, 0], [0, 0]])
st.write(cm)

if os.path.exists(TRAINING_REPORT_PATH):
    st.subheader("Training Report File")
    with open(TRAINING_REPORT_PATH, "r", encoding="utf-8") as f:
        report_text = f.read()
    st.text_area("Training Report", report_text, height=400)
else:
    st.info("Training report file not found.")