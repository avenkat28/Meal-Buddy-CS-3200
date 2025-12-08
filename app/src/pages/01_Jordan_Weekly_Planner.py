import streamlit as st
import pandas as pd
from modules.api_client import api
from modules.nav import SideBarLinks

st.set_page_config(page_title="Weekly Meal Planner", page_icon="MB", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("Please login from the home page first")
    st.stop()

st.title("Weekly Meal Planner")
st.markdown("Plan and manage your meals for the week")

user_id = st.session_state.get('user_id', 1)
plan_id = 1

st.markdown("---")

col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    if st.button("< Previous Week"):
        st.info("Previous week functionality")

with col2:
    st.markdown("### of November 11 - November 17, 2025")

with col3:
    if st.button("Next Week >"):
        st.info("Next week functionality")

st.markdown("---")

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
meal_types = ['Breakfast', 'Lunch', 'Dinner']

mock_meals = {
    'Monday': {
        'Breakfast': {'name': 'Oatmeal with Berries', 'calories': 280},
        'Lunch': {'name': 'Grilled Chicken Salad', 'calories': 450},
        'Dinner': {'name': 'Salmon with Quinoa', 'calories': 520}
    },
    'Tuesday': {
        'Breakfast': {'name': 'Greek Yogurt Parfait', 'calories': 320},
        'Lunch': {'name': 'Turkey Wrap', 'calories': 380},
        'Dinner': {'name': 'Stir-Fry Vegetables', 'calories': 410}
    },
    'Wednesday': {
        'Breakfast': {'name': 'Scrambled Eggs & Toast', 'calories': 350},
        'Lunch': {'name': 'Chicken Rice Bowl', 'calories': 480},
        'Dinner': {'name': 'Pasta Primavera', 'calories': 490}
    },
    'Thursday': {
        'Breakfast': {'name': 'Smoothie Bowl', 'calories': 290},
        'Lunch': {'name': 'Quinoa Salad', 'calories': 420},
        'Dinner': {'name': 'Grilled Steak', 'calories': 580}
    },
    'Friday': {
        'Breakfast': {'name': 'Avocado Toast', 'calories': 340},
        'Lunch': {'name': 'Sushi Bowl', 'calories': 460},
        'Dinner': {'name': 'Shrimp Teriyaki', 'calories': 550}
    },
    'Saturday': {
        'Breakfast': {'name': 'Pancakes', 'calories': 400},
        'Lunch': {'name': 'Burger & Salad', 'calories': 520},
        'Dinner': {'name': 'BBQ Chicken', 'calories': 560}
    },
    'Sunday': {
        'Breakfast': {'name': 'French Toast', 'calories': 380},
        'Lunch': {'name': 'Caesar Salad', 'calories': 390},
        'Dinner': {'name': 'Roast Chicken', 'calories': 540}
    }
}

for day in days:
    st.markdown(f"### {day}")

    cols = st.columns(3)

    for idx, meal_type in enumerate(meal_types):
        with cols[idx]:
            if day in mock_meals and meal_type in mock_meals[day]:
                meal = mock_meals[day][meal_type]
                st.markdown(f"**{meal_type}**")
                st.write(f"{meal['name']}")
                st.write(f"{meal['calories']} cal")

                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("View", key=f"view_{day}_{meal_type}"):
                        st.info(f"Viewing details for {meal['name']}")
                with btn_col2:
                    if st.button("Delete", key=f"delete_{day}_{meal_type}"):
                        st.success(f"Removed {meal['name']}!")
            else:
                st.markdown(f"**{meal_type}**")
                st.write("*No meal planned*")
                if st.button("+ Add", key=f"add_{day}_{meal_type}"):
                    st.info(f"Adding meal for {day} {meal_type}")

    st.markdown("---")

st.markdown("### Summary")

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.metric("Total Meals Planned", "21")

with summary_col2:
    st.metric("Avg Calories/Day", "1,567")

with summary_col3:
    st.metric("Est. Weekly Cost", "$43.85")