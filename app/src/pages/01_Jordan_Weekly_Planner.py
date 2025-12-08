import streamlit as st
import pandas as pd
from app.src.modules.api_client import api
from app.src.modules.nav import SideBarLinks

st.set_page_config(page_title="Weekly Meal Planner", page_icon="📅", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("Please login from the home page first")
    st.stop()

st.title("Weekly Meal Planner")
st.markdown("Plan and manage your meals for the week")

user_id = st.session_state.get('user_id', 1)
plan_id = st.session_state.get('current_plan_id', 1)

st.markdown("---")

col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    if st.button("< Previous Week"):
        st.info("Previous week functionality")

with col2:
    st.markdown("### Week of November 11 - November 17, 2025")

with col3:
    if st.button("Next Week >"):
        st.info("Next week functionality")

st.markdown("---")

# Fetch planned meals from API
planned_meals_data = api.get(f"/meal_plans/{plan_id}/planned_meals")

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_abbr = {'Monday': 'Mon', 'Tuesday': 'Tue', 'Wednesday': 'Wed', 'Thursday': 'Thu',
            'Friday': 'Fri', 'Saturday': 'Sat', 'Sunday': 'Sun'}
meal_types = ['breakfast', 'lunch', 'dinner']

# Organize data by day and meal type
meals_by_day = {}
if planned_meals_data:
    for meal in planned_meals_data:
        day = meal.get('day_of_week', '')
        meal_type = meal.get('meal_type', '').lower()

        if day not in meals_by_day:
            meals_by_day[day] = {}

        meals_by_day[day][meal_type] = {
            'id': meal.get('planned_meal_id'),
            'name': meal.get('meal_name', 'Unknown'),
            'calories': meal.get('calories', 0)
        }

for day in days:
    st.markdown(f"### {day}")
    cols = st.columns(3)

    for idx, meal_type in enumerate(meal_types):
        with cols[idx]:
            day_key = day_abbr[day]

            if day_key in meals_by_day and meal_type in meals_by_day[day_key]:
                meal = meals_by_day[day_key][meal_type]
                st.markdown(f"**{meal_type.capitalize()}**")
                st.write(f"{meal['name']}")
                st.write(f"{meal['calories']} cal")

                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("View", key=f"view_{day}_{meal_type}"):
                        st.info(f"Viewing details for {meal['name']}")
                with btn_col2:
                    if st.button("Delete", key=f"delete_{day}_{meal_type}"):
                        result = api.delete(f"/planned_meals/{meal['id']}")
                        if result:
                            st.success(f"Removed {meal['name']}!")
                            st.rerun()
            else:
                st.markdown(f"**{meal_type.capitalize()}**")
                st.write("*No meal planned*")
                if st.button("+ Add", key=f"add_{day}_{meal_type}"):
                    st.info(f"Adding meal for {day} {meal_type}")

    st.markdown("---")

st.markdown("### Weekly Summary")

# Fetch summary data from API
summary_data = api.get(f"/meal_plans/{plan_id}/summary")

summary_col1, summary_col2, summary_col3 = st.columns(3)

if summary_data:
    with summary_col1:
        st.metric("Total Meals Planned", str(summary_data.get('total_meals', 0)))

    with summary_col2:
        avg_cals = summary_data.get('avg_calories', 0)
        st.metric("Avg Calories/Day", f"{avg_cals:,}")

    with summary_col3:
        cost = summary_data.get('weekly_cost', 0)
        st.metric("Est. Weekly Cost", f"${cost:.2f}")
else:
    with summary_col1:
        st.metric("Total Meals Planned", "21")
    with summary_col2:
        st.metric("Avg Calories/Day", "1,567")
    with summary_col3:
        st.metric("Est. Weekly Cost", "$43.85")
