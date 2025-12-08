import streamlit as st
import pandas as pd
from modules.api_client import api
from modules.nav import SideBarLinks

st.set_page_config(page_title="Error Logs", page_icon="MB", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("Please login from the home page first")
    st.stop()

st.title("Error Logs")
st.markdown("Monitor and resolve system errors")

st.markdown("---")

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

with filter_col1:
    time_filter = st.selectbox("Time Range", ["Last Hour", "Last 24 Hours", "Last 7 Days", "All Time"])

with filter_col2:
    severity_filter = st.selectbox("Severity", ["All", "Critical", "Error", "Warning", "Info"])

with filter_col3:
    status_filter = st.selectbox("Status", ["All", "Unresolved", "Resolved"])

with filter_col4:
    category_filter = st.selectbox("Category", ["All", "API", "Database", "AI", "User Input"])

st.markdown("---")

st.markdown("### Errors (Last 24 hours)")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Errors", "8", "-4 from yesterday")

with col2:
    st.metric("Critical", "0", "0")

with col3:
    st.metric("Unresolved", "3", "-2")

st.markdown("---")

errors = [
    {
        'time': '2:34 PM',
        'severity': 'Error',
        'type': 'Grocery Price API Timeout',
        'message': 'Failed to fetch prices from external API',
        'resolved': False
    },
    {
        'time': '1:12 PM',
        'severity': 'Warning',
        'type': 'Ingredient Mismatch',
        'message': 'Ingredient "Red Bell Pepper" not found in grocery dataset',
        'resolved': False
    },
    {
        'time': '11:45 AM',
        'severity': 'Error',
        'type': 'Database Connection Lost',
        'message': 'Connection pool exhausted, max connections reached',
        'resolved': True
    },
    {
        'time': '10:22 AM',
        'severity': 'Warning',
        'type': 'Invalid User Input',
        'message': 'User entered negative calorie goal: -500',
        'resolved': False
    },
    {
        'time': '9:15 AM',
        'severity': 'Error',
        'type': 'Recipe Not Found',
        'message': 'Meal ID 9999 referenced but does not exist',
        'resolved': True
    }
]

for error in errors:
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 3, 1])
        
        with col1:
            st.caption(error['time'])
        
        with col2:
            if error['severity'] == 'Critical':
                st.error(error['severity'])
            elif error['severity'] == 'Error':
                st.error(error['severity'])
            elif error['severity'] == 'Warning':
                st.warning(error['severity'])
            else:
                st.info(error['severity'])
        
        with col3:
            st.write(f"**{error['type']}**")
        
        with col4:
            st.caption(error['message'])
        
        with col5:
            if error['resolved']:
                st.success("Fixed")
            else:
                if st.button("Fix", key=f"fix_{error['time']}"):
                    st.success("Marked as resolved!")
        
        st.markdown("---")

st.markdown("### Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("Export CSV", use_container_width=True):
        st.success("Error log exported!")

with action_col2:
    if st.button("Clear Resolved", use_container_width=True):
        st.success("Cleared 5 resolved errors")

with action_col3:
    if st.button("Refresh", use_container_width=True):
        st.success("Logs refreshed!")