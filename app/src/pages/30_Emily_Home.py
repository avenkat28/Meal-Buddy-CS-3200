import streamlit as st
from app.src.modules.nav import SideBarLinks
from app.src.modules.api_client import api

st.set_page_config(page_title="Admin Dashboard", page_icon="🔧", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state or st.session_state['user_type'] != 'emily':
    st.warning("Please login from the home page first")
    st.stop()

st.title("Welcome, " + st.session_state.get('user_name', 'Emily'))
st.markdown("### System Administration Dashboard")

user_id = st.session_state.get('user_id', 4)

# Fetch admin dashboard data
dashboard_data = api.get("/admin/dashboard")

col1, col2, col3, col4 = st.columns(4)

if dashboard_data:
    with col1:
        active_users = dashboard_data.get('active_users', 0)
        user_change = dashboard_data.get('user_change', 0)
        st.metric("Active Users", str(active_users), f"{user_change:+d}")

    with col2:
        api_health = dashboard_data.get('api_health_pct', 0)
        health_change = dashboard_data.get('health_change', 0)
        st.metric("API Health", f"{api_health}%", f"{health_change:+.1f}%")

    with col3:
        errors_24h = dashboard_data.get('errors_24h', 0)
        error_change = dashboard_data.get('error_change', 0)
        st.metric("Errors (24h)", str(errors_24h), f"{error_change:+d}")

    with col4:
        db_size = dashboard_data.get('db_size_mb', 0)
        size_change = dashboard_data.get('size_change_mb', 0)
        st.metric("DB Size", f"{db_size} MB", f"{size_change:+.1f} MB")
else:
    with col1:
        st.metric("Active Users", "42", "+3")
    with col2:
        st.metric("API Health", "98.5%", "+0.3%")
    with col3:
        st.metric("Errors (24h)", "12", "-8")
    with col4:
        st.metric("DB Size", "145 MB", "+2.3 MB")

st.markdown("---")

st.markdown("### System Status")

# Fetch system status
system_status = api.get("/admin/system/status")

status_col1, status_col2 = st.columns(2)

with status_col1:
    st.markdown("#### Services")

    if system_status:
        services = system_status.get('services', [])
        for service in services:
            name = service.get('name', '')
            status = service.get('status', '')
            if status == 'healthy':
                st.success(f"✓ {name}: {status}")
            elif status == 'degraded':
                st.warning(f"⚠ {name}: {status}")
            else:
                st.error(f"✗ {name}: {status}")
    else:
        st.success("✓ API Server: Healthy")
        st.success("✓ Database: Healthy")
        st.success("✓ Cache: Healthy")
        st.warning("⚠ Email Service: Degraded")

with status_col2:
    st.markdown("#### Recent Activity")

    if system_status:
        activities = system_status.get('recent_activities', [])
        for activity in activities:
            timestamp = activity.get('timestamp', '')
            message = activity.get('message', '')
            st.write(f"• {timestamp}: {message}")
    else:
        st.write("• 10:45 AM: System backup completed")
        st.write("• 10:30 AM: Database optimization finished")
        st.write("• 09:15 AM: 3 new users registered")
        st.write("• 08:50 AM: API health check passed")

st.markdown("---")

st.markdown("### Quick Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("View System Dashboard", use_container_width=True):
        st.switch_page("app/src/pages/31_Emily_System_Dashboard.py")
    st.write("Monitor API and database performance")

with action_col2:
    if st.button("View Error Logs", use_container_width=True):
        st.switch_page("app/src/pages/32_Emily_Error_Logs.py")
    st.write("Review and resolve system errors")

with action_col3:
    if st.button("Data Cleanup Tools", use_container_width=True):
        st.switch_page("app/src/pages/33_Emily_Data_Cleanup.py")
    st.write("Find and fix data quality issues")

st.markdown("---")

st.markdown("### Critical Alerts")

# Fetch alerts
alerts = api.get("/admin/alerts")

if alerts and len(alerts) > 0:
    for alert in alerts:
        severity = alert.get('severity', 'info')
        message = alert.get('message', '')
        timestamp = alert.get('timestamp', '')

        if severity == 'critical':
            st.error(f"🚨 {message} - {timestamp}")
        elif severity == 'warning':
            st.warning(f"⚠️ {message} - {timestamp}")
        else:
            st.info(f"ℹ️ {message} - {timestamp}")
else:
    st.success("No critical alerts at this time")
