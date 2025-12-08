import streamlit as st
from app.src.modules.nav import SideBarLinks

st.set_page_config(page_title="Jordan's Dashboard", page_icon="🎓", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state or st.session_state['user_type'] != 'jordan':
    st.warning("Please login from the home page first")
    st.stop()

st.title("Welcome, " + st.session_state.get('user_name', 'Jordan'))
st.markdown("### Your Meal Planning Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Meals This Week", "12", "2")

with col2:
    st.metric("Calories Today", "1,450", "-50")

with col3:
    st.metric("Grocery Items", "24", "8")

with col4:
    st.metric("Goal Progress", "86%", "6%")

st.markdown("---")

st.markdown("### Quick Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("View Weekly Meal Plan", use_container_width=True):
        st.switch_page("app/src/pages/01_Jordan_Weekly_Planner.py")
    st.write("See and manage your meals for the week")

with action_col2:
    if st.button("View Grocery List", use_container_width=True):
        st.switch_page("app/src/pages/02_Jordan_Grocery_List.py")
    st.write("Check what you need to buy")

with action_col3:
    if st.button("View Progress", use_container_width=True):
        st.switch_page("app/src/pages/03_Jordan_Progress.py")
    st.write("Track your nutrition goals")

st.markdown("---")

st.markdown("### Today's Meals")

today_col1, today_col2, today_col3 = st.columns(3)

with today_col1:
    st.markdown("#### Breakfast")
    st.write("**Oatmeal with Berries**")
    st.write("8:00 AM | 280 cal")

with today_col2:
    st.markdown("#### Lunch")
    st.write("**Grilled Chicken Salad**")
    st.write("12:30 PM | 450 cal")

with today_col3:
    st.markdown("#### Dinner")
    st.write("**Salmon with Quinoa**")
    st.write("7:00 PM | 520 cal")