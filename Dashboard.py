import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(
    page_title="HEART Analysis Dashboard",
    page_icon="❤️",
    layout="wide"
)

# Title
st.title("❤️ HEART Analysis Dashboard")
st.write("User Experience Analysis for an E-Learning Application")

# Upload Excel file
st.sidebar.header("📁 Upload Dataset")

file = st.sidebar.file_uploader(
    "Upload your HEART Excel file",
    type=["xlsx"]
)

# Stop until file is uploaded
if file is None:
    st.info("👈 Please upload your HEART_ANALYSIS Excel file from the sidebar.")
    st.stop()

# Read Excel file
df = pd.read_excel(file, sheet_name="Sheet1")

st.sidebar.success("Dataset loaded successfully!")

# Sidebar filter
st.sidebar.header("🔎 Filters")

if "Time difference Category" in df.columns:

    categories = df["Time difference Category"].dropna().unique()

    selected = st.sidebar.multiselect(
        "Time-to-Value Category",
        categories,
        default=categories
    )

    data = df[df["Time difference Category"].isin(selected)]

else:
    data = df

# HEART Metrics
st.subheader("📊 HEART Metrics")

c1, c2, c3, c4, c5 = st.columns(5)

# Happiness
if "CSAT_Response" in data.columns:
    c1.metric(
        "😊 Happiness",
        f"{data['CSAT_Response'].mean():.2f}/5"
    )

# Engagement
if "Sessions" in data.columns:
    c2.metric(
        "📈 Engagement",
        f"{data['Sessions'].mean():.1f}"
    )

# Adoption
if "Core_Action" in data.columns:
    c3.metric(
        "🚀 Adoption",
        f"{data['Core_Action'].mean()*100:.1f}%"
    )

# Retention
if "Day7_Return" in data.columns:
    c4.metric(
        "🔄 Retention",
        f"{data['Day7_Return'].mean()*100:.1f}%"
    )

# Task Success
if "Task_Completed" in data.columns:
    c5.metric(
        "✅ Task Success",
        f"{data['Task_Completed'].mean()*100:.1f}%"
    )

st.divider()

# Happiness & Engagement
col1, col2 = st.columns(2)

with col1:
    st.subheader("😊 Happiness")

    if "CSAT_Response" in data.columns:
        csat = data["CSAT_Response"].value_counts().sort_index()
        st.bar_chart(csat)

with col2:
    st.subheader("📈 Engagement")

    if "Sessions" in data.columns:
        sessions = data["Sessions"].value_counts().sort_index()
        st.bar_chart(sessions)

# Adoption & Retention
col3, col4 = st.columns(2)

with col3:
    st.subheader("🚀 Adoption")

    if "Core_Action" in data.columns:

        adoption = pd.DataFrame({
            "Users": [
                data["Core_Action"].sum(),
                len(data) - data["Core_Action"].sum()
            ]
        }, index=[
            "Adopted",
            "Not Adopted"
        ])

        st.bar_chart(adoption)

with col4:
    st.subheader("🔄 Retention")

    if "Day7_Return" in data.columns:

        retention = pd.DataFrame({
            "Users": [
                data["Day7_Return"].sum(),
                len(data) - data["Day7_Return"].sum()
            ]
        }, index=[
            "Returned",
            "Did Not Return"
        ])

        st.bar_chart(retention)

# Task Performance
st.divider()

st.subheader("✅ Task Performance")

if "Task_Attempts" in data.columns and "Errors" in data.columns:

    task_data = data[
        ["Task_Attempts", "Errors"]
    ].copy()

    task_data.index = range(1, len(task_data) + 1)

    st.line_chart(task_data)

# UX Risk
st.subheader("⚠️ UX Risk Overview")

risk_columns = [
    "User_ID",
    "SUS_Total",
    "CES_Response",
    "Time Difference",
    "User Error Rate",
    "Sessions",
    "Retention Flag",
    "Task Completion Flag"
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

# Dataset preview
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
