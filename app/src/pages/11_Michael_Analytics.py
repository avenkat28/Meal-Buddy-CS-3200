import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from app.src.modules.nav import SideBarLinks
from app.src.modules.api_client import api

st.set_page_config(page_title="Nutrition Analytics", page_icon="📈", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("Please login from the home page first")
    st.stop()

st.title("Nutrition Analytics")
st.markdown("Deep dive into your dietary trends")

user_id = st.session_state.get('user_id', 2)

st.markdown("---")

date_col1, date_col2 = st.columns(2)

with date_col1:
    start_date = st.date_input("Start Date")

with date_col2:
    end_date = st.date_input("End Date")

st.markdown("---")

st.markdown("### Macro Trends")

# Fetch macro trends data from API
macro_trends = api.get(f"/users/{user_id}/analytics/macro_trends",
                       params={"start_date": str(start_date), "end_date": str(end_date)})

if macro_trends and len(macro_trends) > 0:
    dates = [item.get('day', '') for item in macro_trends]
    protein = [item.get('protein', 0) for item in macro_trends]
    carbs = [item.get('carbs', 0) for item in macro_trends]
    fat = [item.get('fat', 0) for item in macro_trends]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dates, y=protein, mode='lines+markers', name='Protein (g)', line=dict(color='#FF6B6B')))
    fig.add_trace(go.Scatter(x=dates, y=carbs, mode='lines+markers', name='Carbs (g)', line=dict(color='#4ECDC4')))
    fig.add_trace(go.Scatter(x=dates, y=fat, mode='lines+markers', name='Fat (g)', line=dict(color='#FFE66D')))

    fig.update_layout(title="Daily Macronutrient Intake", xaxis_title="Day", yaxis_title="Grams", height=400)

    st.plotly_chart(fig, use_container_width=True)
else:
    # Fallback data
    dates = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    protein = [78, 85, 72, 81, 88, 82, 82]
    carbs = [182, 195, 178, 188, 202, 192, 185]
    fat = [52, 58, 48, 55, 61, 56, 56]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dates, y=protein, mode='lines+markers', name='Protein (g)', line=dict(color='#FF6B6B')))
    fig.add_trace(go.Scatter(x=dates, y=carbs, mode='lines+markers', name='Carbs (g)', line=dict(color='#4ECDC4')))
    fig.add_trace(go.Scatter(x=dates, y=fat, mode='lines+markers', name='Fat (g)', line=dict(color='#FFE66D')))

    fig.update_layout(title="Daily Macronutrient Intake", xaxis_title="Day", yaxis_title="Grams", height=400)

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.markdown("### Meal Type Distribution")

# Fetch meal type distribution
meal_dist = api.get(f"/users/{user_id}/analytics/meal_distribution")

pie_col1, pie_col2 = st.columns(2)

with pie_col1:
    if meal_dist:
        labels = ['Plant-Based', 'Meat-Based']
        values = [meal_dist.get('plant_based_pct', 64), meal_dist.get('meat_based_pct', 36)]
    else:
        labels = ['Plant-Based', 'Meat-Based']
        values = [64, 36]

    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig_pie.update_layout(title="Plant vs Meat Based Meals")
    st.plotly_chart(fig_pie, use_container_width=True)

with pie_col2:
    st.markdown("#### Key Stats")

    if meal_dist:
        total_meals = meal_dist.get('total_meals', 30)
        plant_count = meal_dist.get('plant_based_count', 19)
        meat_count = meal_dist.get('meat_based_count', 11)
        plant_pct = meal_dist.get('plant_based_pct', 64)
        target = meal_dist.get('target_pct', 70)

        st.write(f"**Total Meals Analyzed:** {total_meals}")
        st.write(f"**Plant-Based:** {plant_count} meals ({plant_pct}%)")
        st.write(f"**Meat-Based:** {meat_count} meals ({100 - plant_pct}%)")
        st.write(f"**Target:** {target}% plant-based")
        st.progress(plant_pct / 100)
    else:
        st.write("**Total Meals Analyzed:** 30")
        st.write("**Plant-Based:** 19 meals (64%)")
        st.write("**Meat-Based:** 11 meals (36%)")
        st.write("**Target:** 70% plant-based")
        st.progress(0.64)

st.markdown("---")

st.markdown("### Weekly Summary")

# Fetch weekly summary
weekly_summary = api.get(f"/users/{user_id}/analytics/weekly_summary")

if weekly_summary:
    summary_data = {
        'Metric': ['Avg Calories', 'Avg Protein', 'Avg Carbs', 'Avg Fat', 'Avg Fiber'],
        'Actual': [
            weekly_summary.get('avg_calories', 0),
            weekly_summary.get('avg_protein', 0),
            weekly_summary.get('avg_carbs', 0),
            weekly_summary.get('avg_fat', 0),
            weekly_summary.get('avg_fiber', 0)
        ],
        'Target': [
            weekly_summary.get('target_calories', 0),
            weekly_summary.get('target_protein', 0),
            weekly_summary.get('target_carbs', 0),
            weekly_summary.get('target_fat', 0),
            weekly_summary.get('target_fiber', 0)
        ],
        'Variance': [
            weekly_summary.get('calories_variance', ''),
            weekly_summary.get('protein_variance', ''),
            weekly_summary.get('carbs_variance', ''),
            weekly_summary.get('fat_variance', ''),
            weekly_summary.get('fiber_variance', '')
        ]
    }
else:
    summary_data = {
        'Metric': ['Avg Calories', 'Avg Protein', 'Avg Carbs', 'Avg Fat', 'Avg Fiber'],
        'Actual': [1642, 82, 185, 56, 32],
        'Target': [1800, 75, 200, 60, 28],
        'Variance': ['-8.8%', '+9.3%', '-7.5%', '-6.7%', '+14.3%']
    }

df = pd.DataFrame(summary_data)
st.dataframe(df, use_container_width=True, hide_index=True)
