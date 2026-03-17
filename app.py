import os
import streamlit as st

from auth.login import require_login, logout_button
from config import APP_TITLE

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🛡️",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None

if "history" not in st.session_state:
    st.session_state.history = []

if "latest_report_html" not in st.session_state:
    st.session_state.latest_report_html = None


def load_template(file_name):
    file_path = os.path.join("templates", file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h2>Template not found</h2>"


st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617 0%, #0f172a 35%, #111827 70%, #1e293b 100%);
    color: white;
}
.block-container {
    max-width: 1250px;
    padding-top: 1.2rem;
    padding-bottom: 90px;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
.footer-box {
    margin-top: 28px;
    padding: 18px;
    border-radius: 18px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    text-align: center;
    color: #cbd5e1;
    font-size: 0.92rem;
}
.fixed-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    text-align: center;
    padding: 10px 12px;
    background: rgba(2, 6, 23, 0.95);
    border-top: 1px solid rgba(255,255,255,0.08);
    color: #f8fafc;
    font-size: 15px;
    font-weight: 700;
    z-index: 9999;
    backdrop-filter: blur(6px);
}
</style>
""", unsafe_allow_html=True)

require_login()

with st.sidebar:
    st.success(f"👤 Logged in as: {st.session_state.username}")
    st.info(f"Role: {st.session_state.role}")
    st.markdown("---")
    logout_button()

st.markdown(load_template("dashboard.html"), unsafe_allow_html=True)

st.markdown("""
<div style="
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 24px;
    margin-top: 10px;
">
    <h3 style="color:white;">🚀 Welcome to the Project Home</h3>
    <p style="color:#dbeafe;">
        This is a production-style phishing URL detection project built with:
        Python, Streamlit, Machine Learning, SQLite, HTML/CSS, and Real-Time URL Analysis.
    </p>
    <ul style="color:#cbd5e1; line-height:1.8;">
        <li>User Scanner page for live URL scanning</li>
        <li>Scan History page for stored results</li>
        <li>Admin Dashboard for analytics</li>
        <li>Model Insights page for ML metrics</li>
    </ul>
    <p style="color:#f8fafc;"><b>Use the left sidebar pages to navigate.</b></p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer-box">
    Built with ❤️ Asit using Python, Streamlit, Machine Learning, HTML, CSS, and Cybersecurity logic.<br>
    Project: Advanced AI Phishing URL Detection System
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="fixed-footer">
    Developed By : Asit ❤️
</div>
""", unsafe_allow_html=True)