import streamlit as st
import pandas as pd
import plotly.express as px
from modules.nav import SideBarLinks

st.set_page_config(page_title="Cost Analysis", page_icon="💰", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("Please login from the home page first")
    st.stop()

st.title("Meal Cost Analysis")
st.markdown("Track and optimize your food budget")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Weekly Cost", "$43.85", "-$5.15")

with col2:
    st.metric("Avg Cost/Meal", "$8.77", "-$0.50")

with col3:
    st.metric("Monthly Projection", "$187.40", "-$22.00")

with col4:
    st.metric("Budget Remaining", "$112.60", "")

st.markdown("---")

st.markdown("### Cost Breakdown by Meal")

meal_costs = {
    'Meal': ['Grilled Chicken Salad', 'Salmon with Quinoa', 'Chicken Rice', 'Pasta Primavera', 'Shrimp Teriyaki'],
    'Cost': [7.25, 12.40, 6.80, 5.90, 11.50],
    'Servings': [1, 1, 1, 1, 1]
}

df_meals = pd.DataFrame(meal_costs)

fig = px.bar(df_meals, x='Meal', y='Cost', title='Cost per Recipe', color='Cost',
             color_continuous_scale='Greens')
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.markdown("### Cost Optimization Tips")

tip_col1, tip_col2 = st.columns(2)

with tip_col1:
    st.info("**Savings Opportunity:** Buy chicken breast in bulk at Costco to save $4.50/week")
    st.info("**Seasonal Tip:** Bell peppers are 30% cheaper at farmers markets this week")

with tip_col2:
    st.success("**Well Done:** You're using olive oil efficiently across 4 meals")
    st.success("**Great Choice:** Quinoa provides best protein/$ ratio in your plan")

st.markdown("---")

st.markdown("### Detailed Cost Report")

detailed_costs = {
    'Ingredient': ['Chicken Breast', 'Salmon Fillet', 'Quinoa', 'Olive Oil', 'Bell Peppers'],
    'Quantity': ['3 lbs', '1.5 lbs', '2 cups', '1 bottle', '4 pieces'],
    'Unit Price': ['$4.99/lb', '$12.99/lb', '$5.99/lb', '$8.99', '$1.50 each'],
    'Total': ['$14.97', '$19.49', '$11.98', '$8.99', '$6.00']
}

df_detailed = pd.DataFrame(detailed_costs)
st.dataframe(df_detailed, use_container_width=True, hide_index=True)

st.markdown(f"**Total Weekly Grocery Cost:** $61.43")
st.markdown(f"**Projected Meals from Ingredients:** 7 meals")
st.markdown(f"**Average Cost per Meal:** $8.77")