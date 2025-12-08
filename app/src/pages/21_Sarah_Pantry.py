import streamlit as st
import pandas as pd
from app.src.modules.nav import SideBarLinks
from app.src.modules.api_client import api

st.set_page_config(page_title="Pantry Manager", page_icon="🥫", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("Please login from the home page first")
    st.stop()

st.title("Pantry Manager")
st.markdown("Track what ingredients you have at home")

user_id = st.session_state.get('user_id', 3)

st.markdown("---")

# Fetch pantry stats
pantry_stats = api.get(f"/users/{user_id}/inventory/stats")

col1, col2, col3, col4 = st.columns(4)

if pantry_stats:
    with col1:
        total = pantry_stats.get('total_items', 0)
        st.metric("Total Items", str(total))

    with col2:
        expiring = pantry_stats.get('expiring_soon', 0)
        st.metric("Expiring Soon", f"{expiring} items")

    with col3:
        need = pantry_stats.get('items_to_buy', 0)
        st.metric("Need to Buy", f"{need} items")

    with col4:
        value = pantry_stats.get('estimated_value', 0)
        st.metric("Est. Value", f"${value:.2f}")
else:
    with col1:
        st.metric("Total Items", "28")
    with col2:
        st.metric("Expiring Soon", "4 items")
    with col3:
        st.metric("Need to Buy", "6 items")
    with col4:
        st.metric("Est. Value", "$85.50")

st.markdown("---")

filter_col1, filter_col2, filter_col3 = st.columns([2, 1, 1])

with filter_col1:
    search = st.text_input("Search ingredients", "")

with filter_col2:
    category_filter = st.selectbox("Category", ["All", "Produce", "Protein", "Grains", "Dairy", "Spices"])

with filter_col3:
    status_filter = st.selectbox("Status", ["All", "In Stock", "Low Stock", "Out of Stock"])

st.markdown("---")

# Fetch pantry items
pantry_items = api.get(f"/users/{user_id}/inventory")

if pantry_items and len(pantry_items) > 0:
    # Group by category
    items_by_category = {}
    for item in pantry_items:
        category = item.get('category', 'Other')
        if category not in items_by_category:
            items_by_category[category] = []
        items_by_category[category].append(item)

    # Filter by selected category
    if category_filter != "All":
        items_by_category = {k: v for k, v in items_by_category.items() if k == category_filter}

    for category, items in items_by_category.items():
        st.markdown(f"### {category}")

        for item in items:
            ingredient_name = item.get('ingredient_name', '')

            # Apply search filter
            if search.lower() in ingredient_name.lower() or search == "":
                # Apply status filter
                owned = item.get('owned', False)
                quantity = item.get('quantity', 0)

                status = "In Stock" if owned and quantity > 0 else "Out of Stock"
                if owned and quantity <= 2:
                    status = "Low Stock"

                if status_filter == "All" or status == status_filter:
                    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])

                    with col1:
                        st.write(f"**{ingredient_name}**")

                    with col2:
                        unit = item.get('unit', '')
                        st.write(f"{quantity} {unit}")

                    with col3:
                        # Toggle owned status
                        new_owned = st.checkbox(
                            "Own",
                            key=f"own_{item['inventory_id']}",
                            value=owned
                        )

                        if new_owned != owned:
                            result = api.put(f"/inventory/{item['inventory_id']}", {"owned": new_owned})
                            if result:
                                st.rerun()

                    with col4:
                        if st.button("+ Grocery", key=f"grocery_{item['inventory_id']}"):
                            result = api.post("/grocery_list", {
                                "user_id": user_id,
                                "ingredient_id": item['ingredient_id'],
                                "quantity": 1,
                                "unit": unit
                            })
                            if result:
                                st.success("Added to grocery list!")

                    with col5:
                        if st.button("Edit", key=f"edit_{item['inventory_id']}"):
                            st.info(f"Edit {ingredient_name}")

        st.markdown("---")
else:
    st.info("Your pantry is empty. Add ingredients to get started!")

st.markdown("### Add New Ingredient")

add_col1, add_col2, add_col3, add_col4 = st.columns([3, 1, 1, 1])

with add_col1:
    new_ingredient = st.text_input("Ingredient name", key="new_ing")

with add_col2:
    new_quantity = st.number_input("Quantity", min_value=0.0, value=1.0, step=0.5, key="new_qty")

with add_col3:
    new_unit = st.selectbox("Unit", ["cups", "lbs", "oz", "pieces"], key="new_unit")

with add_col4:
    st.write("")
    st.write("")
    if st.button("Add to Pantry"):
        if new_ingredient:
            result = api.post(f"/users/{user_id}/inventory", {
                "ingredient_name": new_ingredient,
                "quantity": new_quantity,
                "unit": new_unit,
                "owned": True
            })
            if result:
                st.success(f"Added {new_ingredient} to pantry!")
                st.rerun()

st.markdown("---")

st.markdown("### Recipe Suggestions Based on Your Pantry")

# Fetch meal suggestions
suggestions = api.get(f"/users/{user_id}/meal_suggestions")

if suggestions and len(suggestions) > 0:
    sug_col1, sug_col2, sug_col3 = st.columns(3)

    for idx, meal in enumerate(suggestions[:3]):
        with [sug_col1, sug_col2, sug_col3][idx]:
            st.write(f"**{meal.get('meal_name', '')}**")
            match_pct = meal.get('ingredient_match_pct', 0)
            st.write(f"{match_pct}% ingredient match")

            if st.button("View Recipe", key=f"view_{meal.get('meal_id')}"):
                st.info(f"Viewing {meal.get('meal_name')}")
else:
    sug_col1, sug_col2, sug_col3 = st.columns(3)

    with sug_col1:
        st.write("**Grilled Chicken Salad**")
        st.write("85% ingredient match")
        if st.button("View Recipe", key="view_1"):
            st.info("Recipe details")

    with sug_col2:
        st.write("**Quinoa Bowl**")
        st.write("78% ingredient match")
        if st.button("View Recipe", key="view_2"):
            st.info("Recipe details")

    with sug_col3:
        st.write("**Stir Fry**")
        st.write("72% ingredient match")
        if st.button("View Recipe", key="view_3"):
            st.info("Recipe details")
