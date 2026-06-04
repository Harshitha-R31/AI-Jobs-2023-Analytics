import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv("data/AI_Impact_on_Jobs_2030.csv")

st.title("💰 Salary Insights")

salary_country = (
    df.groupby("Country")["Average_Salary_USD"]
    .mean()
    .reset_index()
)

fig = px.choropleth(
    salary_country,
    locations="Country",
    locationmode="country names",
    color="Average_Salary_USD",
    title="Average Salary by Country"
)

st.plotly_chart(fig,use_container_width=True)
