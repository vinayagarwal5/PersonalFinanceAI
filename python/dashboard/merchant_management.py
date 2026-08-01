import os
import sys
import streamlit as st

# ---------------------------------------------------------
# Add project root to Python path
# ---------------------------------------------------------
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(PROJECT_ROOT)

from services.merchant_service import MerchantService


st.set_page_config(page_title="Merchant Management", layout="wide")

st.title("🏷 Merchant Management")

service = MerchantService()

# =====================================================
# Search
# =====================================================

search = st.text_input("Search Merchant", placeholder="Amazon, Blinkit, Airtel...")

if search:
    merchant_df = service.search_merchants(search)

else:
    merchant_df = service.get_all_merchants()

st.write(f"### Total Merchants : {len(merchant_df)}")

if merchant_df.empty:
    st.warning("No merchants found.")
    st.stop()

# =====================================================
# Select Merchant
# =====================================================

merchant_list = merchant_df["merchant_name"].tolist()

selected = st.selectbox("Select Merchant", merchant_list)

merchant = service.get_merchant(selected)

st.divider()

# =====================================================
# Edit Form
# =====================================================

st.subheader("Merchant Details")

col1, col2 = st.columns(2)

with col1:
    merchant_name = st.text_input(
        "Merchant Name", value=merchant["merchant_name"], disabled=True
    )

    normalized_name = st.text_input(
        "Normalized Name", value=merchant["normalized_name"]
    )

    categories = service.get_categories()

    current_category = merchant["category"]

    if current_category in categories:
        category_index = categories.index(current_category)

    else:
        category_index = 0

    category = st.selectbox("Category", categories, index=category_index)

with col2:
    sub_category = st.text_input(
        "Sub Category",
        value="" if merchant["sub_category"] is None else merchant["sub_category"],
    )

    merchant_type = st.text_input(
        "Merchant Type",
        value="" if merchant["merchant_type"] is None else merchant["merchant_type"],
    )

    active = st.checkbox("Active", value=bool(merchant["is_active"]))

st.divider()

# =====================================================
# Save
# =====================================================

if st.button("💾 Save Changes", use_container_width=True):
    service.update_merchant(
        merchant_name=merchant_name,
        normalized_name=normalized_name,
        category=category,
        sub_category=sub_category,
        merchant_type=merchant_type,
    )

    service.set_active(merchant_name, active)

    st.success("Merchant updated successfully.")

    st.rerun()

# =====================================================
# Merchant Table
# =====================================================

st.divider()

st.subheader("Merchant Master")

st.dataframe(merchant_df, use_container_width=True, hide_index=True)
