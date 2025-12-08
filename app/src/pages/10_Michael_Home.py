import streamlit as st
from app.src.modules.nav import SideBarLinks
from app.src.modules.api_client import api

st.set_page_config(page_title="Michael's Analytics", page_icon="📊", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state or st.session_state['user_type'] != 'michael':
    st.warning("Please login from the home page first")
    st.stop()

st.title("Welcome, " + st.session_state.get('user_name', 'Michael'))
st.markdown("### Data Analytics Dashboard")

user_id = st.session_state.get('user_id', 2)

# Fetch analytics dashboard data
dashboard_data = api.get(f"/users/{user_id}/analytics/dashboard")

col1, col2, col3, col4 = st.columns(4)

if dashboard_data:
    with col1:
        avg_cal = dashboard_data.get('avg_daily_calories', 0)
        cal_change = dashboard_data.get('cal_change_pct', 0)
        st.metric("Avg Daily Calories", f"{avg_cal:,}", f"{cal_change:+.0f}%")

    with col2:
        protein = dashboard_data.get('protein_per_day', 0)
        protein_change = dashboard_data.get('protein_change_pct', 0)
        st.metric("Protein/Day", f"{protein}g", f"{protein_change:+.0f}%")

    with col3:
        weekly_cost = dashboard_data.get('weekly_cost', 0)
        cost_change = dashboard_data.get('cost_change', 0)
        st.metric("Weekly Cost", f"${weekly_cost:.2f}", f"-${abs(cost_change):.2f}")

    with col4:
        plant_based = dashboard_data.get('plant_based_pct', 0)
        pb_change = dashboard_data.get('pb_change_pct', 0)
        st.metric("Plant-Based %", f"{plant_based}%", f"{pb_change:+.0f}%")
else:
    with col1:
        st.metric("Avg Daily Calories", "1,642", "+8%")
    with col2:
        st.metric("Protein/Day", "82g", "+9%")
    with col3:
        st.metric("Weekly Cost", "$43.85", "-$5")
    with col4:
        st.metric("Plant-Based %", "64%", "+4%")

st.markdown("---")

st.markdown("### Quick Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("View Analytics", use_container_width=True):
        st.switch_page("app/src/pages/11_Michael_Analytics.py")
    st.write("Deep dive into nutrition trends")

with action_col2:
    if st.button("Export Data", use_container_width=True):
        st.switch_page("app/src/pages/12_Michael_Export_Data.py")
    st.write("Download CSV reports")

with action_col3:
    if st.button("Cost Analysis", use_container_width=True):
        st.switch_page("app/src/pages/13_Michael_Cost_Analysis.py")
    st.write("Analyze meal costs")
