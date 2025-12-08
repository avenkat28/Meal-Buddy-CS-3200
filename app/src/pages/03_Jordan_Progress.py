import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app.src.modules.nav import SideBarLinks
from app.src.modules.api_client import api

st.set_page_config(page_title="Nutrition Progress", page_icon="📊", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("Please login from the home page first")
    st.stop()

st.title("Nutrition Progress Tracker")
st.markdown("Monitor your progress toward your health goals")

user_id = st.session_state.get('user_id', 1)

st.markdown("---")

st.markdown("### This Week's Goals")

# Fetch goals data from API
goals_data = api.get(f"/users/{user_id}/goals/progress")

goal_col1, goal_col2, goal_col3, goal_col4 = st.columns(4)

if goals_data:
    with goal_col1:
        cal_current = goals_data.get('calories_current', 0)
        cal_target = goals_data.get('calories_target', 0)
        cal_pct = int((cal_current / cal_target * 100)) if cal_target > 0 else 0
        st.metric("Calorie Goal", f"{cal_current:,} / {cal_target:,}", f"{cal_pct}%")
        st.progress(min(cal_pct / 100, 1.0))

    with goal_col2:
        protein_current = goals_data.get('protein_current', 0)
        protein_target = goals_data.get('protein_target', 0)
        protein_pct = int((protein_current / protein_target * 100)) if protein_target > 0 else 0
        st.metric("Protein Intake", f"{protein_current}g / {protein_target}g", f"{protein_pct}%")
        st.progress(min(protein_pct / 100, 1.0))

    with goal_col3:
        water_current = goals_data.get('water_current', 0)
        water_target = goals_data.get('water_target', 0)
        water_pct = int((water_current / water_target * 100)) if water_target > 0 else 0
        st.metric("Water Intake", f"{water_current} / {water_target} cups", f"{water_pct}%")
        st.progress(min(water_pct / 100, 1.0))

    with goal_col4:
        meals_current = goals_data.get('healthy_meals_current', 0)
        meals_target = goals_data.get('healthy_meals_target', 0)
        meals_pct = int((meals_current / meals_target * 100)) if meals_target > 0 else 0
        st.metric("Healthy Meals", f"{meals_current} / {meals_target} meals", f"{meals_pct}%")
        st.progress(min(meals_pct / 100, 1.0))
else:
    with goal_col1:
        st.metric("Calorie Goal", "8,400 / 10,500", "80%")
        st.progress(0.80)
    with goal_col2:
        st.metric("Protein Intake", "420g / 525g", "80%")
        st.progress(0.80)
    with goal_col3:
        st.metric("Water Intake", "48 / 56 cups", "86%")
        st.progress(0.86)
    with goal_col4:
        st.metric("Healthy Meals", "12 / 14 meals", "86%")
        st.progress(0.86)

st.markdown("---")

st.markdown("### Daily Nutrition Breakdown")

# Fetch daily nutrition data
nutrition_data = api.get(f"/users/{user_id}/nutrition/daily")

if nutrition_data and len(nutrition_data) > 0:
    dates = [item.get('day', '') for item in nutrition_data]
    calories = [item.get('calories', 0) for item in nutrition_data]
    target_cal = nutrition_data[0].get('target_calories', 1500)

    fig_calories = go.Figure()

    fig_calories.add_trace(go.Scatter(
        x=dates,
        y=calories,
        mode='lines+markers',
        name='Actual',
        line=dict(color='#4CAF50', width=3),
        marker=dict(size=10)
    ))

    fig_calories.add_trace(go.Scatter(
        x=dates,
        y=[target_cal] * len(dates),
        mode='lines',
        name='Goal',
        line=dict(color='red', width=2, dash='dash')
    ))

    fig_calories.update_layout(
        title="Daily Calorie Intake",
        xaxis_title="Day",
        yaxis_title="Calories",
        height=400,
        hovermode='x unified'
    )

    st.plotly_chart(fig_calories, use_container_width=True)
else:
    # Fallback chart
    dates = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    calories = [1520, 1680, 1450, 1590, 1720, 1610, 1450]

    fig_calories = go.Figure()

    fig_calories.add_trace(go.Scatter(
        x=dates,
        y=calories,
        mode='lines+markers',
        name='Actual',
        line=dict(color='#4CAF50', width=3),
        marker=dict(size=10)
    ))

    fig_calories.add_trace(go.Scatter(
        x=dates,
        y=[1500] * len(dates),
        mode='lines',
        name='Goal',
        line=dict(color='red', width=2, dash='dash')
    ))

    fig_calories.update_layout(
        title="Daily Calorie Intake",
        xaxis_title="Day",
        yaxis_title="Calories",
        height=400,
        hovermode='x unified'
    )

    st.plotly_chart(fig_calories, use_container_width=True)

st.markdown("---")

st.markdown("### Macronutrient Breakdown (This Week)")

# Fetch macro data
macro_data = api.get(f"/users/{user_id}/nutrition/macros")

macro_col1, macro_col2 = st.columns(2)

with macro_col1:
    if macro_data:
        labels = ['Protein', 'Carbs', 'Fat']
        values = [
            macro_data.get('protein_pct', 30),
            macro_data.get('carbs_pct', 45),
            macro_data.get('fat_pct', 25)
        ]
        colors = ['#FF6B6B', '#4ECDC4', '#FFE66D']

        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            hole=.3
        )])

        fig_pie.update_layout(title="Macro Distribution (%)")
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        labels = ['Protein', 'Carbs', 'Fat']
        values = [30, 45, 25]
        colors = ['#FF6B6B', '#4ECDC4', '#FFE66D']

        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            hole=.3
        )])

        fig_pie.update_layout(title="Macro Distribution (%)")
        st.plotly_chart(fig_pie, use_container_width=True)

with macro_col2:
    st.markdown("#### Weekly Averages")

    if macro_data:
        protein_avg = macro_data.get('protein_avg', 82)
        protein_target = macro_data.get('protein_target', 75)
        st.write(f"**Protein:** {protein_avg}g / day")
        st.progress(min(protein_avg / protein_target, 1.0))
        st.caption(f"Target: {protein_target}g" + (" - On Track" if protein_avg >= protein_target else ""))

        carbs_avg = macro_data.get('carbs_avg', 185)
        carbs_target = macro_data.get('carbs_target', 200)
        st.write(f"**Carbs:** {carbs_avg}g / day")
        st.progress(min(carbs_avg / carbs_target, 1.0))
        st.caption(f"Target: {carbs_target}g")

        fat_avg = macro_data.get('fat_avg', 56)
        fat_target = macro_data.get('fat_target', 60)
        st.write(f"**Fat:** {fat_avg}g / day")
        st.progress(min(fat_avg / fat_target, 1.0))
        st.caption(f"Target: {fat_target}g")
    else:
        st.write("**Protein:** 82g / day")
        st.progress(0.82)
        st.caption("Target: 75g - On Track")

        st.write("**Carbs:** 185g / day")
        st.progress(0.93)
        st.caption("Target: 200g")

        st.write("**Fat:** 56g / day")
        st.progress(0.93)
        st.caption("Target: 60g")

st.markdown("---")

st.markdown("### This Week's Summary")

# Fetch achievements
achievements_data = api.get(f"/users/{user_id}/nutrition/achievements")

if achievements_data:
    for achievement in achievements_data:
        status = achievement.get('status', 'complete')
        text = achievement.get('text', '')
        prefix = "✓" if status == 'complete' else "!"
        st.write(f"{prefix} {text}")
else:
    achievements = [
        "✓ Stayed under calorie goal 6/7 days",
        "✓ Averaged 60g protein per meal",
        "✓ 86% whole foods, 14% processed",
        "! Only 2 servings of vegetables on Tuesday"
    ]

    for achievement in achievements:
        st.write(achievement)

st.markdown("---")

st.success("**You're doing amazing! Keep it up!**")
