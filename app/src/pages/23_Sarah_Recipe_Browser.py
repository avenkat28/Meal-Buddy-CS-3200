import streamlit as st
import pandas as pd
from modules.api_client import api
from modules.nav import SideBarLinks

st.set_page_config(page_title="Recipe Browser", page_icon="📖", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("⚠️ Please login from the home page first")
    st.stop()

st.title("📖 Recipe Browser")
st.markdown("Explore delicious meal ideas")

st.markdown("---")

search_col1, search_col2 = st.columns([3, 1])

with search_col1:
    search = st.text_input("🔍 Search recipes", placeholder="Try 'chicken', 'pasta', 'healthy'...")

with search_col2:
    category = st.selectbox("Category", ["All", "Breakfast", "Lunch", "Dinner", "Snacks"])

st.markdown("---")

st.markdown("### 🔥 Popular This Week")

popular_recipes = [
    {
        'name': 'Shrimp Teriyaki',
        'difficulty': 'Medium',
        'time': 30,
        'calories': 550,
        'rating': 4.8,
        'image': '🍤'
    },
    {
        'name': 'Grilled Chicken Salad',
        'difficulty': 'Easy',
        'time': 20,
        'calories': 450,
        'rating': 4.6,
        'image': '🥗'
    },
    {
        'name': 'Salmon with Quinoa',
        'difficulty': 'Medium',
        'time': 35,
        'calories': 520,
        'rating': 4.9,
        'image': '🐟'
    }
]

cols = st.columns(3)

for idx, recipe in enumerate(popular_recipes):
    with cols[idx]:
        st.markdown(f"<div style='text-align: center; font-size: 4rem;'>{recipe['image']}</div>", unsafe_allow_html=True)
        st.markdown(f"### {recipe['name']}")
        st.write(f"⭐ {recipe['rating']} | ⏰ {recipe['time']} min | 🔥 {recipe['calories']} cal")
        st.write(f"**Difficulty:** {recipe['difficulty']}")
        if st.button("View Details", key=f"popular_{recipe['name']}"):
            st.session_state['selected_recipe'] = recipe['name']

st.markdown("---")

st.markdown("### 📚 All Recipes")

all_recipes = [
    {'name': 'Chicken Fried Rice', 'difficulty': 'Easy', 'time': 25, 'calories': 380, 'category': 'Dinner'},
    {'name': 'Greek Yogurt Parfait', 'difficulty': 'Easy', 'time': 5, 'calories': 320, 'category': 'Breakfast'},
    {'name': 'Turkey Wrap', 'difficulty': 'Easy', 'time': 10, 'calories': 380, 'category': 'Lunch'},
    {'name': 'Pasta Primavera', 'difficulty': 'Medium', 'time': 30, 'calories': 490, 'category': 'Dinner'},
    {'name': 'Smoothie Bowl', 'difficulty': 'Easy', 'time': 10, 'calories': 290, 'category': 'Breakfast'},
    {'name': 'BBQ Chicken', 'difficulty': 'Medium', 'time': 45, 'calories': 560, 'category': 'Dinner'},
    {'name': 'Caesar Salad', 'difficulty': 'Easy', 'time': 15, 'calories': 390, 'category': 'Lunch'},
    {'name': 'Avocado Toast', 'difficulty': 'Easy', 'time': 5, 'calories': 340, 'category': 'Breakfast'}
]

for recipe in all_recipes:
    if search.lower() in recipe['name'].lower() or search == "":
        if category == "All" or recipe['category'] == category:
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            
            with col1:
                st.write(f"**{recipe['name']}**")
                st.caption(recipe['category'])
            
            with col2:
                if recipe['difficulty'] == 'Easy':
                    st.success(recipe['difficulty'])
                else:
                    st.warning(recipe['difficulty'])
            
            with col3:
                st.write(f"⏰ {recipe['time']} min")
            
            with col4:
                st.write(f"🔥 {recipe['calories']} cal")
            
            with col5:
                if st.button("View", key=f"recipe_{recipe['name']}"):
                    st.session_state['selected_recipe'] = recipe['name']
            
            st.markdown("---")

if 'selected_recipe' in st.session_state and st.session_state['selected_recipe']:
    st.markdown("### 📋 Recipe Details")
    
    recipe_name = st.session_state['selected_recipe']
    
    st.markdown(f"## {recipe_name}")
    
    detail_col1, detail_col2 = st.columns([2, 1])
    
    with detail_col1:
        st.markdown("#### Ingredients")
        ingredients = [
            "12 oz Large Shrimp",
            "1/4 cup Teriyaki Sauce",
            "2 cups White Rice",
            "1 cup Broccoli Florets",
            "2 tbsp Sesame Oil",
            "1 tsp Sesame Seeds"
        ]
        for ingredient in ingredients:
            st.write(f"• {ingredient}")
        
        st.markdown("#### Recipe Steps")
        steps = [
            "Cook rice according to package directions and set aside",
            "Sauté shrimp in sesame oil until pink",
            "Add broccoli and teriyaki sauce, cook for 5 minutes",
            "Serve over rice and garnish with sesame seeds"
        ]
        for idx, step in enumerate(steps, 1):
            st.write(f"{idx}. {step}")
    
    with detail_col2:
        st.markdown("#### Nutritional Facts")
        st.metric("Calories", "550")
        st.metric("Protein", "32g")
        st.metric("Carbs", "48g")
        st.metric("Fat", "22g")
        
        st.markdown("---")
        
        if st.button("➕ Add to Meal Plan", use_container_width=True):
            st.success(f"Added {recipe_name} to your meal plan!")
        
        if st.button("🛒 Add Ingredients to List", use_container_width=True):
            st.success("Ingredients added to grocery list!")