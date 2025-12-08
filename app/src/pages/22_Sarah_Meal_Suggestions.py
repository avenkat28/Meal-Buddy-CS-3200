import streamlit as st
import pandas as pd
from app.src.modules.api_client import api
from app.src.modules.nav import SideBarLinks

st.set_page_config(page_title="Meal Suggestions", page_icon="", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("Please login from the home page first")
    st.stop()

st.title("Meal Suggestions")
st.markdown("Discover recipes based on what you have")

user_id = st.session_state.get('user_id', 3)

st.markdown("---")

st.markdown("### Filter Suggestions")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    difficulty = st.selectbox("Difficulty", ["All", "Easy", "Medium", "Hard"])

with filter_col2:
    max_time = st.slider("Max Cooking Time (min)", 0, 120, 60)

with filter_col3:
    min_match = st.slider("Min Ingredient Match", 0, 100, 50)

st.markdown("---")

st.markdown("### Recommended for You")

meals = [
    {
        'name': 'Chicken Fried Rice',
        'difficulty': 'Easy',
        'time': 25,
        'match': 80,
        'ingredients_owned': 4,
        'ingredients_total': 5,
        'missing': ['Green Onions']
    },
    {
        'name': 'Garlic Butter Chicken',
        'difficulty': 'Easy',
        'time': 30,
        'match': 75,
        'ingredients_owned': 3,
        'ingredients_total': 4,
        'missing': ['Butter']
    },
    {
        'name': 'Vegetable Stir-Fry',
        'difficulty': 'Easy',
        'time': 20,
        'match': 70,
        'ingredients_owned': 5,
        'ingredients_total': 7,
        'missing': ['Broccoli', 'Carrots']
    },
    {
        'name': 'Tomato Basil Pasta',
        'difficulty': 'Medium',
        'time': 35,
        'match': 65,
        'ingredients_owned': 4,
        'ingredients_total': 6,
        'missing': ['Basil', 'Parmesan']
    },
    {
        'name': 'Quinoa Power Bowl',
        'difficulty': 'Easy',
        'time': 40,
        'match': 60,
        'ingredients_owned': 3,
        'ingredients_total': 5,
        'missing': ['Avocado', 'Chickpeas']
    }
]

for meal in meals:
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 2, 1])
        
        with col1:
            st.markdown(f"### {meal['name']}")
            st.caption(f"You have {meal['ingredients_owned']}/{meal['ingredients_total']} ingredients")
        
        with col2:
            if meal['difficulty'] == 'Easy':
                st.success(meal['difficulty'])
            elif meal['difficulty'] == 'Medium':
                st.warning(meal['difficulty'])
            else:
                st.error(meal['difficulty'])
        
        with col3:
            st.info(f"{meal['time']} min")
        
        with col4:
            st.metric("Match", f"{meal['match']}%")
            st.progress(meal['match'] / 100)
        
        with col5:
            if st.button("View Recipe", key=f"view_{meal['name']}"):
                st.session_state[f'show_recipe_{meal["name"]}'] = True
        
        if st.session_state.get(f'show_recipe_{meal["name"]}', False):
            st.markdown("**Missing Ingredients:**")
            for missing in meal['missing']:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.write(f"• {missing}")
                with col_b:
                    if st.button("Add", key=f"add_{meal['name']}_{missing}"):
                        st.success(f"Added {missing} to grocery list!")
            
            if st.button("Add to Meal Plan", key=f"plan_{meal['name']}"):
                st.success(f"Added {meal['name']} to your meal plan!")
        
        st.markdown("---")

st.markdown("### Cost-Effective Options")

st.info("**Save $8.50 this week!** Try 'Chicken Fried Rice' and 'Vegetable Stir-Fry' - you already have most ingredients!")