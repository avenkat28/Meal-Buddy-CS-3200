import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app.src.modules.nav import SideBarLinks

st.set_page_config(page_title="Nutrition Progress", page_icon="📊", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("⚠️ Please login from the home page first")
    st.stop()

st.title("📊 Nutrition Progress Tracker")
st.markdown("Monitor your progress toward your health goals")

user_id = st.session_state.get('user_id', 1)

st.markdown("---")

st.markdown("### 🎯 This Week's Goals")

goal_col1, goal_col2, goal_col3, goal_col4 = st.columns(4)

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

st.markdown("### 📅 Daily Nutrition Breakdown")

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

st.markdown("### 🥗 Macronutrient Breakdown (This Week)")

macro_col1, macro_col2 = st.columns(2)

with macro_col1:
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

    st.write("**Protein:** 82g / day")
    st.progress(0.82)
    st.caption("Target: 75g ✅")

    st.write("**Carbs:** 185g / day")
    st.progress(0.93)
    st.caption("Target: 200g")

    st.write("**Fat:** 56g / day")
    st.progress(0.93)
    st.caption("Target: 60g")

st.markdown("---")

st.markdown("### 📋 This Week's Summary")

achievements = [
    "✅ Stayed under calorie goal 6/7 days",
    "✅ Averaged 60g protein per meal",
    "✅ 86% whole foods, 14% processed",
    "⚠️ Only 2 servings of vegetables on Tuesday"
]

for achievement in achievements:
    st.write(achievement)

st.markdown("---")

st.success("🎉 **You're doing amazing! Keep it up!**")