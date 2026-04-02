import streamlit as st
from datetime import date
from utils.db import get_connection
from utils.styles import get_styles, page_header, metric_card, status_badge, section_title
import plotly.graph_objects as go

st.set_page_config(page_title="Home Dashboard", layout="wide", page_icon="💹")

st.markdown("""
<style>
[data-testid="stHeader"]  { background-color: #faecd8 !important; }
[data-testid="stToolbar"] { display: none !important; }
section[data-testid="stSidebarNav"] { display: none !important; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], .main { background-color: #fdf8f0 !important; }

.section-title {
    font-weight: 700;
    color: #a07850;
    margin-top: 20px;
    margin-bottom: 10px;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

# refresh trigger
if st.session_state.get("refresh_trigger"):
    st.session_state["refresh_trigger"] = False

user_id = st.session_state.get("user_id")
st.markdown(get_styles(), unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(page_header("📊 Financial Dashboard", "Your real-time budget health overview"), unsafe_allow_html=True)

# ---------------- DB ----------------
today = date.today()
conn = get_connection()
cursor = conn.cursor()

month = today.month
year = today.year

cursor.execute(
    "SELECT income, budget FROM user_monthly_financials WHERE user_id=? AND month=? AND year=?",
    (user_id, month, year)
)
data = cursor.fetchone()
income, budget = data if data else (0, 0)

cursor.execute(
    """SELECT SUM(amount) FROM user_expenses
       WHERE user_id=? AND strftime('%m',expense_date)=? AND strftime('%Y',expense_date)=?""",
    (user_id, str(month).zfill(2), str(year))
)
spent = cursor.fetchone()[0] or 0
conn.close()

# ---------------- CALCULATIONS ----------------
remaining = budget - spent
utilization = (spent / budget * 100) if budget > 0 else 0
health_score = max(0, 100 - utilization)

# ---------------- TITLE ----------------
st.markdown("<div class='section-title'>💡 BUDGET HEALTH OVERVIEW</div>", unsafe_allow_html=True)

# ---------------- METRICS ----------------
col1, col2, col3, col4 = st.columns(4)

col1.markdown(metric_card("Monthly Budget", f"₹{budget:,.0f}", "💰", "#c97b4b", "rgba(201,123,75,0.08)"), unsafe_allow_html=True)
col2.markdown(metric_card("Total Spent", f"₹{spent:,.0f}", "💸", "#e8a87c", "rgba(232,168,124,0.08)"), unsafe_allow_html=True)
col3.markdown(metric_card("Remaining", f"₹{remaining:,.0f}", "🏦", "#3a6e37", "rgba(104,163,100,0.08)"), unsafe_allow_html=True)
col4.markdown(metric_card("Health Score", f"{health_score:.0f}/100", "❤️", "#3a6e37", "rgba(104,163,100,0.08)"), unsafe_allow_html=True)

# ---------------- STATUS ----------------
if health_score >= 80:
    st.markdown(status_badge("🟢 Budget Status: Good — Your spending is well within the budget.", "#3a6e37", "rgba(104,163,100,0.1)"), unsafe_allow_html=True)
elif health_score >= 50:
    st.markdown(status_badge("🟡 Budget Status: Moderate — Monitor your spending.", "#8a5c1a", "rgba(210,153,80,0.1)"), unsafe_allow_html=True)
else:
    st.markdown(status_badge("🔴 Budget Risk — Overspending alert!", "#9b3030", "rgba(200,80,80,0.1)"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- MAIN LAYOUT ----------------
left, right = st.columns([2, 1])

# ---------------- GAUGE ----------------
with left:
    st.markdown("<div class='section-title'>📊 BUDGET UTILIZATION GAUGE</div>", unsafe_allow_html=True)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=utilization,
        number={"suffix": "%"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#c97b4b"},
            "steps": [
                {"range": [0, 60], "color": "rgba(104,163,100,0.2)"},
                {"range": [60, 85], "color": "rgba(210,153,80,0.2)"},
                {"range": [85, 100], "color": "rgba(200,80,80,0.2)"}
            ],
            "threshold": {"value": 85}
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

# ---------------- RIGHT PANEL ----------------
with right:
    st.markdown("<div class='section-title'>📅 DAILY SPENDING</div>", unsafe_allow_html=True)

    selected_date = st.date_input("Date", value=today)

    conn2 = get_connection()
    cursor2 = conn2.cursor()
    cursor2.execute(
        "SELECT SUM(amount) FROM user_expenses WHERE user_id=? AND expense_date=?",
        (user_id, str(selected_date))
    )
    daily = cursor2.fetchone()[0] or 0
    conn2.close()

    st.markdown(metric_card("Spent on this Date", f"₹{daily:,.2f}", "📅", "#c97b4b", "rgba(201,123,75,0.08)"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>⚡ QUICK ACTIONS</div>", unsafe_allow_html=True)

    if st.button("➕ Log Expense", width="stretch"):
        st.switch_page("pages/Log_Daily_Expense.py")

    if st.button("🔍 Check Purchase", width="stretch"):
        st.switch_page("pages/3_Prediction.py")

    if st.button("📈 View Analytics", width="stretch"):
        st.switch_page("pages/4_Analytics.py")