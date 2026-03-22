# styles.py — frontend/utils/styles.py
# Warm Sand palette

def get_styles():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    /* ===== GLOBAL ===== */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
        color: #3d2b1f !important;
    }

    .stApp {
        background: linear-gradient(135deg, #fdf8f0 0%, #faecd8 50%, #f5e0c4 100%) !important;
    }

    html, body, [data-testid="stAppViewContainer"],
    [data-testid="stApp"], .main {
        background-color: #fdf8f0 !important;
    }

    /* ===== HIDE DEFAULT TOP SIDEBAR NAV ===== */
    section[data-testid="stSidebarNav"] { display: none !important; }
    [data-testid="stHeader"] {
        background-color: #faecd8 !important;
        border-bottom: 1px solid rgba(201,123,75,0.2) !important;
    }
    [data-testid="stToolbar"] { display: none !important; }

    /* ===== HIDE STREAMLIT DEFAULTS ===== */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f5e0c4 0%, #faecd8 100%) !important;
        border-right: 1px solid rgba(201,123,75,0.2) !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] div {
        color: #3d2b1f !important;
    }

    /* ===== TEXT INPUT ===== */
    .stTextInput > div > div > input {
        background: #fff8f2 !important;
        border: 1px solid rgba(201,123,75,0.35) !important;
        border-radius: 10px !important;
        color: #3d2b1f !important;
        font-size: 14px !important;
        caret-color: #c97b4b !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #c97b4b !important;
        box-shadow: 0 0 0 3px rgba(201,123,75,0.15) !important;
        color: #3d2b1f !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #a07850 !important;
        opacity: 1 !important;
    }

    /* ===== NUMBER INPUT ===== */
    .stNumberInput > div > div > input {
        background: #fff8f2 !important;
        border: 1px solid rgba(201,123,75,0.35) !important;
        border-radius: 10px !important;
        color: #3d2b1f !important;
        font-size: 14px !important;
        caret-color: #c97b4b !important;
    }
    .stNumberInput > div > div > input:focus {
        border-color: #c97b4b !important;
        color: #3d2b1f !important;
    }


    /* ===== NUMBER INPUT + - BUTTONS ===== */
    .stNumberInput button,
    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        background-color: #f5e0c4 !important;
        border: 1px solid rgba(201,123,75,0.35) !important;
        color: #7c4a2d !important;
    }
    .stNumberInput button:hover,
    button[data-testid="stNumberInputStepDown"]:hover,
    button[data-testid="stNumberInputStepUp"]:hover {
        background-color: #e8c9a8 !important;
        color: #5c3520 !important;
    }

    /* ===== DATE INPUT ===== */
    .stDateInput > div > div > input {
        background: #fff8f2 !important;
        border: 1px solid rgba(201,123,75,0.35) !important;
        border-radius: 10px !important;
        color: #3d2b1f !important;
        font-size: 14px !important;
    }

    /* ===== SELECTBOX ===== */
    .stSelectbox > div > div {
        background: #fff8f2 !important;
        border: 1px solid rgba(201,123,75,0.35) !important;
        border-radius: 10px !important;
        color: #3d2b1f !important;
    }
    .stSelectbox > div > div > div { color: #3d2b1f !important; }
    .stSelectbox span { color: #3d2b1f !important; }
    .stSelectbox svg { fill: #a07850 !important; }

    /* ===== MULTISELECT ===== */
    .stMultiSelect > div > div {
        background: #fff8f2 !important;
        border: 1px solid rgba(201,123,75,0.35) !important;
        border-radius: 10px !important;
        color: #3d2b1f !important;
    }
    .stMultiSelect span { color: #3d2b1f !important; }
    .stMultiSelect [data-baseweb="tag"] {
        background: rgba(201,123,75,0.15) !important;
        border: 1px solid rgba(201,123,75,0.4) !important;
        border-radius: 6px !important;
    }
    .stMultiSelect [data-baseweb="tag"] span { color: #7c4a2d !important; }

    /* ===== DROPDOWN POPUP ===== */
    [data-baseweb="popover"],
    [data-baseweb="popover"] * {
        background: #fff8f2 !important;
        color: #3d2b1f !important;
    }
    [data-baseweb="menu"] {
        background: #fff8f2 !important;
        border: 1px solid rgba(201,123,75,0.2) !important;
    }
    [data-baseweb="option"] {
        background: #fff8f2 !important;
        color: #3d2b1f !important;
    }
    [data-baseweb="option"]:hover,
    [data-baseweb="option"][aria-selected="true"] {
        background: rgba(201,123,75,0.12) !important;
        color: #c97b4b !important;
    }

    /* ===== ALL LABELS ===== */
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stMultiSelect label,
    .stDateInput label,
    .stRadio label,
    .stCheckbox label {
        color: #a07850 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #e8a87c, #c97b4b) !important;
        color: #fff8f2 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(201,123,75,0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(201,123,75,0.5) !important;
    }

    /* ===== RADIO ===== */
    .stRadio > div { gap: 4px !important; }
    .stRadio > div > label { color: #a07850 !important; }

    /* ===== DIVIDER ===== */
    hr { border-color: rgba(201,123,75,0.15) !important; }

    /* ===== ALERTS ===== */
    .stSuccess {
        background: rgba(104,163,100,0.1) !important;
        border: 1px solid rgba(104,163,100,0.3) !important;
        border-radius: 10px !important;
        color: #3a6e37 !important;
    }
    .stWarning {
        background: rgba(210,153,80,0.1) !important;
        border: 1px solid rgba(210,153,80,0.3) !important;
        border-radius: 10px !important;
        color: #8a5c1a !important;
    }
    .stError {
        background: rgba(200,80,80,0.1) !important;
        border: 1px solid rgba(200,80,80,0.3) !important;
        border-radius: 10px !important;
        color: #9b3030 !important;
    }


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

    /* ===== REMOVE SELECTBOX INNER SEPARATOR LINE ===== */
    div[data-baseweb="select"] > div > div {
        border: none !important;
        box-shadow: none !important;
    }
    div[data-baseweb="select"] > div > div:last-child {
        border-left: none !important;
    }

    /* ===== WARNING (pre-login) ===== */
    .stWarning, [data-testid="stAlert"] {
        background: rgba(201,123,75,0.08) !important;
        border: 1px solid rgba(201,123,75,0.3) !important;
        border-radius: 10px !important;
        color: #7c4a2d !important;
    }

    /* ===== DATAFRAME ===== */
    .stDataFrame {
        border: 1px solid rgba(201,123,75,0.2) !important;
        border-radius: 12px !important;
    }

    /* ===== PROGRESS BAR ===== */
    .stProgress > div > div {
        background: linear-gradient(90deg, #e8a87c, #c97b4b) !important;
        border-radius: 10px !important;
    }

    /* ===== GENERAL TEXT ===== */
    p, h1, h2, h3, h4, h5, h6 {
        color: #3d2b1f !important;
    }

    /* ===== PAGE FADE IN ===== */
    [data-testid="stAppViewContainer"] > section {
        animation: fadeIn 0.15s ease-in;
    }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

    </style>
    """


def page_header(title, subtitle=""):
    return f"""
    <div style="
        background: linear-gradient(135deg, rgba(232,168,124,0.2), rgba(201,123,75,0.1));
        border: 1px solid rgba(201,123,75,0.25);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 28px;
    ">
        <h1 style="
            font-family: 'Syne', sans-serif;
            font-size: 26px;
            font-weight: 800;
            background: linear-gradient(135deg, #c97b4b, #7c4a2d);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 0 4px 0;
            letter-spacing: -0.5px;
        ">{title}</h1>
        <p style="color: #a07850; font-size: 14px; margin: 0;">{subtitle}</p>
    </div>
    """


def metric_card(label, value, icon, color="#c97b4b", bg="rgba(201,123,75,0.08)"):
    return f"""
    <div style="
        background: {bg};
        border: 1px solid {color}33;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        background-color: #fff8f2;
    ">
        <div style="font-size: 28px; margin-bottom: 8px;">{icon}</div>
        <div style="
            font-family: 'Syne', sans-serif;
            font-size: 22px;
            font-weight: 800;
            color: {color};
            margin-bottom: 4px;
        ">{value}</div>
        <div style="
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #a07850;
        ">{label}</div>
    </div>
    """


def status_badge(text, color, bg):
    return f"""
    <div style="
        display: inline-block;
        background: {bg};
        border: 1px solid {color}55;
        border-radius: 20px;
        padding: 8px 20px;
        color: {color};
        font-weight: 600;
        font-size: 14px;
        margin: 8px 0;
    ">{text}</div>
    """


def section_title(title):
    return f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 20px 0 14px 0;
    ">
        <span style="
            font-family: 'Syne', sans-serif;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #a07850;
        ">{title}</span>
        <div style="flex:1; height:1px; background:rgba(201,123,75,0.2);"></div>
    </div>
    """


def sidebar_html():
    return """
    <div style="text-align:center;padding:10px 0 20px 0;">
        <div style="font-size:40px;">💹</div>
        <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;
            background:linear-gradient(135deg,#c97b4b,#7c4a2d);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;">FinSight AI</div>
        <div style="font-size:11px;color:#a07850;margin-top:4px;">AI Budget Advisor</div>
    </div>
    """