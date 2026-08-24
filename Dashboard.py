import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="HEART Analysis Dashboard",
    page_icon="❤️",
    layout="wide"
)

# Load Excel file
df = pd.read_excel("HEART_ANALYSIS (1).xlsx", sheet_name="Sheet1")

# Title
st.title("❤️ HEART Analysis Dashboard")
st.write("User Experience Analysis for an E-Learning Application")

# Sidebar
st.sidebar.header("🔎 Filters")

categories = df["Time difference Category"].dropna().unique()

selected = st.sidebar.multiselect(
    "Time-to-Value Category",
    categories,
    default=categories
)

data = df[df["Time difference Category"].isin(selected)]

# HEART Metrics
st.subheader("📊 HEART Metrics")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("😊 Happiness", f"{data['CSAT_Response'].mean():.2f}/5")
c2.metric("📈 Engagement", f"{data['Sessions'].mean():.1f}")
c3.metric("🚀 Adoption", f"{data['Core_Action'].mean()*100:.1f}%")
c4.metric("🔄 Retention", f"{data['Day7_Return'].mean()*100:.1f}%")
c5.metric("✅ Task Success", f"{data['Task_Completed'].mean()*100:.1f}%")

st.divider()

# Happiness
col1, col2 = st.columns(2)

with col1:
    st.subheader("😊 Happiness")
    st.bar_chart(
        data["CSAT_Response"].value_counts().sort_index()
    )

with col2:
    st.subheader("📈 Engagement")
    st.bar_chart(
        data["Sessions"].value_counts().sort_index()
    )

# Adoption & Retention
col3, col4 = st.columns(2)

with col3:
    st.subheader("🚀 Adoption")

    adoption = pd.DataFrame({
        "Users": [
            data["Core_Action"].sum(),
            len(data) - data["Core_Action"].sum()
        ]
    }, index=["Adopted", "Not Adopted"])

    st.bar_chart(adoption)

with col4:
    st.subheader("🔄 Retention")

    retention = pd.DataFrame({
        "Users": [
            data["Day7_Return"].sum(),
            len(data) - data["Day7_Return"].sum()
        ]
    }, index=["Returned", "Did Not Return"])

    st.bar_chart(retention)

# Task Performance
st.divider()

st.subheader("✅ Task Performance")

task_data = data[["Task_Attempts", "Errors"]].copy()
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
    col for col in risk_columns if col in data.columns
]

st.dataframe(
    data[available_columns],
    use_container_width=True
)

st.divider()

st.caption("HEART Analysis Dashboard | Python + Streamlit")

