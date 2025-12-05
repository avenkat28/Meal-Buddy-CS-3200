import streamlit as st


def SideBarLinks():
    st.sidebar.markdown("# 🍽️ MealBuddy")
    st.sidebar.markdown("---")

    if "user_type" not in st.session_state:
        st.switch_page("Home.py")
        return

    user_type = st.session_state.get("user_type")

    if user_type == "jordan":
        st.sidebar.markdown("### 🎓 College Student")
        st.sidebar.page_link("pages/00_Jordan_Home.py", label="Dashboard", icon="📊")
        st.sidebar.page_link("pages/01_Jordan_Weekly_Planner.py", label="Weekly Planner", icon="📅")
        st.sidebar.page_link("pages/02_Jordan_Grocery_List.py", label="Grocery List", icon="🛒")
        st.sidebar.page_link("pages/03_Jordan_Progress.py", label="Progress", icon="📈")

    elif user_type == "michael":
        st.sidebar.markdown("### 📊 Data Analyst")
        st.sidebar.page_link("pages/10_Michael_Home.py", label="Dashboard", icon="📊")
        st.sidebar.page_link("pages/11_Michael_Analytics.py", label="Analytics", icon="📈")
        st.sidebar.page_link("pages/12_Michael_Export_Data.py", label="Export Data", icon="📤")
        st.sidebar.page_link("pages/13_Michael_Cost_Analysis.py", label="Cost Analysis", icon="💰")

    elif user_type == "sarah":
        st.sidebar.markdown("### 🏠 Young Adult")
        st.sidebar.page_link("pages/20_Sarah_Home.py", label="Dashboard", icon="🏠")
        st.sidebar.page_link("pages/21_Sarah_Pantry.py", label="Pantry", icon="📦")
        st.sidebar.page_link("pages/22_Sarah_Meal_Suggestions.py", label="Suggestions", icon="💡")
        st.sidebar.page_link("pages/23_Sarah_Recipe_Browser.py", label="Recipes", icon="📖")

    elif user_type == "emily":
        st.sidebar.markdown("### ⚙️ System Admin")
        st.sidebar.page_link("pages/30_Emily_Home.py", label="Dashboard", icon="⚙️")
        st.sidebar.page_link("pages/31_Emily_System_Dashboard.py", label="System Health", icon="📊")
        st.sidebar.page_link("pages/32_Emily_Error_Logs.py", label="Error Logs", icon="🚨")
        st.sidebar.page_link("pages/33_Emily_Data_Cleanup.py", label="Data Cleanup", icon="🧹")

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        for key in ['user_type', 'user_name', 'user_id']:
            if key in st.session_state:
                del st.session_state[key]
        st.switch_page("Home.py")