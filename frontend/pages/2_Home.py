# 2_Home.py
import streamlit as st
from datetime import date
from utils.db import get_connection
from utils.styles import get_styles, page_header, metric_card, status_badge, section_title
import plotly.graph_objects as go

st.set_page_config(page_title="Home Dashboard", layout="wide", page_icon="💹")

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

    input, .stDateInput input {
        background-color: #fff8f2 !important;
        color: #3d2b1f !important;
        border: 1px solid rgba(201,123,75,0.35) !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

user_id = st.session_state.get("user_id")
st.markdown(get_styles(), unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div style='padding:10px 0 20px 0;'></div>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.switch_page("app.py")

st.markdown(page_header("📊 Financial Dashboard", "Your real-time budget health overview"), unsafe_allow_html=True)

today  = date.today()
conn   = get_connection()
cursor = conn.cursor()

current_month = today.month
current_year  = today.year

cursor.execute(
    "SELECT income, budget FROM user_monthly_financials WHERE user_id=? AND month=? AND year=?",
    (user_id, current_month, current_year)
)
monthly_data = cursor.fetchone()
monthly_income, monthly_budget = monthly_data if monthly_data else (0, 0)

cursor.execute(
    """SELECT SUM(amount) FROM user_expenses
    WHERE user_id=? AND strftime('%m',expense_date)=? AND strftime('%Y',expense_date)=?""",
    (user_id, str(current_month).zfill(2), str(current_year))
)
monthly_spent = cursor.fetchone()[0] or 0
conn.close()

remaining_budget    = monthly_budget - monthly_spent
budget_utilization  = (monthly_spent / monthly_budget * 100) if monthly_budget > 0 else 0
budget_health_score = max(0, 100 - budget_utilization)

st.markdown(section_title("💡 Budget Health Overview"), unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(metric_card("Monthly Budget", f"₹{monthly_budget:,.0f}",   "💰", "#c97b4b", "rgba(201,123,75,0.08)"), unsafe_allow_html=True)
with col2:
    st.markdown(metric_card("Total Spent",    f"₹{monthly_spent:,.0f}",    "💸", "#e8a87c", "rgba(232,168,124,0.08)"), unsafe_allow_html=True)
with col3:
    r_color = "#3a6e37" if remaining_budget >= 0 else "#9b3030"
    r_bg    = "rgba(104,163,100,0.08)" if remaining_budget >= 0 else "rgba(200,80,80,0.08)"
    st.markdown(metric_card("Remaining",      f"₹{remaining_budget:,.0f}", "🏦", r_color, r_bg), unsafe_allow_html=True)
with col4:
    h_color = "#3a6e37" if budget_health_score >= 80 else "#8a5c1a" if budget_health_score >= 50 else "#9b3030"
    h_bg    = "rgba(104,163,100,0.08)" if budget_health_score >= 80 else "rgba(210,153,80,0.08)" if budget_health_score >= 50 else "rgba(200,80,80,0.08)"
    st.markdown(metric_card("Health Score",   f"{budget_health_score:.0f}/100", "❤️", h_color, h_bg), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if budget_health_score >= 80:
    st.markdown(status_badge("🟢  Budget Status: Good — Your spending is well within the budget.", "#3a6e37", "rgba(104,163,100,0.1)"), unsafe_allow_html=True)
elif budget_health_score >= 50:
    st.markdown(status_badge("🟡  Budget Status: Moderate — Monitor your spending carefully.", "#8a5c1a", "rgba(210,153,80,0.1)"), unsafe_allow_html=True)
else:
    st.markdown(status_badge("🔴  Budget Status: Risk — You are close to exceeding your budget!", "#9b3030", "rgba(200,80,80,0.1)"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([2, 1])

with left:
    st.markdown(section_title("📊 Budget Utilization Gauge"), unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=budget_utilization,
        number={"suffix": "%", "font": {"color": "#3d2b1f", "size": 32}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#a07850", "tickfont": {"color": "#a07850"}},
            "bar": {"color": "#c97b4b", "thickness": 0.25},
            "bgcolor": "rgba(253,248,240,0.5)", "borderwidth": 0,
            "steps": [
                {"range": [0,  60], "color": "rgba(104,163,100,0.2)"},
                {"range": [60, 85], "color": "rgba(210,153,80,0.2)"},
                {"range": [85,100], "color": "rgba(200,80,80,0.2)"},
            ],
            "threshold": {"line": {"color": "#9b3030", "width": 3}, "thickness": 0.75, "value": 85}
        },
        title={"text": "Budget Utilized", "font": {"color": "#a07850", "size": 13}}
    ))
    fig_gauge.update_layout(
        height=260, paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#3d2b1f"}, margin=dict(t=40, b=10, l=30, r=30)
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

with right:
    st.markdown(section_title("📅 Daily Spending"), unsafe_allow_html=True)
    if "selected_date" not in st.session_state:
        st.session_state.selected_date = today
    selected_date = st.date_input("Date", value=st.session_state.selected_date,
                                  max_value=today, label_visibility="collapsed")
    st.session_state.selected_date = selected_date

    conn2   = get_connection()
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT SUM(amount) FROM user_expenses WHERE user_id=? AND expense_date=?",
                    (user_id, str(selected_date)))
    daily_spent = cursor2.fetchone()[0] or 0
    conn2.close()

    st.markdown(metric_card("Spent on this Date", f"₹{daily_spent:,.2f}", "🗓️", "#c97b4b", "rgba(201,123,75,0.08)"), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(section_title("⚡ Quick Actions"), unsafe_allow_html=True)

    if st.button("➕ Log Expense",    use_container_width=True):
        st.switch_page("pages/Log_Daily_Expense.py")
    if st.button("🔍 Check Purchase", use_container_width=True):
        st.switch_page("pages/3_Prediction.py")
    if st.button("📈 View Analytics", use_container_width=True):
        st.switch_page("pages/4_Analytics.py")