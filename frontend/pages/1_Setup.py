# 1_Setup.py
import streamlit as st
from utils.db import get_connection
from utils.styles import get_styles, page_header, section_title, sidebar_html
from datetime import datetime

st.set_page_config(page_title="Monthly Financial Setup", layout="wide", page_icon="⚙️")

st.markdown("""
<style>
    [data-testid="stHeader"]  { background-color: #faecd8 !important; border-bottom: 1px solid rgba(201,123,75,0.2) !important; }
    [data-testid="stToolbar"] { display: none !important; }
    section[data-testid="stSidebarNav"] { display: none !important; }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f5e0c4 0%, #faecd8 100%) !important;
        border-right: 1px solid rgba(201,123,75,0.2) !important;
    }
    section[data-testid="stSidebar"] * { color: #3d2b1f !important; }
    html, body, [data-testid="stAppViewContainer"],
    [data-testid="stApp"], .main { background-color: #fdf8f0 !important; }
    [data-testid="stAppViewContainer"] > section { animation: fadeIn 0.15s ease-in; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

    /* ── ALL select/input containers ── */
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] > div > div,
    div[data-baseweb="select"] > div > div > div,
    div[data-baseweb="input"],
    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"],
    div[data-baseweb="base-input"] > div {
        background-color: #fff8f2 !important;
        color: #3d2b1f !important;
    }

    div[data-baseweb="select"] > div {
        border: 1px solid rgba(201,123,75,0.4) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    div[data-baseweb="tag"] {
        background-color: rgba(201,123,75,0.15) !important;
        border: 1px solid rgba(201,123,75,0.3) !important;
    }
    div[data-baseweb="tag"] span { color: #7c4a2d !important; }

    ul[data-testid="stMultiSelectDropdown"],
    div[role="listbox"],
    li[role="option"] {
        background-color: #fff8f2 !important;
        color: #3d2b1f !important;
    }
    li[role="option"]:hover {
        background-color: rgba(201,123,75,0.12) !important;
    }

    div[data-baseweb="select"] svg {
        fill: #a07850 !important;
        color: #a07850 !important;
    }

    input, .stNumberInput input {
        background-color: #fff8f2 !important;
        color: #3d2b1f !important;
        border: 1px solid rgba(201,123,75,0.35) !important;
        border-radius: 10px !important;
        caret-color: #c97b4b !important;
    }
    .stNumberInput input:focus {
        border-color: #c97b4b !important;
        box-shadow: 0 0 0 3px rgba(201,123,75,0.15) !important;
    }

    input::placeholder { color: #a07850 !important; opacity: 1 !important; }

    hr { display: none !important; visibility: hidden !important; }

    div[data-baseweb="select"] * {
        border: none !important;
        box-shadow: none !important;
    }
    div[data-baseweb="select"] > div > div {
        background-color: #fff8f2 !important;
    }
    div[data-baseweb="select"] input {
        background-color: transparent !important;
    }
    div[data-baseweb="select"] > div {
        display: flex !important;
        align-items: center !important;
        border: 1px solid rgba(201,123,75,0.35) !important;
        border-radius: 10px !important;
        min-height: 45px !important;
        height: auto !important;
        padding: 6px !important;
        flex-wrap: wrap !important;
    }
    div[data-baseweb="select"]:hover { border-color: #c97b4b !important; }
    div[role="listbox"] hr { display: none !important; }
    div[data-baseweb="tag"] {
        display: flex !important;
        align-items: center !important;
        height: auto !important;
        padding: 4px 8px !important;
    }
    div[data-baseweb="select"] { overflow: visible !important; }

    /* Labels */
    label, .stSelectbox label, .stMultiSelect label, .stNumberInput label {
        color: #a07850 !important;
        font-size: 13px !important;
    }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()

st.markdown(get_styles(), unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div style='padding:10px 0 20px 0;'></div>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.switch_page("app.py")

now    = datetime.now()
months = ["January","February","March","April","May","June",
          "July","August","September","October","November","December"]

st.markdown(page_header(
    "⚙️ Monthly Financial Setup",
    f"{months[now.month - 1]} {now.year} — Set your income, budget and category priorities"
), unsafe_allow_html=True)

current_month = now.month
current_year  = now.year

conn   = get_connection()
cursor = conn.cursor()

cursor.execute(
    "SELECT income, budget, expected_expenditure FROM user_monthly_financials WHERE user_id=? AND month=? AND year=?",
    (st.session_state.user_id, current_month, current_year)
)
record = cursor.fetchone()
income_default, budget_default, exp_default = record if record else (0.0, 0.0, 0.0)

st.markdown(section_title("💰 Monthly Financials"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    income = st.number_input("💼 Monthly Income (₹)", value=float(income_default), step=1000.0)
with col2:
    budget = st.number_input("💰 Monthly Budget (₹)", value=float(budget_default), step=1000.0)
with col3:
    expected_expenditure = st.number_input("📊 Expected Expenditure (₹)", value=float(exp_default), step=1000.0)

if income > 0 and budget > 0:
    savings_preview = income - budget
    savings_pct     = (savings_preview / income) * 100
    color = "#3a6e37" if savings_pct >= 20 else "#8a5c1a" if savings_pct >= 10 else "#9b3030"
    st.markdown(f"""
    <div style="background:rgba(201,123,75,0.06);border:1px solid rgba(201,123,75,0.2);
        border-radius:10px;padding:12px 16px;margin-top:8px;font-size:13px;color:{color};">
        💡 Estimated Monthly Savings: <b>₹{savings_preview:,.0f}</b> ({savings_pct:.1f}% of income)
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(section_title("📂 Category Priorities"), unsafe_allow_html=True)

st.markdown("""
<div style="background:rgba(201,123,75,0.06);border:1px solid rgba(201,123,75,0.15);
    border-radius:10px;padding:12px 16px;font-size:13px;color:#a07850;margin-bottom:16px;">
    📌 Select categories you spend in and assign priority levels (1 = Highest, 5 = Lowest).
    This helps the AI make smarter purchase recommendations.
</div>
""", unsafe_allow_html=True)

category_list  = ["Groceries", "Rent", "Utilities", "Travel", "Education", "Entertainment", "Healthcare", "Others"]
CATEGORY_ICONS = {
    "Groceries": "🛒", "Rent": "🏠", "Utilities": "💡", "Travel": "✈️",
    "Education": "📚", "Entertainment": "🎬", "Healthcare": "🏥", "Others": "📦"
}

cursor.execute("SELECT category_name, priority_level FROM user_categories WHERE user_id=?",
               (st.session_state.user_id,))
existing_categories = {row[0]: row[1] for row in cursor.fetchall()}
valid_defaults = [c for c in existing_categories if c in category_list]

selected_categories = st.multiselect(
    "Select Your Spending Categories", category_list,
    default=valid_defaults, format_func=lambda x: f"{CATEGORY_ICONS[x]} {x}"
)

priority_inputs  = {}
priority_options = [1, 2, 3, 4, 5]
priority_labels  = {1: "🔴 Highest", 2: "🟠 High", 3: "🟡 Medium", 4: "🟢 Low", 5: "⚪ Lowest"}

if selected_categories:
    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, category in enumerate(selected_categories):
        default_priority = existing_categories.get(category, 3)
        if default_priority not in priority_options:
            default_priority = 3
        with cols[i % 2]:
            priority = st.selectbox(
                f"{CATEGORY_ICONS[category]} {category}", priority_options,
                index=priority_options.index(default_priority),
                format_func=lambda x: priority_labels[x],
                key=f"priority_{category}"
            )
            priority_inputs[category] = priority

st.markdown("<br>", unsafe_allow_html=True)

if st.button("💾 Save / Update Setup", use_container_width=True):
    if record:
        cursor.execute(
            "UPDATE user_monthly_financials SET income=?, budget=?, expected_expenditure=? WHERE user_id=? AND month=? AND year=?",
            (income, budget, expected_expenditure, st.session_state.user_id, current_month, current_year)
        )
    else:
        cursor.execute(
            "INSERT INTO user_monthly_financials (user_id, month, year, income, budget, expected_expenditure) VALUES (?,?,?,?,?,?)",
            (st.session_state.user_id, current_month, current_year, income, budget, expected_expenditure)
        )
    for category, priority in priority_inputs.items():
        cursor.execute("SELECT id FROM user_categories WHERE user_id=? AND category_name=?",
                       (st.session_state.user_id, category))
        if cursor.fetchone():
            cursor.execute("UPDATE user_categories SET priority_level=? WHERE user_id=? AND category_name=?",
                           (priority, st.session_state.user_id, category))
        else:
            cursor.execute("INSERT INTO user_categories (user_id, category_name, priority_level) VALUES (?,?,?)",
                           (st.session_state.user_id, category, priority))
    for existing_category in existing_categories:
        if existing_category not in selected_categories:
            cursor.execute("DELETE FROM user_categories WHERE user_id=? AND category_name=?",
                           (st.session_state.user_id, existing_category))
    conn.commit()
    st.markdown("""
    <div style="background:rgba(104,163,100,0.1);border:1px solid rgba(104,163,100,0.3);
        border-radius:12px;padding:16px 20px;display:flex;align-items:center;gap:12px;margin-top:8px;">
        <span style="font-size:28px;">✅</span>
        <div style="font-size:15px;font-weight:600;color:#3a6e37;">Setup updated successfully!</div>
    </div>
    """, unsafe_allow_html=True)

conn.close()