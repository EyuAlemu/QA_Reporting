from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Callable


import streamlit as st

from config import APP_TITLE
from database.db import initialize_database
from services.openai_service import ask_openai

# ---------------------------------------------------------
# Streamlit page config must be first Streamlit command
# ---------------------------------------------------------
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_database()



# ---------------------------------------------------------
# Landing page logo
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
PAGES_DIR = BASE_DIR / "pages"

logo_path = BASE_DIR / "assets" / "AmpcusLogo.png"

if logo_path.exists():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(str(logo_path), width=250)
else:
    st.warning(f"Logo not found: {logo_path}")


def load_page_callable(module_path: Path) -> Callable[[], None]:
    spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load page: {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "page") or not callable(module.page):
        raise AttributeError(
            f"{module_path.name} must define a callable function named 'page'."
        )

    return module.page


# ---------------------------------------------------------
# Load page functions
# ---------------------------------------------------------
executive_overview = load_page_callable(PAGES_DIR / "1_Executive_Overview.py")
test_execution = load_page_callable(PAGES_DIR / "2_Test_Execution.py")
defect_analytics = load_page_callable(PAGES_DIR / "3_Defect_Analytics.py")
data_management = load_page_callable(PAGES_DIR / "4_Data_Management.py")
ai_insights_chat = load_page_callable(PAGES_DIR / "5_AI_Insights_Chat.py")

# ---------------------------------------------------------
# Navigation
# ---------------------------------------------------------
pg = st.navigation(
    [
        st.Page(
            executive_overview,
            title="Executive Overview",
            icon="📈",
            url_path="executive-overview",
            default=True,
        ),
        st.Page(
            test_execution,
            title="Test Execution",
            icon="🧪",
            url_path="test-execution",
        ),
        st.Page(
            defect_analytics,
            title="Defect Analytics",
            icon="🐞",
            url_path="defect-analytics",
        ),
        st.Page(
            data_management,
            title="Data Management",
            icon="🗂️",
            url_path="data-management",
        ),
        st.Page(
            ai_insights_chat,
            title="AI Insights & Chat",
            icon="🤖",
            url_path="ai-insights-chat",
        ),
    ],
    position="sidebar",
)

# ---------------------------------------------------------
# Shared sidebar content
# ---------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.caption("© Copyright Ampcus Inc. All Rights Reserved")

# ---------------------------------------------------------
# Sidebar Chatbot
# ---------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 Insight Bot")

if "sidebar_chat_history" not in st.session_state:
    st.session_state.sidebar_chat_history = []

user_question = st.sidebar.text_input(
    "Ask about defects, pass rate, execution, risks...",
    key="sidebar_chat_input",
)

col_btn1, col_btn2 = st.sidebar.columns([1, 1])

with col_btn1:
    send_clicked = st.button("Send", key="sidebar_send_btn", use_container_width=True)

with col_btn2:
    clear_clicked = st.button("Clear", key="sidebar_clear_btn", use_container_width=True)

if clear_clicked:
    st.session_state.sidebar_chat_history = []

if send_clicked and user_question:
    try:
        response = ask_openai(user_question)

        # Keep only the latest question and answer in the sidebar
        st.session_state.sidebar_chat_history = [
            {"role": "user", "content": user_question},
            {"role": "assistant", "content": response},
        ]

    except Exception as e:
        st.sidebar.error(f"OpenAI error: {str(e)}")

# Display only the most recent sidebar chat exchange
for msg in st.session_state.sidebar_chat_history:
    if msg["role"] == "user":
        st.sidebar.markdown(f"**You:** {msg['content']}")
    else:
        st.sidebar.markdown(f"**Copilot:** {msg['content']}")

# ---------------------------------------------------------
# Run selected page
# ---------------------------------------------------------
pg.run()