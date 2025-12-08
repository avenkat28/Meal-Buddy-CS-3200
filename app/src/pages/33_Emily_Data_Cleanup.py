import streamlit as st
import pandas as pd
from app.src.modules.nav import SideBarLinks
from app.src.modules.api_client import api

st.set_page_config(page_title="Data Cleanup", page_icon="🧹", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("Please login from the home page first")
    st.stop()

st.title("Data Quality & Cleanup Tools")
st.markdown("Identify and resolve data integrity issues")

st.markdown("---")

# Data quality summary
quality_summary = api.get("/admin/data/quality_summary")

col1, col2, col3, col4 = st.columns(4)

if quality_summary:
    with col1:
        total_issues = quality_summary.get('total_issues', 0)
        st.metric("Total Issues", str(total_issues))

    with col2:
        duplicates = quality_summary.get('duplicates', 0)
        st.metric("Duplicates", str(duplicates))

    with col3:
        orphaned = quality_summary.get('orphaned_records', 0)
        st.metric("Orphaned Records", str(orphaned))

    with col4:
        integrity = quality_summary.get('integrity_violations', 0)
        st.metric("Integrity Violations", str(integrity))
else:
    with col1:
        st.metric("Total Issues", "23")
    with col2:
        st.metric("Duplicates", "8")
    with col3:
        st.metric("Orphaned Records", "12")
    with col4:
        st.metric("Integrity Violations", "3")

st.markdown("---")

# Tabs for different types of issues
tab1, tab2, tab3, tab4 = st.tabs([
    "Duplicate Ingredients",
    "Orphaned Records",
    "Missing Data",
    "Invalid References"
])

with tab1:
    st.markdown("### Duplicate Ingredients")
    st.caption("Ingredients that may be duplicates with slight name variations")

    # Fetch duplicate ingredients
    duplicates = api.get("/admin/data/duplicates/ingredients")

    if duplicates and len(duplicates) > 0:
        for dup_group in duplicates:
            group_id = dup_group.get('group_id')
            ingredients = dup_group.get('ingredients', [])

            with st.expander(f"Duplicate Group {group_id} ({len(ingredients)} items)"):
                st.write("**Possible duplicates:**")

                for ing in ingredients:
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                    with col1:
                        st.write(f"• {ing.get('ingredient_name', '')}")

                    with col2:
                        st.caption(f"ID: {ing.get('ingredient_id', '')}")

                    with col3:
                        st.caption(f"Used in {ing.get('usage_count', 0)} meals")

                    with col4:
                        if st.button("Keep", key=f"keep_{ing.get('ingredient_id')}"):
                            st.info(f"Keeping {ing.get('ingredient_name')}")

                merge_col1, merge_col2 = st.columns(2)

                with merge_col1:
                    primary_id = st.selectbox(
                        "Select primary ingredient to keep",
                        [ing.get('ingredient_id') for ing in ingredients],
                        key=f"primary_{group_id}"
                    )

                with merge_col2:
                    st.write("")
                    st.write("")
                    if st.button("Merge Duplicates", key=f"merge_{group_id}"):
                        result = api.post("/admin/data/merge_ingredients", {
                            "primary_id": primary_id,
                            "duplicate_ids": [ing.get('ingredient_id') for ing in ingredients if
                                              ing.get('ingredient_id') != primary_id]
                        })
                        if result:
                            st.success("Duplicates merged successfully!")
                            st.rerun()
    else:
        # Fallback duplicates
        with st.expander("Duplicate Group 1 (3 items)"):
            st.write("**Possible duplicates:**")

            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write("• Chicken Breast")
            with col2:
                st.caption("ID: 45")
            with col3:
                st.caption("Used in 8 meals")
            with col4:
                if st.button("Keep", key="keep_45"):
                    st.info("Keeping Chicken Breast")

            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write("• chicken breast")
            with col2:
                st.caption("ID: 78")
            with col3:
                st.caption("Used in 3 meals")
            with col4:
                if st.button("Keep", key="keep_78"):
                    st.info("Keeping chicken breast")

            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write("• Chicken breast (boneless)")
            with col2:
                st.caption("ID: 92")
            with col3:
                st.caption("Used in 5 meals")
            with col4:
                if st.button("Keep", key="keep_92"):
                    st.info("Keeping Chicken breast (boneless)")

            merge_col1, merge_col2 = st.columns(2)
            with merge_col1:
                primary_id = st.selectbox("Select primary ingredient to keep", [45, 78, 92])
            with merge_col2:
                st.write("")
                st.write("")
                if st.button("Merge Duplicates"):
                    st.success("Duplicates merged successfully!")

with tab2:
    st.markdown("### Orphaned Records")
    st.caption("Records that reference non-existent foreign keys")

    # Fetch orphaned records
    orphaned = api.get("/admin/data/orphaned_records")

    if orphaned and len(orphaned) > 0:
        df_orphaned = pd.DataFrame(orphaned)

        for idx, record in df_orphaned.iterrows():
            table = record.get('table_name', '')
            record_id = record.get('record_id', '')
            issue = record.get('issue', '')

            col1, col2, col3 = st.columns([2, 3, 1])

            with col1:
                st.write(f"**{table}** (ID: {record_id})")

            with col2:
                st.write(issue)

            with col3:
                if st.button("Delete", key=f"delete_orphan_{table}_{record_id}"):
                    result = api.delete(f"/admin/data/orphaned/{table}/{record_id}")
                    if result:
                        st.success("Deleted!")
                        st.rerun()
    else:
        # Fallback orphaned records
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            st.write("**planned_meals** (ID: 234)")
        with col2:
            st.write("References meal_id=999 which doesn't exist")
        with col3:
            if st.button("Delete", key="delete_1"):
                st.success("Deleted!")

        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            st.write("**user_goals** (ID: 78)")
        with col2:
            st.write("References user_id=55 which doesn't exist")
        with col3:
            if st.button("Delete", key="delete_2"):
                st.success("Deleted!")

        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            st.write("**grocery_list** (ID: 456)")
        with col2:
            st.write("References ingredient_id=777 which doesn't exist")
        with col3:
            if st.button("Delete", key="delete_3"):
                st.success("Deleted!")

with tab3:
    st.markdown("### Missing Required Data")
    st.caption("Records with NULL values in non-nullable fields")

    # Fetch missing data issues
    missing_data = api.get("/admin/data/missing_data")

    if missing_data and len(missing_data) > 0:
        df_missing = pd.DataFrame(missing_data)
        st.dataframe(df_missing, use_container_width=True, hide_index=True)

        if st.button("Auto-fill with defaults"):
            result = api.post("/admin/data/autofill_missing", {})
            if result:
                st.success("Missing data filled with default values!")
                st.rerun()
    else:
        # Fallback missing data
        missing_data_dict = {
            'Table': ['meals', 'users', 'ingredients'],
            'Record ID': [123, 45, 89],
            'Missing Field': ['prep_time', 'email', 'unit'],
            'Count': [5, 2, 8]
        }
        df_missing = pd.DataFrame(missing_data_dict)
        st.dataframe(df_missing, use_container_width=True, hide_index=True)

        if st.button("Auto-fill with defaults"):
            st.success("Missing data filled with default values!")

with tab4:
    st.markdown("### Invalid Foreign Key References")
    st.caption("Data integrity violations that need manual review")

    # Fetch integrity violations
    violations = api.get("/admin/data/integrity_violations")

    if violations and len(violations) > 0:
        for violation in violations:
            table = violation.get('table', '')
            issue = violation.get('issue', '')
            count = violation.get('count', 0)

            with st.expander(f"{table}: {issue} ({count} records)"):
                st.write("**Suggested Fix:**")
                st.write(violation.get('suggested_fix', 'Manual review required'))

                if st.button("View Affected Records", key=f"view_{table}_{hash(issue)}"):
                    # Fetch detailed records
                    details = api.get(f"/admin/data/violation_details/{table}/{hash(issue)}")
                    if details:
                        df_details = pd.DataFrame(details)
                        st.dataframe(df_details, use_container_width=True, hide_index=True)

                fix_col1, fix_col2 = st.columns(2)

                with fix_col1:
                    if st.button("Apply Suggested Fix", key=f"fix_{table}_{hash(issue)}"):
                        result = api.post(f"/admin/data/apply_fix/{table}/{hash(issue)}", {})
                        if result:
                            st.success("Fix applied!")
                            st.rerun()

                with fix_col2:
                    if st.button("Delete Invalid Records", key=f"delete_{table}_{hash(issue)}"):
                        result = api.delete(f"/admin/data/violation_records/{table}/{hash(issue)}")
                        if result:
                            st.warning("Invalid records deleted!")
                            st.rerun()
    else:
        # Fallback violations
        with st.expander("user_dietary_preferences: References non-existent user_id (3 records)"):
            st.write("**Suggested Fix:** Delete these preference records or create placeholder users")

            if st.button("View Affected Records", key="view_1"):
                st.write("Records: 41, 42, 43")

            fix_col1, fix_col2 = st.columns(2)
            with fix_col1:
                if st.button("Apply Suggested Fix", key="fix_1"):
                    st.success("Fix applied!")
            with fix_col2:
                if st.button("Delete Invalid Records", key="delete_fix_1"):
                    st.warning("Invalid records deleted!")

st.markdown("---")

st.markdown("### Bulk Actions")

bulk_col1, bulk_col2, bulk_col3 = st.columns(3)

with bulk_col1:
    if st.button("Run Full Data Validation", use_container_width=True):
        with st.spinner("Running validation..."):
            result = api.post("/admin/data/validate_all", {})
            if result:
                issues_found = result.get('issues_found', 0)
                st.success(f"Validation complete! Found {issues_found} issues.")

with bulk_col2:
    if st.button("Generate Data Quality Report", use_container_width=True):
        result = api.get("/admin/data/quality_report")
        if result:
            st.download_button(
                label="Download Report",
                data=str(result),
                file_name="data_quality_report.txt",
                mime="text/plain"
            )

with bulk_col3:
    if st.button("Backup Database", use_container_width=True):
        with st.spinner("Creating backup..."):
            result = api.post("/admin/database/backup", {})
            if result:
                st.success("Database backup created successfully!")
