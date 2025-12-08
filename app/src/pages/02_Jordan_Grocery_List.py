import streamlit as st
import pandas as pd
from modules.api_client import api
from modules.nav import SideBarLinks

st.set_page_config(page_title="Grocery List", page_icon="🛒", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("Please login from the home page first")
    st.stop()

st.title("Grocery List")
st.markdown("Your shopping list for this week's meals")

plan_id = 1

st.markdown("---")

col1, col2, col3 = st.columns(3)

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

grocery_data = {
    'Proteins': [
        {'name': 'Chicken Breast', 'quantity': '2 lbs', 'owned': False},
        {'name': 'Salmon Fillet', 'quantity': '1.5 lbs', 'owned': False},
        {'name': 'Ground Turkey', 'quantity': '1 lb', 'owned': True},
        {'name': 'Shrimp', 'quantity': '12 oz', 'owned': False}
    ],
    'Vegetables': [
        {'name': 'Broccoli', 'quantity': '2 heads', 'owned': True},
        {'name': 'Bell Peppers', 'quantity': '4 pieces', 'owned': False},
        {'name': 'Spinach', 'quantity': '1 bag', 'owned': False},
        {'name': 'Tomatoes', 'quantity': '6 pieces', 'owned': True}
    ],
    'Grains': [
        {'name': 'Quinoa', 'quantity': '2 cups', 'owned': False},
        {'name': 'Brown Rice', 'quantity': '3 cups', 'owned': True},
        {'name': 'Whole Wheat Pasta', 'quantity': '1 lb', 'owned': False},
        {'name': 'Oats', 'quantity': '2 lbs', 'owned': True}
    ],
    'Dairy': [
        {'name': 'Greek Yogurt', 'quantity': '32 oz', 'owned': False},
        {'name': 'Milk', 'quantity': '1 gallon', 'owned': False},
        {'name': 'Cheese', 'quantity': '8 oz', 'owned': True}
    ],
    'Pantry': [
        {'name': 'Olive Oil', 'quantity': '1 bottle', 'owned': True},
        {'name': 'Soy Sauce', 'quantity': '1 bottle', 'owned': False},
        {'name': 'Honey', 'quantity': '1 jar', 'owned': True}
    ],
    'Fruits': [
        {'name': 'Bananas', 'quantity': '6 pieces', 'owned': False},
        {'name': 'Apples', 'quantity': '5 pieces', 'owned': False},
        {'name': 'Berries', 'quantity': '2 containers', 'owned': True}
    ]
}

for category, items in grocery_data.items():
    st.markdown(f"### {category}")

    for item in items:
        if search.lower() in item['name'].lower() or search == "":
            if not (show_owned and item['owned']):
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                with col1:
                    st.write(f"**{item['name']}**")

                with col2:
                    st.write(f"{item['quantity']}")

                with col3:
                    owned = st.checkbox("Own", key=f"own_{category}_{item['name']}", value=item['owned'])

                with col4:
                    if st.button("Add to Inventory", key=f"inventory_{category}_{item['name']}"):
                        st.success(f"Added {item['name']} to inventory")

    st.markdown("---")

st.markdown("### Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("Email List", use_container_width=True):
        st.success("Grocery list sent to your email!")

with action_col2:
    if st.button("Download PDF", use_container_width=True):
        st.info("PDF download feature coming soon")

with action_col3:
    if st.button("Send to Phone", use_container_width=True):
        st.success("List sent to your phone!")

st.info("Tip: You can save $12 by shopping at Market Basket instead of Whole Foods this week!")