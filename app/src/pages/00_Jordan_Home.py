import streamlit as st
from app.src.modules.nav import SideBarLinks
from app.src.modules.api_client import api

st.set_page_config(page_title="Jordan's Dashboard", page_icon="🎓", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state or st.session_state['user_type'] != 'jordan':
    st.warning("Please login from the home page first")
    st.stop()

st.title("Welcome, " + st.session_state.get('user_name', 'Jordan'))
st.markdown("### Your Meal Planning Dashboard")

user_id = st.session_state.get('user_id', 1)

# Fetch dashboard stats from API
dashboard_data = api.get(f"/users/{user_id}/dashboard")

col1, col2, col3, col4 = st.columns(4)

if dashboard_data:
    with col1:
        meals_this_week = dashboard_data.get('meals_this_week', 0)
        change = dashboard_data.get('meals_change', 0)
        st.metric("Meals This Week", str(meals_this_week), f"{change:+d}")

    with col2:
        calories_today = dashboard_data.get('calories_today', 0)
        cal_change = dashboard_data.get('calories_change', 0)
        st.metric("Calories Today", f"{calories_today:,}", f"{cal_change:+d}")

    with col3:
        grocery_items = dashboard_data.get('grocery_items', 0)
        grocery_change = dashboard_data.get('grocery_change', 0)
        st.metric("Grocery Items", str(grocery_items), f"{grocery_change:+d}")

    with col4:
        goal_progress = dashboard_data.get('goal_progress', 0)
        progress_change = dashboard_data.get('progress_change', 0)
        st.metric("Goal Progress", f"{goal_progress}%", f"{progress_change:+d}%")
else:
    # Fallback values if API fails
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

# Fetch today's meals from API
today_meals = api.get(f"/users/{user_id}/meals/today")

if today_meals and len(today_meals) > 0:
    today_col1, today_col2, today_col3 = st.columns(3)

    meal_columns = [today_col1, today_col2, today_col3]
    meal_types = ['breakfast', 'lunch', 'dinner']

    for idx, meal_type in enumerate(meal_types):
        with meal_columns[idx]:
            st.markdown(f"#### {meal_type.capitalize()}")

            meal = next((m for m in today_meals if m.get('meal_type', '').lower() == meal_type), None)

            if meal:
                st.write(f"**{meal.get('meal_name', 'Unknown')}**")
                time_str = meal.get('time', 'N/A')
                calories = meal.get('calories', 0)
                st.write(f"{time_str} | {calories} cal")
            else:
                st.write("*No meal planned*")
else:
    # Fallback data
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
