import streamlit as st
from app.src.modules.nav import SideBarLinks
from app.src.modules.api_client import api

st.set_page_config(page_title="Meal Suggestions", page_icon="💡", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("Please login from the home page first")
    st.stop()

st.title("Meal Suggestions")
st.markdown("Discover recipes you can make with what you have")

user_id = st.session_state.get('user_id', 3)

st.markdown("---")

st.markdown("### Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    meal_type = st.selectbox("Meal Type", ["All", "Breakfast", "Lunch", "Dinner", "Snack"])

with filter_col2:
    difficulty = st.selectbox("Difficulty", ["All", "Easy", "Medium", "Hard"])

with filter_col3:
    max_time = st.slider("Max Prep Time (min)", 10, 120, 60)

st.markdown("---")

# Fetch meal suggestions based on pantry
suggestions = api.get(f"/users/{user_id}/meal_suggestions", params={
    "meal_type": meal_type if meal_type != "All" else None,
    "difficulty": difficulty if difficulty != "All" else None,
    "max_time": max_time
})

if suggestions and len(suggestions) > 0:
    for meal in suggestions:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

            with col1:
                st.markdown(f"### {meal.get('meal_name', '')}")
                description = meal.get('description', '')
                st.write(description if description else "Delicious and nutritious meal")

            with col2:
                match_pct = meal.get('ingredient_match_pct', 0)
                st.metric("Match", f"{match_pct}%")
                missing = meal.get('missing_ingredients', 0)
                st.caption(f"{missing} ingredients to buy")

            with col3:
                prep_time = meal.get('prep_time', 0)
                st.metric("Prep Time", f"{prep_time} min")
                difficulty_level = meal.get('difficulty', 'Medium')
                st.caption(f"Difficulty: {difficulty_level}")

            with col4:
                calories = meal.get('calories', 0)
                st.metric("Calories", str(calories))
                st.write("")
                if st.button("View Recipe", key=f"view_{meal.get('meal_id')}"):
                    st.session_state['selected_meal_id'] = meal.get('meal_id')
                    st.switch_page("app/src/pages/23_Sarah_Recipe_Browser.py")

            # Show what you have vs need
            exp_col1, exp_col2 = st.columns(2)

            with exp_col1:
                st.write("**You Have:**")
                have_ingredients = meal.get('have_ingredients', [])
                if have_ingredients:
                    for ing in have_ingredients:
                        st.write(f"✓ {ing}")
                else:
                    st.write("✓ Chicken, ✓ Rice, ✓ Bell peppers")

            with exp_col2:
                st.write("**You Need:**")
                need_ingredients = meal.get('need_ingredients', [])
                if need_ingredients:
                    for ing in need_ingredients:
                        st.write(f"○ {ing}")
                else:
                    st.write("○ Soy sauce, ○ Garlic")

            st.markdown("---")
else:
    # Fallback suggestions
    st.markdown("### Grilled Chicken Salad")
    st.write("Fresh and healthy salad with grilled chicken")

    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

    with col2:
        st.metric("Match", "85%")
        st.caption("2 ingredients to buy")

    with col3:
        st.metric("Prep Time", "25 min")
        st.caption("Difficulty: Easy")

    with col4:
        st.metric("Calories", "450")
        st.write("")
        if st.button("View Recipe", key="view_1"):
            st.info("Recipe details")

    exp_col1, exp_col2 = st.columns(2)

    with exp_col1:
        st.write("**You Have:**")
        st.write("✓ Chicken breast")
        st.write("✓ Lettuce")
        st.write("✓ Cherry tomatoes")
        st.write("✓ Olive oil")

    with exp_col2:
        st.write("**You Need:**")
        st.write("○ Balsamic vinegar")
        st.write("○ Feta cheese")

    st.markdown("---")

    st.markdown("### Quinoa Power Bowl")
    st.write("Nutrient-packed bowl with quinoa and vegetables")

    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

    with col2:
        st.metric("Match", "78%")
        st.caption("3 ingredients to buy")

    with col3:
        st.metric("Prep Time", "35 min")
        st.caption("Difficulty: Medium")

    with col4:
        st.metric("Calories", "520")
        st.write("")
        if st.button("View Recipe", key="view_2"):
            st.info("Recipe details")

    exp_col1, exp_col2 = st.columns(2)

    with exp_col1:
        st.write("**You Have:**")
        st.write("✓ Quinoa")
        st.write("✓ Bell peppers")
        st.write("✓ Black beans")

    with exp_col2:
        st.write("**You Need:**")
        st.write("○ Avocado")
        st.write("○ Lime")
        st.write("○ Cilantro")

    st.markdown("---")

st.info("Tip: Update your pantry to get more accurate suggestions!")
