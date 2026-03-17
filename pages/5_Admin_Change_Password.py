import os
import sys
import json
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.login import require_login
from auth.password_utils import hash_password, verify_password

USERS_FILE = os.path.join("auth", "users.json")

st.set_page_config(page_title="Admin Change Password", page_icon="🔐", layout="wide")
require_login()

if st.session_state.get("role") != "admin":
    st.error("Access denied. Admin only page.")
    st.stop()

st.title("🔐 Admin Change Password")

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def change_admin_password(username, old_password, new_password):
    users = load_users()

    for user in users:
        if user["username"] == username and user["role"] == "admin":
            if not verify_password(old_password, user["password_hash"]):
                return False, "Old password is incorrect."

            user["password_hash"] = hash_password(new_password)
            save_users(users)
            return True, "Admin password changed successfully."

    return False, "Admin user not found."

st.markdown("""
<div style="
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;
">
    <h3 style="color:white; margin-top:0;">Change Admin Password</h3>
    <p style="color:#cbd5e1;">
        Password tabhi change hoga jab old password sahi hoga.
    </p>
</div>
""", unsafe_allow_html=True)

with st.form("change_password_form"):
    username = st.text_input("Admin Username", value=st.session_state.get("username", "admin"))
    old_password = st.text_input("Old Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    submit_btn = st.form_submit_button("Change Password")

if submit_btn:
    if not old_password or not new_password or not confirm_password:
        st.warning("Please fill all fields.")
    elif new_password != confirm_password:
        st.error("New password and confirm password do not match.")
    elif len(new_password) < 6:
        st.error("New password must be at least 6 characters long.")
    else:
        success, message = change_admin_password(username, old_password, new_password)
        if success:
            st.success(message)
            st.info("Next login se new password use karna.")
        else:
            st.error(message)