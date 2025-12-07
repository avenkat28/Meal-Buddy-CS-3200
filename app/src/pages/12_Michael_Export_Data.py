import streamlit as st
import pandas as pd
from datetime import datetime
from app.src.modules.api_client import api

st.set_page_config(page_title="Export Data", page_icon="📤", layout="wide")

if 'user_type' not in st.session_state:
    st.warning("⚠️ Please login from the home page first")
    st.stop()

st.title("📤 Export Nutrition Data")
st.markdown("Download your meal and nutrition data in CSV format")

user_id = st.session_state.get('user_id', 2)

st.markdown("---")

st.markdown("### 🔧 Export Options")

export_col1, export_col2 = st.columns(2)

with export_col1:
    export_type = st.selectbox(
        "Select Data Type",
        ["Daily Nutrition Summary", "Meal Plans", "Ingredients", "Cost Analysis", "All Data"]
    )

with export_col2:
    date_range = st.selectbox(
        "Date Range",
        ["Last 7 Days", "Last 30 Days", "This Month", "All Time"]
    )

include_raw = st.checkbox("Include raw ingredient data", value=True)
include_recipes = st.checkbox("Include recipe steps", value=False)
include_costs = st.checkbox("Include cost breakdown", value=True)

st.markdown("---")

st.markdown("### 📊 Data Preview")

preview_data = {
    'Date': ['2025-11-18', '2025-11-19', '2025-11-20', '2025-11-21', '2025-11-22'],
    'Calories': [1520, 1680, 1450, 1590, 1720],
    'Protein (g)': [78, 85, 72, 81, 88],
    'Carbs (g)': [182, 195, 178, 188, 202],
    'Fat (g)': [52, 58, 48, 55, 61]
}

df_preview = pd.DataFrame(preview_data)
st.dataframe(df_preview, use_container_width=True, hide_index=True)

st.info(f"📊 **Preview:** Showing 5 of {len(df_preview)} rows")

st.markdown("---")

export_btn_col1, export_btn_col2, export_btn_col3 = st.columns(3)

with export_btn_col1:
    if st.button("📥 Download CSV", use_container_width=True):
        csv = df_preview.to_csv(index=False)
        st.download_button(
            label="💾 Click to Download",
            data=csv,
            file_name=f"nutrition_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with export_btn_col2:
    if st.button("📧 Email Report", use_container_width=True):
        st.success("✅ Report sent to your email!")

with export_btn_col3:
    if st.button("☁️ Save to Cloud", use_container_width=True):
        st.success("✅ Saved to cloud storage!")

st.markdown("---")

st.markdown("### 📋 Export History")

history_data = {
    'Date': ['2025-11-15', '2025-11-08', '2025-11-01'],
    'Type': ['Daily Nutrition', 'Meal Plans', 'All Data'],
    'Size': ['45 KB', '128 KB', '512 KB']
}

df_history = pd.DataFrame(history_data)
st.dataframe(df_history, use_container_width=True, hide_index=True)