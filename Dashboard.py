import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="HEART Analysis Dashboard",
    page_icon="❤️",
    layout="wide"
)

# ------------------------------------------------
# LOAD EXCEL FILE
# ------------------------------------------------

file_path = os.path.join(
    os.path.dirname(__file__),
    "HEART_ANALYSIS.xlsx"
)

if not os.path.exists(file_path):
    st.error("❌ HEART_ANALYSIS.xlsx not found in the GitHub repository.")
    st.stop()

# Read the HEART analysis sheet
df = pd.read_excel(file_path, sheet_name="Sheet1")

# Remove accidental spaces from column names
df.columns = df.columns.astype(str).str.strip()

# ------------------------------------------------
# TITLE
# ------------------------------------------------

st.title("❤️ HEART Analysis Dashboard")
st.write("User Experience Analysis – E-Learning Application")

# ------------------------------------------------
# SIDEBAR FILTER
# ------------------------------------------------

st.sidebar.header("🔎 Filters")

# Check whether category column exists
if "Time difference Category" in df.columns:

    categories = df["Time difference Category"].dropna().unique()

    selected = st.sidebar.multiselect(
        "Time-to-Value Category",
        categories,
        default=list(categories)
    )

    data = df[
        df["Time difference Category"].isin(selected)
    ]

else:
    # If column is unavailable, use complete dataset
    data = df

# ------------------------------------------------
# HEART METRICS
# ------------------------------------------------

st.subheader("📊 HEART Metrics")

c1, c2, c3, c4, c5 = st.columns(5)

# Happiness
c1.metric(
    "😊 Happiness",
    f"{data['CSAT_Response'].mean():.2f}/5"
)

# Engagement
c2.metric(
    "📈 Engagement",
    f"{data['Sessions'].mean():.1f}"
)

# Adoption
c3.metric(
    "🚀 Adoption",
    f"{data['Core_Action'].mean() * 100:.1f}%"
)

# Retention
c4.metric(
    "🔄 Retention",
    f"{data['Day7_Return'].mean() * 100:.1f}%"
)

# Task Success
c5.metric(
    "✅ Task Success",
    f"{data['Task_Completed'].mean() * 100:.1f}%"
)

st.divider()

# ------------------------------------------------
# HAPPINESS & ENGAGEMENT
# ------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("😊 Happiness – CSAT")

    csat = data["CSAT_Response"].value_counts().sort_index()

    st.bar_chart(csat)


with col2:

    st.subheader("📈 Engagement – Sessions")

    sessions = data["Sessions"].value_counts().sort_index()

    st.bar_chart(sessions)

# ------------------------------------------------
# ADOPTION & RETENTION
# ------------------------------------------------

col3, col4 = st.columns(2)

with col3:

    st.subheader("🚀 Adoption")

    adopted = data["Core_Action"].sum()
    not_adopted = len(data) - adopted

    adoption = pd.DataFrame(
        {"Users": [adopted, not_adopted]},
        index=["Adopted", "Not Adopted"]
    )

    st.bar_chart(adoption)


with col4:

    st.subheader("🔄 Retention")

    returned = data["Day7_Return"].sum()
    not_returned = len(data) - returned

    retention = pd.DataFrame(
        {"Users": [returned, not_returned]},
        index=["Returned", "Did Not Return"]
    )

    st.bar_chart(retention)

# ------------------------------------------------
# TASK PERFORMANCE
# ------------------------------------------------

st.divider()

st.subheader("✅ Task Performance")

task_data = data[
    ["Task_Attempts", "Errors"]
].copy()

task_data.index = range(1, len(task_data) + 1)

st.line_chart(task_data)

# ------------------------------------------------
# UX RISK
# ------------------------------------------------

st.subheader("⚠️ UX Risk Overview")

risk_columns = [
    "User_ID",
    "SUS_Total",
    "CES_Response",
    "Time Difference",
    "User Error Rate",
    "Sessions",
    "Retention Flag",
    "Task Completion Flag",
    "UX_Risk_Points"
]

available_columns = [
    col for col in risk_columns
    if col in data.columns
]

if available_columns:

    st.dataframe(
        data[available_columns],
        use_container_width=True
    )

# ------------------------------------------------
# COMPLETE DATASET
# ------------------------------------------------

st.divider()

with st.expander("📋 View Complete Dataset"):

    st.dataframe(
        data,
        use_container_width=True
    )

st.divider()

st.caption(
    "HEART Analysis Dashboard | Python + Streamlit"
)
