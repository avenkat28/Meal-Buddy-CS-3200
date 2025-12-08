import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(page_title="Michael's Analytics", page_icon="MB", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state or st.session_state['user_type'] != 'michael':
    st.warning("Please login from the home page first")
    st.stop()

st.title("Welcome, " + st.session_state.get('user_name', 'Michael'))
st.markdown("### Analytics Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Avg Daily Calories", "1,642", "+8%")

with col2:
    st.metric("Protein/Day", "82g", "+9%")

with col3:
    st.metric("Weekly Cost", "$43.85", "-$5")

with col4:
    st.metric("Plant-Based %", "64%", "+4%")

st.markdown("---")

st.markdown("### Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("View Analytics", use_container_width=True):
        st.switch_page("pages/11_Michael_Analytics.py")
    st.write("Deep dive into nutrition trends")

with action_col2:
    if st.button("Export Data", use_container_width=True):
        st.switch_page("pages/12_Michael_Export_Data.py")
    st.write("Download CSV reports")

with action_col3:
    if st.button("Cost Analysis", use_container_width=True):
        st.switch_page("pages/13_Michael_Cost_Analysis.py")
    st.write("Analyze meal costs")