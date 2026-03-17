import os
import sys
import pandas as pd
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import require_login
from src.utils import get_db_connection

st.set_page_config(page_title="Scan History", page_icon="📜", layout="wide")
require_login()

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617 0%, #0f172a 35%, #111827 70%, #1e293b 100%);
    color: white;
}
.block-container {
    padding-bottom: 90px;
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

st.title("📜 Scan History")

current_user = st.session_state.get("username", "unknown")
current_role = st.session_state.get("role", "user")


def get_user_scan_history(username):
    conn = get_db_connection()
    query = """
        SELECT id, username, url, prediction, risk_score, phishing_confidence,
               legitimate_confidence, severity, domain_resolves, http_status, scan_time
        FROM scan_history
        WHERE username = ?
        ORDER BY id DESC
    """
    df = pd.read_sql_query(query, conn, params=(username,))
    conn.close()
    return df


def get_all_scan_history():
    conn = get_db_connection()
    query = """
        SELECT id, username, url, prediction, risk_score, phishing_confidence,
               legitimate_confidence, severity, domain_resolves, http_status, scan_time
        FROM scan_history
        ORDER BY id DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def reset_user_scan_history(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scan_history WHERE username = ?", (username,))
    conn.commit()
    conn.close()


def reset_all_scan_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scan_history")
    conn.commit()
    conn.close()


if current_role != "admin":
    st.subheader("👤 Your Scan History")

    col1, col2 = st.columns([1, 3])

    with col1:
        if st.button("🗑️ Reset My History", use_container_width=True):
            reset_user_scan_history(current_user)
            st.success("Your scan history has been reset successfully.")
            st.rerun()

    user_df = get_user_scan_history(current_user)

    if user_df.empty:
        st.info("No scan history found for your account.")
    else:
        st.dataframe(user_df, use_container_width=True, hide_index=True)

else:
    st.subheader("🛠️ Admin Scan History Panel")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("🗑️ Reset My History", use_container_width=True):
            reset_user_scan_history(current_user)
            st.success("Admin personal scan history has been reset.")
            st.rerun()

    with c2:
        if st.button("🔥 Reset ALL Users History", use_container_width=True):
            reset_all_scan_history()
            st.success("All users scan history has been reset.")
            st.rerun()

    st.write("")

    st.subheader("📊 All Scan Records")
    all_df = get_all_scan_history()

    if all_df.empty:
        st.info("No scan history found in system.")
    else:
        st.dataframe(all_df, use_container_width=True, hide_index=True)

st.markdown("""
<div class="fixed-footer">
    Developed By : Asit ❤️
</div>
""", unsafe_allow_html=True)