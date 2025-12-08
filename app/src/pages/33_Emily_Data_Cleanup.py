import streamlit as st
import pandas as pd
from modules.api_client import api
from modules.nav import SideBarLinks

st.set_page_config(page_title="Data Cleanup", page_icon="MB", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("Please login from the home page first")
    st.stop()

st.title("Data Cleanup & Maintenance")
st.markdown("Maintain database quality and fix data issues")

st.markdown("---")

st.markdown("### Quality Issues")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Duplicate Ingredients", "12", "")

with col2:
    st.metric("Unmatched Items", "8", "")

with col3:
    st.metric("Orphaned Records", "5", "")

with col4:
    st.metric("Invalid Entries", "3", "")

st.markdown("---")

st.markdown("### Ingredients")

duplicates = [
    {'ingredient': 'Tomato', 'count': 3, 'variations': ['Tomato', 'tomato', 'Tomatoes']},
    {'ingredient': 'Chicken Breast', 'count': 2, 'variations': ['Chicken Breast', 'chicken breast']},
    {'ingredient': 'Olive Oil', 'count': 2, 'variations': ['Olive Oil', 'olive oil']},
    {'ingredient': 'Bell Pepper', 'count': 3, 'variations': ['Bell Pepper', 'bell pepper', 'Bell Peppers']}
]

for dup in duplicates:
    col1, col2, col3 = st.columns([3, 2, 1])
    
    with col1:
        st.write(f"**{dup['ingredient']}**")
        st.caption(f"Variations: {', '.join(dup['variations'])}")
    
    with col2:
        st.write(f"{dup['count']} duplicates found")
    
    with col3:
        if st.button("Merge", key=f"merge_{dup['ingredient']}"):
            st.success(f"Merged {dup['count']} entries into '{dup['ingredient']}'")

st.markdown("---")

st.markdown("### Grocery Items")

st.info("These ingredients don't have standardized names for grocery price matching")

unmatched = [
    {'ingredient': 'Red Bell Pepper', 'suggested': 'Bell Peppers (Red)'},
    {'ingredient': 'Chicken Thighs (boneless)', 'suggested': 'Chicken Thighs'},
    {'ingredient': 'Extra Virgin Olive Oil', 'suggested': 'Olive Oil'},
    {'ingredient': 'Sweet Onion', 'suggested': 'Yellow Onion'}
]

for item in unmatched:
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.write(f"**{item['ingredient']}**")
    
    with col2:
        st.write(f"→ {item['suggested']}")
    
    with col3:
        if st.button("Update", key=f"update_{item['ingredient']}"):
            st.success(f"Updated to '{item['suggested']}'")

st.markdown("---")

st.markdown("### Records")

st.warning("These records reference deleted items")

orphaned = [
    {'type': 'Meal Plan', 'id': 'MP-1234', 'issue': 'References deleted user ID 999'},
    {'type': 'Planned Meal', 'id': 'PM-5678', 'issue': 'References deleted meal ID 1234'},
    {'type': 'Inventory', 'id': 'INV-9012', 'issue': 'References deleted ingredient ID 567'}
]

for record in orphaned:
    col1, col2, col3, col4 = st.columns([1, 1, 3, 1])
    
    with col1:
        st.write(record['type'])
    
    with col2:
        st.code(record['id'])
    
    with col3:
        st.caption(record['issue'])
    
    with col4:
        if st.button("Delete", key=f"delete_{record['id']}"):
            st.success(f"Deleted {record['id']}")

st.markdown("---")

st.markdown("### Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("Run Full Cleanup", use_container_width=True):
        with st.spinner("Running cleanup..."):
            st.success("Cleanup complete! Fixed 28 issues.")

with action_col2:
    if st.button("Generate Report", use_container_width=True):
        st.success("Data quality report generated and downloaded")

with action_col3:
    if st.button("Backup Database", use_container_width=True):
        st.success("Database backed up successfully")

st.markdown("---")

st.info("**Tip:** Run full cleanup weekly to maintain optimal database performance")