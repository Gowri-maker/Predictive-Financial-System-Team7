# app.py
import streamlit as st
import re
from utils.db import create_tables
from utils.auth import register_user, login_user, reset_password

create_tables()

st.set_page_config(page_title="Predictive Financial System", layout="centered", page_icon="💹")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }

[data-testid="stHeader"]  { background-color: #faecd8 !important; border-bottom: 1px solid rgba(201,123,75,0.2) !important; }
[data-testid="stToolbar"] { display: none !important; }
section[data-testid="stSidebarNav"] { display: none !important; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f5e0c4 0%, #faecd8 100%) !important;
    border-right: 1px solid rgba(201,123,75,0.2) !important;
}
section[data-testid="stSidebar"] * { color: #3d2b1f !important; }

#MainMenu, footer, header { visibility: hidden; }

.stApp {
    background: linear-gradient(135deg, #fdf8f0 0%, #faecd8 50%, #f5e0c4 100%);
}
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], .main { background-color: #fdf8f0 !important; }

.block-container { padding-top: 2rem !important; max-width: 500px !important; }

input {
    color: #3d2b1f !important;
    caret-color: #c97b4b !important;
    background: #fff8f2 !important;
}

.stTextInput > div > div > input {
    background: #fff8f2 !important;
    border: 1.5px solid rgba(201,123,75,0.4) !important;
    border-radius: 10px !important;
    color: #3d2b1f !important;
    font-size: 14px !important;
    padding: 12px 14px !important;
    caret-color: #c97b4b !important;
}
.stTextInput > div > div > input:focus {
    border-color: #c97b4b !important;
    box-shadow: 0 0 0 3px rgba(201,123,75,0.15) !important;
    color: #3d2b1f !important;
    background: #ffffff !important;
}
.stTextInput > div > div > input::placeholder {
    color: #a07850 !important;
    opacity: 1 !important;
}

.stTextInput label, .stRadio label, .stRadio > div > label {
    color: #a07850 !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

.stRadio > div {
    display: flex !important;
    gap: 4px !important;
    background: rgba(201,123,75,0.06) !important;
    border: 1px solid rgba(201,123,75,0.2) !important;
    border-radius: 12px !important;
    padding: 5px !important;
}
.stRadio > div > label {
    flex: 1 !important;
    text-align: center !important;
    padding: 8px 4px !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #a07850 !important;
}
[data-baseweb="radio"] > div:first-child { display: none !important; }

.stButton > button {
    background: linear-gradient(135deg, #e8a87c, #c97b4b) !important;
    color: #fff8f2 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    width: 100% !important;
    box-shadow: 0 4px 15px rgba(201,123,75,0.3) !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(201,123,75,0.5) !important;
}

.stSuccess { background: rgba(104,163,100,0.1) !important; border: 1px solid rgba(104,163,100,0.3) !important; border-radius: 10px !important; }

/* ===== PASSWORD EYE BUTTON ===== */
button[data-testid="baseButton-secondary"],
.stTextInput button,
[data-testid="stTextInputRootElement"] button {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #7c4a2d !important;
}
[data-testid="stTextInputRootElement"] button:hover {
    background-color: rgba(201,123,75,0.1) !important;
}
[data-testid="stTextInputRootElement"] button svg {
    fill: #7c4a2d !important;
    color: #7c4a2d !important;
}

.stError   { background: rgba(200,80,80,0.1) !important;  border: 1px solid rgba(200,80,80,0.3) !important;  border-radius: 10px !important; }

p, span, div { color: #3d2b1f; }
</style>
""", unsafe_allow_html=True)

# -------- HERO --------
st.markdown("""
<div style="text-align:center; padding:32px 0 24px 0;">
    <div style="font-size:52px; margin-bottom:12px;">💹</div>
    <h1 style="
        font-family:'Syne',sans-serif; font-size:32px; font-weight:800;
        letter-spacing:-1px; margin:0 0 6px 0;
        background:linear-gradient(135deg,#c97b4b,#7c4a2d);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    ">Predictive Financial System</h1>
</div>

<div style="padding:0 8px;">
""", unsafe_allow_html=True)

menu = st.radio("Navigation", ["Login", "Register", "Forgot Password"],
                horizontal=True, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

# -------- LOGIN --------
if menu == "Login":
    st.markdown("<p style='color:#a07850;font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;'>Email or Phone</p>", unsafe_allow_html=True)
    identifier = st.text_input("id", placeholder="you@email.com or 9876543210", label_visibility="collapsed", key="login_id")

    st.markdown("<p style='color:#a07850;font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;'>Password</p>", unsafe_allow_html=True)
    password = st.text_input("pw", type="password", placeholder="Enter your password", label_visibility="collapsed", key="login_pw")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔐 Login"):
        if not identifier or not password:
            st.error("Please enter Email/Phone and Password")
        else:
            user = login_user(identifier, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.session_state.is_setup_complete = user[1]
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")

# -------- REGISTER --------
elif menu == "Register":
    st.markdown("<p style='color:#a07850;font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;'>Email or Phone</p>", unsafe_allow_html=True)
    identifier = st.text_input("id", placeholder="you@email.com or 9876543210", label_visibility="collapsed", key="reg_id")

    st.markdown("<p style='color:#a07850;font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;'>Password</p>", unsafe_allow_html=True)
    password = st.text_input("pw", type="password", placeholder="Min 6 characters", label_visibility="collapsed", key="reg_pw")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✨ Create Account"):
        if not identifier or not password:
            st.error("Please fill all fields")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters")
        elif "@" in identifier:
            if not is_valid_email(identifier):
                st.error("Please enter a valid email address")
            else:
                if register_user(identifier, identifier, password):
                    st.success("🎉 Account created! Please login.")
                else:
                    st.error("Email already exists.")
        else:
            if not is_valid_phone(identifier):
                st.error("Please enter a valid 10-digit phone number")
            else:
                if register_user(identifier, identifier, password):
                    st.success("🎉 Account created! Please login.")
                else:
                    st.error("Phone number already exists.")

# -------- FORGOT PASSWORD --------
elif menu == "Forgot Password":
    st.markdown("<p style='color:#a07850;font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;'>Email or Phone</p>", unsafe_allow_html=True)
    identifier = st.text_input("id", placeholder="you@email.com or 9876543210", label_visibility="collapsed", key="fp_id")

    st.markdown("<p style='color:#a07850;font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;'>New Password</p>", unsafe_allow_html=True)
    new_password = st.text_input("pw", type="password", placeholder="Min 6 characters", label_visibility="collapsed", key="fp_pw")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Reset Password"):
        if not identifier or not new_password:
            st.error("Please enter Email/Phone and New Password")
        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters")
        else:
            reset_password(identifier, new_password)
            st.success("✅ Password updated! Please login.")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;margin-top:24px;">
    <p style="color:#c4a882;font-size:12px;">Powered by CatBoost · Prophet · SHAP</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.logged_in:
    if st.session_state.is_setup_complete == 0:
        st.switch_page("pages/1_Setup.py")
    else:
        st.switch_page("pages/2_Home.py")