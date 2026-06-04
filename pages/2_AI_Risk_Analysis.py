import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/AI_Impact_on_Jobs_2030.csv")

st.title("⚠ AI Risk Analytics")

industry_risk = (
    df.groupby("Industry")["AI_Replacement_Risk"]
    .mean()
    .reset_index()
)

fig = px.bar(
    industry_risk,
    x="Industry",
    y="AI_Replacement_Risk",
    color="AI_Replacement_Risk",
    title="Industry AI Risk"
)

st.plotly_chart(fig,use_container_width=True)
