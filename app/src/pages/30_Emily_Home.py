import streamlit as st

st.set_page_config(page_title="Admin Dashboard", page_icon="⚙️", layout="wide")

if 'user_type' not in st.session_state or st.session_state['user_type'] != 'emily':
    st.warning("⚠️ Please login from the home page first")
    st.stop()

st.title("⚙️ Welcome, " + st.session_state.get('user_name', 'Emily'))
st.markdown("### System Administration Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Active Users", "1,247", "+24")
    
with col2:
    st.metric("System Status", "✅ Healthy", "")
    
with col3:
    st.metric("API Calls (1h)", "8,453", "+203")
    
with col4:
    st.metric("Errors (24h)", "8", "-4")

st.markdown("---")

st.markdown("### 🚀 Quick Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("📊 System Dashboard", use_container_width=True):
        st.switch_page("pages/31_Emily_System_Dashboard.py")
    st.write("Monitor system health")

with action_col2:
    if st.button("🚨 View Error Logs", use_container_width=True):
        st.switch_page("pages/32_Emily_Error_Logs.py")
    st.write("Check recent errors")

with action_col3:
    if st.button("🧹 Data Cleanup", use_container_width=True):
        st.switch_page("pages/33_Emily_Data_Cleanup.py")
    st.write("Maintain database quality")