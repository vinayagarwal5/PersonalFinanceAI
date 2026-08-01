import streamlit as st

from home import show_home
from merchant_management import show_merchant_management

st.set_page_config(
    page_title="Personal Finance AI",
    page_icon="💰",
    layout="wide"
)

st.sidebar.title("💰 Personal Finance AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🏷 Merchant Management"
    ]
)

if page == "🏠 Dashboard":
    show_home()

elif page == "🏷 Merchant Management":
    show_merchant_management()