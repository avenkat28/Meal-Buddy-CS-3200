import streamlit as st
from app.src.modules.nav import SideBarLinks
from app.src.modules.api_client import api

st.set_page_config(page_title="Sarah's Kitchen", page_icon="🏠", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state or st.session_state['user_type'] != 'sarah':
    st.warning("Please login from the home page first")
    st.stop()

st.title("Welcome, " + st.session_state.get('user_name', 'Sarah'))
st.markdown("### Your Kitchen Management Hub")

user_id = st.session_state.get('user_id', 3)

# Fetch kitchen dashboard data
dashboard_data = api.get(f"/users/{user_id}/kitchen/dashboard")

col1, col2, col3, col4 = st.columns(4)

if dashboard_data:
    with col1:
        pantry_items = dashboard_data.get('pantry_items', 0)
        pantry_change = dashboard_data.get('pantry_change', 0)
        st.metric("Pantry Items", str(pantry_items), f"{pantry_change:+d}")

    with col2:
        expiring = dashboard_data.get('expiring_soon', 0)
        st.metric("Expiring Soon", f"{expiring} items", "")

    with col3:
        shared = dashboard_data.get('shared_ingredients', 0)
        shared_change = dashboard_data.get('shared_change', 0)
        st.metric("Shared Ingredients", str(shared), f"{shared_change:+d}")

    with col4:
        waste_reduced = dashboard_data.get('waste_reduced_pct', 0)
        waste_change = dashboard_data.get('waste_change_pct', 0)
        st.metric("Waste Reduced", f"{waste_reduced}%", f"{waste_change:+d}%")
else:
    with col1:
        st.metric("Pantry Items", "28", "-3")
    with col2:
        st.metric("Expiring Soon", "4 items", "")
    with col3:
        st.metric("Shared Ingredients", "8", "+2")
    with col4:
        st.metric("Waste Reduced", "45%", "+12%")

st.markdown("---")

st.markdown("### Quick Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("Manage Pantry", use_container_width=True):
        st.switch_page("app/src/pages/21_Sarah_Pantry.py")
    st.write("Track what you have at home")

with action_col2:
    if st.button("Get Suggestions", use_container_width=True):
        st.switch_page("app/src/pages/22_Sarah_Meal_Suggestions.py")
    st.write("Find recipes using your ingredients")

with action_col3:
    if st.button("Browse Recipes", use_container_width=True):
        st.switch_page("app/src/pages/23_Sarah_Recipe_Browser.py")
    st.write("Explore new meal ideas")
