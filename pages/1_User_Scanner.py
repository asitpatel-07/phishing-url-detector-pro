import os
import sys
import time
from datetime import datetime

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import require_login
from src.predict import predict_url
from src.feature_extractor import normalize_url
from src.realtime_checks import run_realtime_checks
from src.blacklist_checker import is_url_blacklisted
from src.report_generator import generate_html_report
from src.utils import get_db_connection, get_current_timestamp
from src.block_manager import (
    block_url_for_24_hours,
    is_url_currently_blocked,
    remove_expired_blocks
)

st.set_page_config(page_title="User Scanner", page_icon="🔍", layout="wide")
require_login()

if "history" not in st.session_state:
    st.session_state.history = []

if "latest_report_html" not in st.session_state:
    st.session_state.latest_report_html = None


def save_scan_to_db(username, url, prediction, risk_score, phishing_conf, legit_conf, severity, domain_resolves, http_status):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scan_history (
            username, url, prediction, risk_score, phishing_confidence, legitimate_confidence,
            severity, domain_resolves, http_status, scan_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        url,
        prediction,
        risk_score,
        phishing_conf,
        legit_conf,
        severity,
        str(domain_resolves),
        str(http_status),
        get_current_timestamp()
    ))

    cursor.execute("SELECT * FROM app_stats WHERE id = 1")
    row = cursor.fetchone()

    if row:
        total_scans = row["total_scans"] + 1
        phishing_detected = row["phishing_detected"] + (1 if prediction == "Phishing" else 0)
        legitimate_detected = row["legitimate_detected"] + (1 if prediction == "Legitimate" else 0)

        cursor.execute("""
            UPDATE app_stats
            SET total_scans = ?, phishing_detected = ?, legitimate_detected = ?, last_updated = ?
            WHERE id = 1
        """, (
            total_scans,
            phishing_detected,
            legitimate_detected,
            get_current_timestamp()
        ))

    conn.commit()
    conn.close()


def format_remaining_time(seconds_left: int) -> str:
    hours = seconds_left // 3600
    minutes = (seconds_left % 3600) // 60
    seconds = seconds_left % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def show_live_block_countdown(blocked_until_str: str):
    blocked_until = datetime.strptime(blocked_until_str, "%Y-%m-%d %H:%M:%S")
    box = st.empty()

    while True:
        now = datetime.now()
        remaining_seconds = int((blocked_until - now).total_seconds())

        if remaining_seconds <= 0:
            box.markdown("""
            <div class="result-safe">
                ✅ Block expired. You can scan this URL again now.
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
            st.rerun()

        remaining_time = format_remaining_time(remaining_seconds)

        box.markdown(f"""
        <div class="result-danger">
            ⛔ This URL is temporarily blocked for 4 hours due to high phishing risk.<br>
            Block active until: {blocked_until_str}<br><br>
            <b>Remaining Time:</b> {remaining_time}
        </div>
        """, unsafe_allow_html=True)

        time.sleep(1)


st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617 0%, #0f172a 35%, #111827 70%, #1e293b 100%);
    color: white;
}
.block-container {
    padding-bottom: 90px;
}
.metric-box {
    border-radius: 22px;
    padding: 18px;
    color: white;
    font-weight: 700;
    box-shadow: 0 10px 22px rgba(0,0,0,0.20);
}
.metric-blue { background: linear-gradient(135deg, #2563eb, #1d4ed8); }
.metric-pink { background: linear-gradient(135deg, #db2777, #be185d); }
.metric-green { background: linear-gradient(135deg, #16a34a, #15803d); }
.metric-orange { background: linear-gradient(135deg, #ea580c, #c2410c); }

.result-safe {
    background: linear-gradient(135deg, rgba(34,197,94,0.22), rgba(22,163,74,0.14));
    border: 1px solid rgba(34,197,94,0.45);
    color: #dcfce7;
    padding: 16px;
    border-radius: 18px;
    font-weight: 800;
    margin-bottom: 18px;
}
.result-warn {
    background: linear-gradient(135deg, rgba(245,158,11,0.22), rgba(217,119,6,0.14));
    border: 1px solid rgba(245,158,11,0.45);
    color: #fef3c7;
    padding: 16px;
    border-radius: 18px;
    font-weight: 800;
    margin-bottom: 18px;
}
.result-danger {
    background: linear-gradient(135deg, rgba(239,68,68,0.22), rgba(220,38,38,0.14));
    border: 1px solid rgba(239,68,68,0.45);
    color: #fee2e2;
    padding: 16px;
    border-radius: 18px;
    font-weight: 800;
    margin-bottom: 18px;
}
.glass-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 22px;
    padding: 20px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.22);
    margin-bottom: 18px;
}
.risk-ring-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px 0 16px 0;
}
.risk-ring {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    position: relative;
}
.risk-ring::before {
    content: "";
    position: absolute;
    width: 128px;
    height: 128px;
    background: #0f172a;
    border-radius: 50%;
}
.risk-ring-content {
    position: relative;
    z-index: 2;
    text-align: center;
}
.risk-ring-score {
    font-size: 2rem;
    font-weight: 800;
    color: white;
}
.risk-ring-label {
    color: #cbd5e1;
    font-size: 0.9rem;
}
.progress-shell {
    width: 100%;
    height: 16px;
    background: rgba(255,255,255,0.10);
    border-radius: 999px;
    overflow: hidden;
    margin-top: 12px;
    margin-bottom: 10px;
}
.progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #22c55e, #f59e0b, #ef4444);
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

st.title("🔍 User Scanner")

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    user_url = st.text_input("Enter URL to scan", placeholder="https://example.com")
    scan_btn = st.button("🚀 Scan URL")
    st.markdown('</div>', unsafe_allow_html=True)

if scan_btn:
    if not user_url.strip():
        st.warning("Please enter a URL first.")
        st.stop()

    try:
        clean_url = normalize_url(user_url)

        remove_expired_blocks()
        is_blocked, blocked_until = is_url_currently_blocked(clean_url)

        if is_blocked:
            show_live_block_countdown(blocked_until)
            st.stop()

        result = predict_url(clean_url)
        prediction_label = result["prediction_label"]
        phishing_prob = result["phishing_probability"]
        legit_prob = result["legitimate_probability"]
        risk_score = result["risk_score"]
        severity = result["severity"]
        reasons = result["reasons"]
        features = result["features"]

        realtime = run_realtime_checks(clean_url)
        domain_live = realtime["domain_resolves"]
        status_code = realtime["http_status"]

        blacklisted = is_url_blacklisted(clean_url)
        if blacklisted:
            prediction_label = "Phishing"
            risk_score = max(risk_score, 95)
            severity = "High Risk"
            if "URL found in blacklist database" not in reasons:
                reasons.insert(0, "URL found in blacklist database")

        if risk_score >= 85:
            prediction_label = "Phishing"
            severity = "High Risk"
            if "Automatically blocked for 4 hours because risk score is above 85" not in reasons:
                reasons.insert(0, "Automatically blocked for 4 hours because risk score is above 85")

            block_url_for_24_hours(
                clean_url,
                risk_score,
                reason="Blocked automatically because risk score was 85 or higher"
            )

        save_scan_to_db(
            st.session_state.get("username", "unknown"),
            clean_url,
            prediction_label,
            risk_score,
            round(phishing_prob * 100, 2),
            round(legit_prob * 100, 2),
            severity,
            domain_live,
            status_code if status_code is not None else "N/A"
        )

        st.session_state.history.insert(0, {
            "url": clean_url,
            "prediction": prediction_label,
            "risk_score": risk_score,
            "severity": severity
        })

        st.session_state.latest_report_html = generate_html_report(
            clean_url,
            prediction_label,
            severity,
            risk_score,
            phishing_prob * 100,
            legit_prob * 100,
            reasons,
            features
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(f'<div class="metric-box metric-blue">Risk Score<br><h2>{risk_score}/100</h2></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-box metric-pink">Phishing Confidence<br><h2>{phishing_prob*100:.2f}%</h2></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-box metric-green">Legitimate Confidence<br><h2>{legit_prob*100:.2f}%</h2></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="metric-box metric-orange">Severity<br><h2>{severity}</h2></div>', unsafe_allow_html=True)

        st.write("")

        if prediction_label == "Phishing" or risk_score >= 60 or blacklisted:
            st.markdown('<div class="result-danger">⚠️ Final Result: PHISHING / SUSPICIOUS URL</div>', unsafe_allow_html=True)
        else:
            if risk_score >= 35:
                st.markdown('<div class="result-warn">⚠️ Final Result: Mostly safe, but some suspicious indicators are present.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="result-safe">✅ Final Result: LEGITIMATE / LOW RISK URL</div>', unsafe_allow_html=True)

        if risk_score >= 85:
            st.markdown("""
            <div class="result-danger">
                ⛔ This URL has been automatically blocked for 4 hours because the suspicious risk exceeded 85%.
            </div>
            """, unsafe_allow_html=True)

        left, right = st.columns([1.1, 1])

        with left:
            st.subheader("🎯 Animated Risk Meter")
            ring_fill = risk_score * 3.6
            ring_bg = f"conic-gradient(#22c55e 0deg, #f59e0b {ring_fill/2:.1f}deg, #ef4444 {ring_fill:.1f}deg, rgba(255,255,255,0.08) 0deg)"

            st.markdown(f"""
            <div class="glass-card">
                <div class="risk-ring-wrap">
                    <div class="risk-ring" style="background: {ring_bg};">
                        <div class="risk-ring-content">
                            <div class="risk-ring-score">{risk_score}</div>
                            <div class="risk-ring-label">Risk Meter</div>
                        </div>
                    </div>
                </div>
                <div class="progress-shell">
                    <div class="progress-fill" style="width:{risk_score}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.subheader("📌 Reasons")
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            if reasons:
                for reason in reasons:
                    st.write(f"- {reason}")
            else:
                st.write("- No strong suspicious indicators found")
            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            st.subheader("📊 Confidence Chart")
            fig, ax = plt.subplots(figsize=(5, 3.2))
            labels = ["Phishing", "Legitimate"]
            values = [phishing_prob * 100, legit_prob * 100]
            colors = ["#ef4444", "#22c55e"]
            bars = ax.bar(labels, values, color=colors)
            ax.set_ylim(0, 100)
            ax.set_ylabel("Confidence %")
            ax.set_title("AI Prediction Confidence")
            fig.patch.set_facecolor("#0f172a")
            ax.set_facecolor("#0f172a")
            ax.tick_params(colors="white")
            ax.yaxis.label.set_color("white")
            ax.title.set_color("white")
            for spine in ax.spines.values():
                spine.set_color("white")
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height + 2, f"{height:.1f}%", ha="center", color="white")
            st.pyplot(fig)

            st.subheader("🌐 Real-Time Checks")
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.write(f"- Domain resolves: {'Yes' if domain_live else 'No'}")
            st.write(f"- HTTP status code: {status_code if status_code is not None else 'Could not fetch'}")
            st.write(f"- Blacklisted: {'Yes' if blacklisted else 'No'}")
            st.markdown('</div>', unsafe_allow_html=True)

        st.subheader("🧠 Top Feature Summary")
        summary_df = pd.DataFrame([
            {"Feature": "URL Length", "Value": features["url_length"]},
            {"Feature": "Domain Length", "Value": features["domain_length"]},
            {"Feature": "Subdomain Count", "Value": features["subdomain_count"]},
            {"Feature": "Suspicious Word Count", "Value": features["suspicious_word_count"]},
            {"Feature": "Has HTTPS", "Value": features["has_https"]},
            {"Feature": "Uses IP Address", "Value": features["has_ip_address"]},
            {"Feature": "Shortened URL", "Value": features["is_shortened"]},
            {"Feature": "Brand Misuse", "Value": features["has_brand_misuse"]},
            {"Feature": "Digit Ratio", "Value": features["digit_ratio"]},
            {"Feature": "Special Char Ratio", "Value": features["special_char_ratio"]},
        ])
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

        if st.session_state.latest_report_html:
            st.download_button(
                label="📄 Download Latest Scan HTML Report",
                data=st.session_state.latest_report_html,
                file_name="latest_scan_report.html",
                mime="text/html"
            )

    except FileNotFoundError:
        st.error("Model files not found. Pehle run karo: py src\\preprocess.py && py src\\train_model.py")
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("""
<div class="fixed-footer">
    Developed By : Asit ❤️
</div>
""", unsafe_allow_html=True)