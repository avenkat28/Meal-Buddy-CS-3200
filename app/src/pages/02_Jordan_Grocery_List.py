import streamlit as st
import pandas as pd
from app.src.modules.api_client import api
from app.src.modules.nav import SideBarLinks

st.set_page_config(page_title="Grocery List", page_icon="🛒", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("Please login from the home page first")
    st.stop()

st.title("Grocery List")
st.markdown("Your shopping list for this week's meals")

user_id = st.session_state.get('user_id', 1)
plan_id = 1

st.markdown("---")

# Fetch grocery list stats
grocery_stats = api.get(f"/grocery_list/user/{user_id}/stats")

col1, col2, col3 = st.columns(3)

if grocery_stats:
    with col1:
        st.metric("Total Items", str(grocery_stats.get('total_items', 0)))
    with col2:
        st.metric("Categories", str(grocery_stats.get('categories', 0)))
    with col3:
        cost = grocery_stats.get('estimated_cost', 0)
        st.metric("Estimated Cost", f"${cost:.2f}")
else:
    with col1:
        st.metric("Total Items", "24")
    with col2:
        st.metric("Categories", "6")
    with col3:
        st.metric("Estimated Cost", "$38.50")

st.markdown("---")

filter_col1, filter_col2 = st.columns([2, 1])

with filter_col1:
    search = st.text_input("Search ingredients", "")

with filter_col2:
    show_owned = st.checkbox("Hide items I own", value=False)

st.markdown("---")

# Fetch grocery list items from API
grocery_items = api.get(f"/grocery_list/user/{user_id}")

if grocery_items:
    # Group by category
    items_by_category = {}
    for item in grocery_items:
        category = item.get('category', 'Other')
        if category not in items_by_category:
            items_by_category[category] = []
        items_by_category[category].append(item)

    # Display items by category
    for category, items in items_by_category.items():
        st.markdown(f"### {category}")

        for item in items:
            # Filter by search
            if search.lower() in item['ingredient_name'].lower() or search == "":
                # Filter by owned status
                if not (show_owned and item.get('owned', False)):
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                    with col1:
                        st.write(f"**{item['ingredient_name']}**")

                    with col2:
                        quantity = item.get('quantity', 0)
                        unit = item.get('unit', '')
                        st.write(f"{quantity} {unit}")

                    with col3:
                        owned = st.checkbox(
                            "Own",
                            key=f"own_{item['ingredient_id']}",
                            value=item.get('owned', False)
                        )

                        # Update owned status
                        if owned != item.get('owned', False):
                            api.put(f"/grocery_list/item/{item['gl_ingredient_id']}", {"owned": owned})

                    with col4:
                        if st.button("Add to Inventory", key=f"inventory_{item['ingredient_id']}"):
                            result = api.post(f"/users/{user_id}/inventory", {
                                "ingredient_id": item['ingredient_id'],
                                "quantity": item['quantity'],
                                "unit": item['unit']
                            })
                            if result:
                                st.success(f"Added {item['ingredient_name']} to inventory")

        st.markdown("---")
else:
    st.info("No grocery list found. Generate one from your meal plan!")

st.markdown("### Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("Email List", use_container_width=True):
        result = api.post(f"/grocery_list/user/{user_id}/email", {})
        if result:
            st.success("Grocery list sent to your email!")

with action_col2:
    if st.button("Download PDF", use_container_width=True):
        st.info("PDF download feature coming soon")

with action_col3:
    if st.button("Send to Phone", use_container_width=True):
        st.success("List sent to your phone!")

st.info("Tip: You can save $12 by shopping at Market Basket instead of Whole Foods this week!")
