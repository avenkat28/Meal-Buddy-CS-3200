import streamlit as st
import pandas as pd
import plotly.express as px
from app.src.modules.nav import SideBarLinks
from app.src.modules.api_client import api

st.set_page_config(page_title="Cost Analysis", page_icon="💰", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("Please login from the home page first")
    st.stop()

st.title("Meal Cost Analysis")
st.markdown("Track and optimize your food budget")

user_id = st.session_state.get('user_id', 2)

st.markdown("---")

# Fetch cost metrics
cost_metrics = api.get(f"/users/{user_id}/costs/metrics")

col1, col2, col3, col4 = st.columns(4)

if cost_metrics:
    with col1:
        weekly = cost_metrics.get('weekly_cost', 0)
        weekly_change = cost_metrics.get('weekly_change', 0)
        st.metric("Weekly Cost", f"${weekly:.2f}", f"-${abs(weekly_change):.2f}")

    with col2:
        avg_meal = cost_metrics.get('avg_cost_per_meal', 0)
        meal_change = cost_metrics.get('meal_change', 0)
        st.metric("Avg Cost/Meal", f"${avg_meal:.2f}", f"-${abs(meal_change):.2f}")

    with col3:
        monthly = cost_metrics.get('monthly_projection', 0)
        monthly_change = cost_metrics.get('monthly_change', 0)
        st.metric("Monthly Projection", f"${monthly:.2f}", f"-${abs(monthly_change):.2f}")

    with col4:
        remaining = cost_metrics.get('budget_remaining', 0)
        st.metric("Budget Remaining", f"${remaining:.2f}", "")
else:
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

# Fetch meal costs
meal_costs_data = api.get(f"/users/{user_id}/costs/meals")

if meal_costs_data and len(meal_costs_data) > 0:
    df_meals = pd.DataFrame(meal_costs_data)

    fig = px.bar(df_meals, x='meal_name', y='cost', title='Cost per Recipe', color='cost',
                 color_continuous_scale='Greens')
    st.plotly_chart(fig, use_container_width=True)
else:
    # Fallback data
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

# Fetch optimization tips
tips_data = api.get(f"/users/{user_id}/costs/tips")

tip_col1, tip_col2 = st.columns(2)

if tips_data and len(tips_data) > 0:
    savings_tips = [tip for tip in tips_data if tip.get('type') == 'savings']
    success_tips = [tip for tip in tips_data if tip.get('type') == 'success']

    with tip_col1:
        for tip in savings_tips:
            st.info(f"**{tip.get('title', '')}:** {tip.get('message', '')}")

    with tip_col2:
        for tip in success_tips:
            st.success(f"**{tip.get('title', '')}:** {tip.get('message', '')}")
else:
    with tip_col1:
        st.info("**Savings Opportunity:** Buy chicken breast in bulk at Costco to save $4.50/week")
        st.info("**Seasonal Tip:** Bell peppers are 30% cheaper at farmers markets this week")

    with tip_col2:
        st.success("**Well Done:** You're using olive oil efficiently across 4 meals")
        st.success("**Great Choice:** Quinoa provides best protein/$ ratio in your plan")

st.markdown("---")

st.markdown("### Detailed Cost Report")

# Fetch detailed costs
detailed_costs_data = api.get(f"/users/{user_id}/costs/detailed")

if detailed_costs_data and len(detailed_costs_data) > 0:
    df_detailed = pd.DataFrame(detailed_costs_data)
    st.dataframe(df_detailed, use_container_width=True, hide_index=True)

    total_cost = sum([item.get('total_cost', 0) for item in detailed_costs_data])
    total_meals = detailed_costs_data[0].get('projected_meals', 7) if detailed_costs_data else 7
    avg_cost = total_cost / total_meals if total_meals > 0 else 0

    st.markdown(f"**Total Weekly Grocery Cost:** ${total_cost:.2f}")
    st.markdown(f"**Projected Meals from Ingredients:** {total_meals} meals")
    st.markdown(f"**Average Cost per Meal:** ${avg_cost:.2f}")
else:
    # Fallback data
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
