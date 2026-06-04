import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/AI_Impact_on_Jobs_2030.csv")

st.title("📊 Executive Dashboard")

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Employees",
    f"{len(df):,}"
)

col2.metric(
    "Avg Salary",
    f"${df['Average_Salary_USD'].mean():,.0f}"
)

col3.metric(
    "Avg AI Risk",
    round(df['AI_Replacement_Risk'].mean(),2)
)

col4.metric(
    "Avg Future Demand",
    round(df['Future_Demand_Score'].mean(),2)
)

st.divider()

fig = px.histogram(
    df,
    x="AI_Replacement_Risk",
    nbins=25,
    title="AI Replacement Risk Distribution"
)

st.plotly_chart(fig,use_container_width=True)
