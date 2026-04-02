import streamlit as st
from datetime import date
from utils.db_queries import insert_expense
from utils.styles import get_styles, page_header, section_title

st.set_page_config(page_title="Log Daily Expense", layout="centered", page_icon="📝")

# ---------------- SESSION CHECK ----------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()

user_id = st.session_state.user_id

# ---------------- UI ----------------
st.markdown(get_styles(), unsafe_allow_html=True)
st.markdown(page_header("📝 Log Daily Expense", "Track your spending to power accurate AI predictions"), unsafe_allow_html=True)

CATEGORY_ICONS = {
    "Groceries": "🛒", "Rent": "🏠", "Utilities": "💡",
    "Travel": "✈️", "Education": "📚", "Entertainment": "🎬",
    "Healthcare": "🏥", "Others": "📦"
}

st.markdown(section_title("➕ Add New Expense"), unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    expense_date = st.date_input("📅 Expense Date", value=date.today(), max_value=date.today())
    category = st.selectbox("📂 Category", list(CATEGORY_ICONS.keys()),
                           format_func=lambda x: f"{CATEGORY_ICONS[x]} {x}")

with col2:
    product_name = st.text_input("🏷️ Product / Description", placeholder="e.g. Grocery shopping")
    amount = st.number_input("💵 Amount (₹)", min_value=0.0, step=10.0)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- SAVE BUTTON ----------------
if st.button("💾 Save Expense", use_container_width=True):

    if not product_name:
        st.error("⚠️ Please enter a product name.")
        st.stop()

    if amount <= 0:
        st.error("⚠️ Enter amount greater than ₹0.")
        st.stop()

    # ✅ Insert into DB
    insert_expense(user_id, str(expense_date), product_name, category, amount)

    # ✅ Success message
    st.success(f"₹{amount:,.2f} added successfully!")

    # ✅ FORCE REFRESH (CRITICAL FIX)
    st.session_state["refresh_trigger"] = True
    st.rerun()

# ---------------- NAVIGATION ----------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(section_title("🔗 Quick Navigation"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/2_Home.py")

with col2:
    if st.button("📊 Analytics", use_container_width=True):
        st.switch_page("pages/4_Analytics.py")

with col3:
    if st.button("🔍 Prediction", use_container_width=True):
        st.switch_page("pages/3_Prediction.py")