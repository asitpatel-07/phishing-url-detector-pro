import os
import json
import random
import streamlit as st

from auth.password_utils import verify_password

USERS_FILE = os.path.join("auth", "users.json")


def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def authenticate(username, password):
    users = load_users()
    for user in users:
        if user["username"] == username and verify_password(password, user["password_hash"]):
            return {
                "username": user["username"],
                "role": user["role"]
            }
    return None


def generate_user_challenge():
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    op = random.choice(["+", "-", "*"])

    if op == "+":
        answer = a + b
        question = f"{a} + {b}"
    elif op == "-":
        if a < b:
            a, b = b, a
        answer = a - b
        question = f"{a} - {b}"
    else:
        answer = a * b
        question = f"{a} × {b}"

    st.session_state.user_challenge_question = question
    st.session_state.user_challenge_answer = answer


def show_login():
    if "show_user_credentials" not in st.session_state:
        st.session_state.show_user_credentials = False

    if "user_challenge_question" not in st.session_state or "user_challenge_answer" not in st.session_state:
        generate_user_challenge()

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(37,99,235,0.20), rgba(168,85,247,0.18), rgba(236,72,153,0.14));
        border-radius: 22px;
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.08);
    ">
        <h2 style="color:white; margin:0;">🔐 Login Required</h2>
        <p style="color:#dbeafe; margin-top:8px;">
            Please login to access the Advanced AI Phishing URL Detection System.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 18px;
    ">
        <h3 style="color:white; margin-top:0;">👤 User Access Challenge</h3>
        <p style="color:#cbd5e1; margin-bottom:8px;">
            User username and password will be visible only when you solve the math challenge given below.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("user_challenge_form"):
        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 10px;
            color: white;
            font-weight: 700;
            font-size: 1.1rem;
        ">
            Solve this: {st.session_state.user_challenge_question}
        </div>
        """, unsafe_allow_html=True)

        challenge_answer = st.text_input("Enter Answer")
        solve_btn = st.form_submit_button("Solve to Reveal User Credentials")

        if solve_btn:
            try:
                if int(challenge_answer.strip()) == st.session_state.user_challenge_answer:
                    st.session_state.show_user_credentials = True
                    st.success("Correct answer! User credentials revealed below.")
                else:
                    st.session_state.show_user_credentials = False
                    st.error("Wrong answer. Solve correctly to see user credentials.")
                    generate_user_challenge()
                    st.rerun()
            except ValueError:
                st.error("Please enter a valid number.")

    if st.session_state.show_user_credentials:
        st.markdown("""
        <div style="
            background: rgba(34,197,94,0.12);
            border: 1px solid rgba(34,197,94,0.35);
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 18px;
            color: #dcfce7;
            font-weight: 700;
        ">
            User Credentials:<br>
            Username: <b>user</b><br>
            Password: <b>user</b>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 18px;
    ">
        <h3 style="color:white; margin-top:0;">🔑 Login Form</h3>
        <p style="color:#cbd5e1;">
            Admin aur User dono yahan se login kar sakte hain.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

        if login_btn:
            user = authenticate(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = user["username"]
                st.session_state.role = user["role"]
                st.success(f"Welcome, {user['username']}!")
                st.rerun()
            else:
                st.error("Invalid username or password")


def require_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        show_login()
        st.stop()


def logout_button():
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()