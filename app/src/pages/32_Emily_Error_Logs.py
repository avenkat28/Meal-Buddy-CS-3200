import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from app.src.modules.nav import SideBarLinks
from app.src.modules.api_client import api

st.set_page_config(page_title="Error Logs", page_icon="⚠️", layout="wide")
SideBarLinks()

if 'user_type' not in st.session_state:
    st.warning("Please login from the home page first")
    st.stop()

st.title("Error Logs")
st.markdown("Monitor and resolve system errors")

st.markdown("---")

# Error summary metrics
error_summary = api.get("/admin/errors/summary")

col1, col2, col3, col4 = st.columns(4)

if error_summary:
    with col1:
        total_24h = error_summary.get('total_24h', 0)
        change = error_summary.get('change', 0)
        st.metric("Errors (24h)", str(total_24h), f"{change:+d}")

    with col2:
        critical = error_summary.get('critical', 0)
        st.metric("Critical", str(critical), "" if critical == 0 else "⚠️")

    with col3:
        unresolved = error_summary.get('unresolved', 0)
        st.metric("Unresolved", str(unresolved))

    with col4:
        avg_resolution_min = error_summary.get('avg_resolution_minutes', 0)
        st.metric("Avg Resolution", f"{avg_resolution_min} min")
else:
    with col1:
        st.metric("Errors (24h)", "12", "-8")
    with col2:
        st.metric("Critical", "1", "⚠️")
    with col3:
        st.metric("Unresolved", "4")
    with col4:
        st.metric("Avg Resolution", "23 min")

st.markdown("---")

st.markdown("### Filters")

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

with filter_col1:
    severity_filter = st.multiselect(
        "Severity",
        ["Critical", "Error", "Warning", "Info"],
        default=["Critical", "Error"]
    )

with filter_col2:
    status_filter = st.selectbox(
        "Status",
        ["All", "Unresolved", "Resolved"]
    )

with filter_col3:
    time_filter = st.selectbox(
        "Time Range",
        ["Last Hour", "Last 24 Hours", "Last 7 Days", "Last 30 Days"]
    )

with filter_col4:
    component_filter = st.selectbox(
        "Component",
        ["All", "API", "Database", "Authentication", "Email Service"]
    )

st.markdown("---")

# Fetch error logs with filters
errors = api.get("/admin/errors", params={
    "severity": severity_filter,
    "status": status_filter if status_filter != "All" else None,
    "time_range": time_filter.lower().replace(" ", "_"),
    "component": component_filter if component_filter != "All" else None
})

if errors and len(errors) > 0:
    for error in errors:
        error_id = error.get('error_id')
        severity = error.get('severity', 'Error')
        timestamp = error.get('timestamp', '')
        message = error.get('message', '')
        component = error.get('component', 'Unknown')
        status = error.get('status', 'Unresolved')

        # Color code by severity
        if severity == 'Critical':
            st.error(f"🚨 **{severity}** - {timestamp}")
        elif severity == 'Error':
            st.warning(f"⚠️ **{severity}** - {timestamp}")
        else:
            st.info(f"ℹ️ **{severity}** - {timestamp}")

        with st.expander(f"{message[:80]}..."):
            detail_col1, detail_col2 = st.columns([3, 1])

            with detail_col1:
                st.write(f"**Full Message:** {message}")
                st.write(f"**Component:** {component}")
                st.write(f"**Error ID:** {error_id}")

                stack_trace = error.get('stack_trace', '')
                if stack_trace:
                    st.code(stack_trace, language='text')

                user_affected = error.get('user_affected')
                if user_affected:
                    st.write(f"**User Affected:** {user_affected}")

                request_details = error.get('request_details', {})
                if request_details:
                    st.write(f"**Request:** {request_details.get('method', '')} {request_details.get('endpoint', '')}")

            with detail_col2:
                st.write(f"**Status:** {status}")

                if status == 'Unresolved':
                    if st.button("Mark as Resolved", key=f"resolve_{error_id}"):
                        result = api.put(f"/admin/errors/{error_id}/resolve", {})
                        if result:
                            st.success("Marked as resolved!")
                            st.rerun()
                else:
                    resolved_by = error.get('resolved_by', 'Unknown')
                    resolved_at = error.get('resolved_at', '')
                    st.write(f"Resolved by: {resolved_by}")
                    st.write(f"At: {resolved_at}")

                if st.button("View Similar", key=f"similar_{error_id}"):
                    st.info("Finding similar errors...")

        st.markdown("---")
else:
    # Fallback error logs
    st.error("🚨 **Critical** - 2025-12-08 10:45:23")
    with st.expander("Database connection timeout on meal_plans query"):
        detail_col1, detail_col2 = st.columns([3, 1])

        with detail_col1:
            st.write("**Full Message:** Database connection timeout on meal_plans query after 30 seconds")
            st.write("**Component:** Database")
            st.write("**Error ID:** ERR-2025120810452301")
            st.code("""
Traceback (most recent call last):
  File "api/backend/meal_plans.py", line 45, in get_meal_plan
    result = db.execute(query, params)
  File "database/connector.py", line 120, in execute
    raise DatabaseTimeoutError("Connection timeout")
DatabaseTimeoutError: Connection timeout after 30 seconds
            """, language='text')
            st.write("**User Affected:** user_id=15")
            st.write("**Request:** GET /api/meal_plans/42")

        with detail_col2:
            st.write("**Status:** Unresolved")
            if st.button("Mark as Resolved", key="resolve_1"):
                st.success("Marked as resolved!")
            if st.button("View Similar", key="similar_1"):
                st.info("Finding similar errors...")

    st.markdown("---")

    st.warning("⚠️ **Error** - 2025-12-08 10:30:15")
    with st.expander("Invalid meal_id parameter in request"):
        detail_col1, detail_col2 = st.columns([3, 1])

        with detail_col1:
            st.write("**Full Message:** Invalid meal_id parameter 'abc' - expected integer")
            st.write("**Component:** API")
            st.write("**Error ID:** ERR-2025120810301502")
            st.write("**Request:** GET /api/meals/abc")

        with detail_col2:
            st.write("**Status:** Resolved")
            st.write("Resolved by: Emily")
            st.write("At: 10:35:20")

    st.markdown("---")

    st.info("ℹ️ **Warning** - 2025-12-08 09:15:42")
    with st.expander("Slow query detected: grocery_list retrieval took 2.5s"):
        detail_col1, detail_col2 = st.columns([3, 1])

        with detail_col1:
            st.write("**Full Message:** Query execution time exceeded threshold (2.5s > 1.0s)")
            st.write("**Component:** Database")
            st.write("**Error ID:** WRN-2025120809154203")
            st.write("**Request:** GET /api/grocery_list/user/23")

        with detail_col2:
            st.write("**Status:** Unresolved")
            if st.button("Mark as Resolved", key="resolve_3"):
                st.success("Marked as resolved!")

    st.markdown("---")

st.markdown("### Export Error Logs")

export_col1, export_col2 = st.columns(2)

with export_col1:
    if st.button("Download CSV", use_container_width=True):
        # Generate CSV from error data
        if errors and len(errors) > 0:
            df_errors = pd.DataFrame(errors)
            csv = df_errors.to_csv(index=False)
            st.download_button(
                label="Click to Download",
                data=csv,
                file_name=f"error_logs_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No errors to export with current filters")

with export_col2:
    if st.button("Email Report", use_container_width=True):
        result = api.post("/admin/errors/email_report", {
            "severity": severity_filter,
            "status": status_filter,
            "time_range": time_filter
        })
        if result:
            st.success("Error report sent to admin email!")
