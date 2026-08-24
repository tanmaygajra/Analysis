
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="HEART Dashboard", layout="wide")

# Load data
df = pd.read_excel("HEART_ANALYSIS (1).xlsx", sheet_name="Sheet1")

st.title("❤️ HEART UX Analysis Dashboard")
st.caption("Online Learning / E-Learning Application")

# Sidebar
st.sidebar.header("Filters")
category = st.sidebar.multiselect(
    "Time-to-Value Category",
    df["Time difference Category"].dropna().unique(),
    default=df["Time difference Category"].dropna().unique()
)
data = df[df["Time difference Category"].isin(category)]

# KPIs
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("😊 Happiness", f"{data['CSAT_Response'].mean():.2f}/5")
c2.metric("📈 Engagement", f"{data['Sessions'].mean():.1f}")
c3.metric("🚀 Adoption", f"{data['Core_Action'].mean()*100:.1f}%")
c4.metric("🔄 Retention", f"{data['Day7_Return'].mean()*100:.1f}%")
c5.metric("✅ Task Success", f"{data['Task_Completed'].mean()*100:.1f}%")

st.divider()

# HEART charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Happiness")
    fig = px.histogram(data, x="CSAT_Response",
                       title="CSAT Distribution",
                       labels={"CSAT_Response": "CSAT Score"})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Engagement")
    fig = px.histogram(data, x="Sessions",
                       title="Sessions per User",
                       labels={"Sessions": "Sessions"})
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Adoption & Retention")
    temp = pd.DataFrame({
        "Metric": ["Adoption", "Retention"],
        "Percentage": [
            data["Core_Action"].mean()*100,
            data["Day7_Return"].mean()*100
        ]
    })
    fig = px.bar(temp, x="Metric", y="Percentage", range_y=[0,100])
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("Task Performance")
    fig = px.scatter(data, x="Task_Attempts", y="Errors",
                     size="Sessions", hover_name="User_ID",
                     title="Task Attempts vs Errors")
    st.plotly_chart(fig, use_container_width=True)

# Risk table
st.subheader("⚠️ UX Risk Overview")

risk = data[[
    "User_ID", "SUS_Total", "CES_Response",
    "Time Difference", "User Error Rate",
    "Sessions", "Retention Flag",
    "Task Completion Flag"
]].copy()

st.dataframe(risk, use_container_width=True)

