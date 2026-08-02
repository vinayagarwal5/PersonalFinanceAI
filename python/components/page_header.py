import streamlit as st


def show_page_header(title, subtitle=None):

    st.title(title)

    if subtitle:
        st.caption(subtitle)

    st.divider()
