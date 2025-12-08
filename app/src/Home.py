import streamlit as st
import logging

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="MealBuddy - Meal Planning Made Easy",
    page_icon="🍽️",
    layout="wide"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .logo {
        text-align: center;
        font-size: 5rem;
        margin-bottom: 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="logo">MB</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-header">MealBuddy</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your Personal Meal Planning Assistant</p>', unsafe_allow_html=True)

st.markdown("""
---
### Welcome to MealBuddy!
Plan your meals, manage your grocery list, and track your nutrition - all in one place.

**Select your role below to get started:**
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Primary Users")

    with st.container():
        st.markdown("#### Jordan Thompson - College Junior")
        st.write("*Track meals, plan your week, and achieve health goals*")

        jordan_users = [
            "Select a user...",
            "Jordan Thompson (Demo User 1)",
            "Alex Chen (Demo User 2)",
            "Taylor Williams (Demo User 3)"
        ]

        jordan_selected = st.selectbox(
            "Select College Student:",
            jordan_users,
            key="jordan_select"
        )

        if st.button("Login as College Student", key="jordan_login"):
            if jordan_selected != "Select a user...":
                st.session_state['user_type'] = 'jordan'
                st.session_state['user_name'] = jordan_selected
                st.session_state['user_id'] = 1
                st.success(f"Logged in as {jordan_selected}")
                st.info("Use the sidebar to navigate to your features")
            else:
                st.error("Please select a user first")

    st.markdown("---")

    with st.container():
        st.markdown("#### Sarah Martinez - Young Adult")
        st.write("*Reduce food waste, manage pantry, find recipes*")

        sarah_users = [
            "Select a user...",
            "Sarah Martinez (Demo User 1)",
            "Emma Davis (Demo User 2)",
            "Maya Patel (Demo User 3)"
        ]

        sarah_selected = st.selectbox(
            "Select Young Adult:",
            sarah_users,
            key="sarah_select"
        )

        if st.button("Login as Young Adult", key="sarah_login"):
            if sarah_selected != "Select a user...":
                st.session_state['user_type'] = 'sarah'
                st.session_state['user_name'] = sarah_selected
                st.session_state['user_id'] = 3
                st.success(f"Logged in as {sarah_selected}")
                st.info("Use the sidebar to navigate to your features")
            else:
                st.error("Please select a user first")

with col2:
    st.markdown("### Advanced Users")

    with st.container():
        st.markdown("#### Michael Johnson - Data Analyst")
        st.write("*Analyze nutrition data, export reports, track costs*")

        michael_users = [
            "Select a user...",
            "Michael Johnson (Demo User 1)",
            "David Kim (Demo User 2)",
            "Chris Anderson (Demo User 3)"
        ]

        michael_selected = st.selectbox(
            "Select Data Analyst:",
            michael_users,
            key="michael_select"
        )

        if st.button("Login as Data Analyst", key="michael_login"):
            if michael_selected != "Select a user...":
                st.session_state['user_type'] = 'michael'
                st.session_state['user_name'] = michael_selected
                st.session_state['user_id'] = 2
                st.success(f"Logged in as {michael_selected}")
                st.info("Use the sidebar to navigate to your features")
            else:
                st.error("Please select a user first")

    st.markdown("---")

    with st.container():
        st.markdown("#### Emily Carter - System Admin")
        st.write("*Monitor system health, view logs, maintain data*")

        emily_users = [
            "Select a user...",
            "Emily Carter (Demo User 1)",
            "Admin User (Demo User 2)"
        ]

        emily_selected = st.selectbox(
            "Select System Admin:",
            emily_users,
            key="emily_select"
        )

        if st.button("Login as System Admin", key="emily_login"):
            if emily_selected != "Select a user...":
                st.session_state['user_type'] = 'emily'
                st.session_state['user_name'] = emily_selected
                st.session_state['user_id'] = 99
                st.success(f"Logged in as {emily_selected}")
                st.info("Use the sidebar to navigate to your features")
            else:
                st.error("Please select a user first")

st.markdown("---")
if 'user_type' in st.session_state:
    st.success(f"Currently logged in as: **{st.session_state.get('user_name', 'Unknown User')}**")
    st.info("Navigate using the sidebar on the left")
else:
    st.info("Please select a user type and login above to continue")

st.markdown("---")
st.markdown("### Key Features")

feature_col1, feature_col2, feature_col3, feature_col4 = st.columns(4)

with feature_col1:
    st.markdown("#### Meal Planning")
    st.write("Create weekly meal plans tailored to your dietary needs")

with feature_col2:
    st.markdown("#### Grocery Lists")
    st.write("Auto-generate shopping lists from your meal plans")

with feature_col3:
    st.markdown("#### Nutrition Tracking")
    st.write("Monitor your daily nutrition and progress toward goals")

with feature_col4:
    st.markdown("#### Cost Analysis")
    st.write("Track meal costs and optimize your food budget")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>MealBuddy - CS 3200 Database Design Project</p>
    <p>Fall 2025 - Northeastern University</p>
</div>
""", unsafe_allow_html=True)