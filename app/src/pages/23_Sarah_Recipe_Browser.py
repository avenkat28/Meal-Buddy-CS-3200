import streamlit as st
from app.src.modules.nav import SideBarLinks
from app.src.modules.api_client import api

st.set_page_config(page_title="Recipe Browser", page_icon="📖", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("Please login from the home page first")
    st.stop()

st.title("Recipe Browser")
st.markdown("Explore our collection of healthy recipes")

user_id = st.session_state.get('user_id', 3)

st.markdown("---")

# Search and filter controls
search_col1, search_col2, search_col3 = st.columns([3, 1, 1])

with search_col1:
    search_query = st.text_input("Search recipes", placeholder="Try 'chicken', 'vegan', 'quick'...")

with search_col2:
    sort_by = st.selectbox("Sort By", ["Relevance", "Calories", "Prep Time", "Rating"])

with search_col3:
    view_mode = st.radio("View", ["Grid", "List"], horizontal=True)

st.markdown("---")

# Filters in sidebar
with st.sidebar:
    st.markdown("### Filters")

    meal_type_filter = st.multiselect(
        "Meal Type",
        ["Breakfast", "Lunch", "Dinner", "Snack"]
    )

    dietary_filter = st.multiselect(
        "Dietary Preferences",
        ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "High-Protein"]
    )

    calorie_range = st.slider("Calorie Range", 0, 1000, (0, 1000))

    prep_time_max = st.slider("Max Prep Time (min)", 10, 120, 120)

    if st.button("Clear Filters"):
        st.rerun()

# Fetch recipes from API
recipes = api.get("/meals/search", params={
    "query": search_query,
    "meal_types": meal_type_filter,
    "dietary": dietary_filter,
    "min_calories": calorie_range[0],
    "max_calories": calorie_range[1],
    "max_prep_time": prep_time_max,
    "sort_by": sort_by.lower().replace(" ", "_")
})

if recipes and len(recipes) > 0:
    if view_mode == "Grid":
        # Grid view - 3 columns
        for i in range(0, len(recipes), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(recipes):
                    recipe = recipes[i + j]
                    with col:
                        st.markdown(f"#### {recipe.get('meal_name', 'Unknown')}")

                        # Recipe image placeholder
                        st.info("🍽️ Recipe Image")

                        recipe_col1, recipe_col2 = st.columns(2)
                        with recipe_col1:
                            st.caption(f"⏱️ {recipe.get('prep_time', 0)} min")
                            st.caption(f"🔥 {recipe.get('calories', 0)} cal")
                        with recipe_col2:
                            protein = recipe.get('protein', 0)
                            st.caption(f"💪 {protein}g protein")
                            difficulty = recipe.get('difficulty', 'Medium')
                            st.caption(f"📊 {difficulty}")

                        if st.button("View Details", key=f"view_{recipe.get('meal_id')}", use_container_width=True):
                            st.session_state['selected_meal_id'] = recipe.get('meal_id')
                            st.rerun()
    else:
        # List view
        for recipe in recipes:
            with st.container():
                col1, col2, col3 = st.columns([4, 2, 1])

                with col1:
                    st.markdown(f"### {recipe.get('meal_name', 'Unknown')}")
                    description = recipe.get('description', 'Delicious and nutritious meal')
                    st.write(description)

                    tags = recipe.get('tags', [])
                    if tags:
                        tag_str = " ".join([f"#{tag}" for tag in tags])
                        st.caption(tag_str)
                    else:
                        st.caption("#healthy #easy #quick")

                with col2:
                    st.metric("Calories", recipe.get('calories', 0))
                    st.metric("Prep Time", f"{recipe.get('prep_time', 0)} min")
                    protein = recipe.get('protein', 0)
                    st.metric("Protein", f"{protein}g")

                with col3:
                    st.write("")
                    st.write("")
                    if st.button("View Recipe", key=f"view_list_{recipe.get('meal_id')}"):
                        st.session_state['selected_meal_id'] = recipe.get('meal_id')
                        st.rerun()

                st.markdown("---")
else:
    # Fallback recipes
    st.markdown("### Featured Recipes")

    if view_mode == "Grid":
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### Grilled Chicken Salad")
            st.info("🍽️ Recipe Image")
            recipe_col1, recipe_col2 = st.columns(2)
            with recipe_col1:
                st.caption("⏱️ 25 min")
                st.caption("🔥 450 cal")
            with recipe_col2:
                st.caption("💪 38g protein")
                st.caption("📊 Easy")
            if st.button("View Details", key="view_1", use_container_width=True):
                st.info("Recipe details")

        with col2:
            st.markdown("#### Salmon with Quinoa")
            st.info("🍽️ Recipe Image")
            recipe_col1, recipe_col2 = st.columns(2)
            with recipe_col1:
                st.caption("⏱️ 35 min")
                st.caption("🔥 520 cal")
            with recipe_col2:
                st.caption("💪 42g protein")
                st.caption("📊 Medium")
            if st.button("View Details", key="view_2", use_container_width=True):
                st.info("Recipe details")

        with col3:
            st.markdown("#### Veggie Stir Fry")
            st.info("🍽️ Recipe Image")
            recipe_col1, recipe_col2 = st.columns(2)
            with recipe_col1:
                st.caption("⏱️ 20 min")
                st.caption("🔥 380 cal")
            with recipe_col2:
                st.caption("💪 15g protein")
                st.caption("📊 Easy")
            if st.button("View Details", key="view_3", use_container_width=True):
                st.info("Recipe details")
    else:
        # List view fallback
        st.markdown("### Grilled Chicken Salad")
        col1, col2, col3 = st.columns([4, 2, 1])
        with col1:
            st.write("Fresh and healthy salad with grilled chicken, mixed greens, and balsamic vinaigrette")
            st.caption("#healthy #protein #salad")
        with col2:
            st.metric("Calories", "450")
            st.metric("Prep Time", "25 min")
            st.metric("Protein", "38g")
        with col3:
            st.write("")
            st.write("")
            if st.button("View Recipe", key="view_list_1"):
                st.info("Recipe details")
        st.markdown("---")

# Show recipe details if one is selected
if 'selected_meal_id' in st.session_state and st.session_state['selected_meal_id']:
    st.markdown("---")
    st.markdown("### Recipe Details")

    meal_id = st.session_state['selected_meal_id']

    # Fetch detailed recipe
    recipe_details = api.get(f"/meals/{meal_id}")

    if recipe_details:
        st.markdown(f"## {recipe_details.get('meal_name', 'Unknown')}")

        detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4)

        with detail_col1:
            st.metric("Calories", recipe_details.get('calories', 0))
        with detail_col2:
            st.metric("Protein", f"{recipe_details.get('protein', 0)}g")
        with detail_col3:
            st.metric("Prep Time", f"{recipe_details.get('prep_time', 0)} min")
        with detail_col4:
            difficulty = recipe_details.get('difficulty', 'Medium')
            st.metric("Difficulty", difficulty)

        st.markdown("#### Description")
        description = recipe_details.get('description', 'Delicious meal')
        st.write(description)

        st.markdown("#### Ingredients")
        ingredients = recipe_details.get('ingredients', [])
        if ingredients:
            for ing in ingredients:
                quantity = ing.get('quantity', '')
                unit = ing.get('unit', '')
                name = ing.get('ingredient_name', '')
                st.write(f"• {quantity} {unit} {name}")
        else:
            st.write("• 1 lb Chicken breast")
            st.write("• 4 cups Mixed greens")
            st.write("• 1 cup Cherry tomatoes")
            st.write("• 2 tbsp Olive oil")
            st.write("• 2 tbsp Balsamic vinegar")

        st.markdown("#### Instructions")
        instructions = recipe_details.get('instructions', '')
        if instructions:
            st.write(instructions)
        else:
            st.write("1. Season and grill chicken breast until fully cooked")
            st.write("2. Slice chicken into strips")
            st.write("3. Toss greens with tomatoes")
            st.write("4. Add chicken on top")
            st.write("5. Drizzle with oil and vinegar")

        if st.button("Add to Meal Plan"):
            st.success(f"Added {recipe_details.get('meal_name')} to your meal plan!")

        if st.button("Close Details"):
            st.session_state['selected_meal_id'] = None
            st.rerun()
