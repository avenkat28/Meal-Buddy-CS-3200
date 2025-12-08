import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from app.src.modules.api_client import api
from app.src.modules.nav import SideBarLinks

st.set_page_config(page_title="System Dashboard", page_icon="📊", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("Please login from the home page first")
    st.stop()

st.title("System Health Dashboard")
st.markdown("Monitor MealBuddy system performance")

st.markdown("---")

st.markdown("### System Status")

status_col1, status_col2, status_col3, status_col4 = st.columns(4)

with status_col1:
    st.metric("API Status", "Operational")
    st.caption("Avg Response: 127ms")

with status_col2:
    st.metric("Database", "Healthy")
    st.caption("Connections: 24/100")

with status_col3:
    st.metric("Active Users", "1,247", "+24")
    st.caption("Peak: 1,503")

with status_col4:
    st.metric("Uptime", "99.8%", "+0.1%")
    st.caption("Last 30 days")

st.markdown("---")

st.markdown("### API Performance (Last 24 Hours)")

hours = list(range(24))
api_calls = [340, 280, 210, 190, 170, 150, 180, 290, 420, 520, 610, 670, 720, 690, 650, 720, 810, 920, 880, 760, 640,
             520, 450, 380]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=hours,
    y=api_calls,
    mode='lines+markers',
    name='API Calls',
    line=dict(color='#4CAF50', width=2),
    fill='tozeroy'
))

fig.update_layout(
    title="API Calls per Hour",
    xaxis_title="Hour",
    yaxis_title="Calls",
    height=400,
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.markdown("### Database Activity")

db_col1, db_col2, db_col3, db_col4 = st.columns(4)

with db_col1:
    st.metric("Plans Created (24h)", "342", "+12")

with db_col2:
    st.metric("Meals Added", "1,284", "+48")

with db_col3:
    st.metric("API Calls (1h)", "8,453", "+203")

with db_col4:
    st.metric("Database Size", "2.4 GB", "+0.1 GB")

st.markdown("---")

st.markdown("### Recent Alerts")

alerts = [
    {'time': '2 min ago', 'severity': 'Info', 'message': 'Database backup completed successfully'},
    {'time': '15 min ago', 'severity': 'Warning', 'message': 'API response time exceeded 200ms threshold'},
    {'time': '1 hour ago', 'severity': 'Info', 'message': 'Peak usage detected: 1,503 concurrent users'},
    {'time': '3 hours ago', 'severity': 'Success', 'message': 'System update deployed successfully'}
]

for alert in alerts:
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        st.caption(alert['time'])

    with col2:
        if alert['severity'] == 'Info':
            st.info(alert['severity'])
        elif alert['severity'] == 'Warning':
            st.warning(alert['severity'])
        else:
            st.success(alert['severity'])

    with col3:
        st.write(alert['message'])

st.markdown("---")

action_col1, action_col2 = st.columns(2)

with action_col1:
    if st.button("Refresh Data", use_container_width=True):
        st.success("Data refreshed!")

with action_col2:
    if st.button("Generate Report", use_container_width=True):
        st.success("Report generated and sent to admin@mealbuddy.com")