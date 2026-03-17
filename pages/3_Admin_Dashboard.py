import os
import sys
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import require_login
from src.utils import get_db_connection

st.set_page_config(page_title="Admin Dashboard", page_icon="📈", layout="wide")
require_login()

if st.session_state.get("role") != "admin":
    st.error("Access denied. Admin only page.")
    st.stop()

st.title("📈 Admin Dashboard")

conn = get_db_connection()

stats_df = pd.read_sql_query("SELECT * FROM app_stats WHERE id = 1", conn)
history_df = pd.read_sql_query("SELECT * FROM scan_history ORDER BY id DESC", conn)
conn.close()

if stats_df.empty:
    st.warning("App stats not found.")
    st.stop()

stats = stats_df.iloc[0]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Scans", int(stats["total_scans"]))
with c2:
    st.metric("Phishing Detected", int(stats["phishing_detected"]))
with c3:
    st.metric("Legitimate Detected", int(stats["legitimate_detected"]))
with c4:
    st.metric("Last Updated", str(stats["last_updated"]))

st.write("")

if not history_df.empty:
    st.subheader("Prediction Distribution")
    pred_counts = history_df["prediction"].value_counts()

    fig, ax = plt.subplots(figsize=(5, 3.2))
    ax.bar(pred_counts.index.tolist(), pred_counts.values.tolist())
    ax.set_title("Phishing vs Legitimate")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    st.subheader("Top 10 Risky URLs")
    risky_df = history_df.sort_values(by="risk_score", ascending=False).head(10)
    st.dataframe(
        risky_df[["url", "prediction", "risk_score", "severity", "scan_time"]],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Recent Scans")
    st.dataframe(
        history_df[["url", "prediction", "risk_score", "severity", "scan_time"]].head(15),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No scan data available yet.")