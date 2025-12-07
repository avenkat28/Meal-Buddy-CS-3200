import streamlit as st
import pandas as pd
from app.src.modules.api_client import api
from app.src.modules.nav import SideBarLinks

st.set_page_config(page_title="My Pantry", page_icon="📦", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("⚠️ Please login from the home page first")
    st.stop()

st.title("📦 My Pantry")
st.markdown("Track what ingredients you have at home")

user_id = st.session_state.get('user_id', 3)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Items", "28")

with col2:
    st.metric("Expiring Soon", "4 items")

with col3:
    st.metric("Items to Buy", "12")

st.markdown("---")

filter_col1, filter_col2 = st.columns([2, 1])

with filter_col1:
    search = st.text_input("🔍 Search pantry", "")

with filter_col2:
    sort_by = st.selectbox("Sort by", ["Name", "Expiration Date", "Quantity"])

st.markdown("---")

pantry_items = [
    {'name': 'Chicken Breast', 'quantity': '2 lbs', 'owned': True, 'used_in': 3, 'expiring': False},
    {'name': 'Rice (White)', 'quantity': '5 cups', 'owned': False, 'used_in': 2, 'expiring': False},
    {'name': 'Olive Oil', 'quantity': '1 bottle', 'owned': True, 'used_in': 4, 'expiring': False},
    {'name': 'Bell Peppers', 'quantity': '3 pieces', 'owned': False, 'used_in': 2, 'expiring': True},
    {'name': 'Quinoa', 'quantity': '2 cups', 'owned': False, 'used_in': 1, 'expiring': False},
    {'name': 'Soy Sauce', 'quantity': '1 bottle', 'owned': True, 'used_in': 2, 'expiring': False},
    {'name': 'Garlic', 'quantity': '1 bulb', 'owned': True, 'used_in': 5, 'expiring': True},
    {'name': 'Tomatoes', 'quantity': '4 pieces', 'owned': True, 'used_in': 3, 'expiring': True}
]

st.markdown("### My Pantry Items")
st.caption("Check off items you have. Green badge = used in multiple meals this week")

for item in pantry_items:
    if search.lower() in item['name'].lower() or search == "":
        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
        
        with col1:
            checkbox_label = f"**{item['name']}**"
            if item['expiring']:
                checkbox_label += " ⚠️ Expiring Soon"
            st.checkbox(checkbox_label, value=item['owned'], key=f"pantry_{item['name']}")
        
        with col2:
            st.write(f"Used in {item['used_in']} meals this week")
        
        with col3:
            if item['used_in'] >= 3:
                st.markdown("🟢")
            else:
                st.markdown(f"{item['used_in']}")
        
        with col4:
            if st.button("➕", key=f"add_{item['name']}", help="Add to shopping list"):
                st.success(f"Added {item['name']} to shopping list")

st.markdown("---")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:
    st.info("📊 **2 items owned • 6 items to buy**")
    st.caption("Tap to see suggested meals")

with summary_col2:
    if st.button("🛒 View Grocery List", use_container_width=True):
        st.info("Redirecting to grocery list...")

st.markdown("---")

st.markdown("### 💡 Suggested Meals Based on Your Pantry")

suggestions = [
    {'meal': 'Garlic Chicken Stir-Fry', 'matching': '4/5 ingredients'},
    {'meal': 'Tomato Olive Pasta', 'matching': '3/4 ingredients'},
    {'meal': 'Asian Rice Bowl', 'matching': '3/5 ingredients'}
]

for suggestion in suggestions:
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        st.write(f"**{suggestion['meal']}**")
    with col2:
        st.write(f"✅ {suggestion['matching']}")
    with col3:
        if st.button("View", key=f"view_{suggestion['meal']}"):
            st.info(f"Viewing recipe for {suggestion['meal']}")