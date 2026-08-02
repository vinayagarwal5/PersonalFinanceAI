import streamlit as st

from home import show_home
from merchant_management import show_merchant_management
from dashboard.budget import show_budget
from dashboard.cashflow import show_cashflow

st.set_page_config(page_title="Personal Finance AI", page_icon="💰", layout="wide")

st.sidebar.title("💰 Personal Finance AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "💰 Budget Planner",
        "📊 Cash Flow",
        "🏷 Merchant Manager",
    ],
)

if page == "🏠 Home":
    show_home()

elif page == "💰 Budget Planner":
    show_budget()

elif page == "📊 Cash Flow":
    show_cashflow()

elif page == "🏷 Merchant Manager":
    show_merchant_management()
