import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Industry Analysis",
    page_icon="🏭",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
.metric-card{
    background-color:#1E293B;
    padding:15px;
    border-radius:12px;
    text-align:center;
    color:white;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = load_data("data/AI_Impact_on_Jobs_2030.csv")

st.title("🏭 Industry Analysis Dashboard")

st.markdown(
    "Analyze salary trends, AI replacement risk, future demand, and job growth across industries."
)

# --------------------------------------------------
# INDUSTRY FILTER
# --------------------------------------------------

industries = sorted(df["Industry"].unique())

selected_industry = st.selectbox(
    "Select Industry",
    industries
)

industry_df = df[
    df["Industry"] == selected_industry
]

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

avg_salary = industry_df["Average_Salary_USD"].mean()
avg_risk = industry_df["AI_Replacement_Risk"].mean()
avg_demand = industry_df["Future_Demand_Score"].mean()
avg_growth = industry_df["Job_Growth_2030"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Salary",
    f"${avg_salary:,.0f}"
)

col2.metric(
    "AI Risk",
    f"{avg_risk:.2f}"
)

col3.metric(
    "Future Demand",
    f"{avg_demand:.2f}"
)

col4.metric(
    "Job Growth 2030",
    f"{avg_growth:.2f}%"
)

st.divider()

# --------------------------------------------------
# SALARY COMPARISON
# --------------------------------------------------

st.subheader("💰 Industry Salary Comparison")

salary_df = (
    df.groupby("Industry")
    ["Average_Salary_USD"]
    .mean()
    .reset_index()
    .sort_values(
        by="Average_Salary_USD",
        ascending=False
    )
)

fig_salary = px.bar(
    salary_df,
    x="Industry",
    y="Average_Salary_USD",
    color="Average_Salary_USD",
    title="Average Salary by Industry"
)

st.plotly_chart(
    fig_salary,
    use_container_width=True
)

# --------------------------------------------------
# AI RISK COMPARISON
# --------------------------------------------------

st.subheader("⚠ AI Replacement Risk")

risk_df = (
    df.groupby("Industry")
    ["AI_Replacement_Risk"]
    .mean()
    .reset_index()
    .sort_values(
        by="AI_Replacement_Risk",
        ascending=False
    )
)

fig_risk = px.bar(
    risk_df,
    x="Industry",
    y="AI_Replacement_Risk",
    color="AI_Replacement_Risk",
    title="AI Risk Across Industries"
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)

# --------------------------------------------------
# FUTURE DEMAND
# --------------------------------------------------

st.subheader("📈 Future Demand Score")

demand_df = (
    df.groupby("Industry")
    ["Future_Demand_Score"]
    .mean()
    .reset_index()
)

fig_demand = px.bar(
    demand_df,
    x="Industry",
    y="Future_Demand_Score",
    color="Future_Demand_Score",
    title="Future Demand by Industry"
)

st.plotly_chart(
    fig_demand,
    use_container_width=True
)

# --------------------------------------------------
# JOB GROWTH
# --------------------------------------------------

st.subheader("🚀 Job Growth Forecast")

growth_df = (
    df.groupby("Industry")
    ["Job_Growth_2030"]
    .mean()
    .reset_index()
    .sort_values(
        by="Job_Growth_2030",
        ascending=False
    )
)

fig_growth = px.bar(
    growth_df,
    x="Industry",
    y="Job_Growth_2030",
    color="Job_Growth_2030",
    title="Projected Job Growth by 2030"
)

st.plotly_chart(
    fig_growth,
    use_container_width=True
)

# --------------------------------------------------
# SALARY VS AI RISK
# --------------------------------------------------

st.subheader("📊 Salary vs AI Risk")

fig_scatter = px.scatter(
    df,
    x="Average_Salary_USD",
    y="AI_Replacement_Risk",
    color="Industry",
    size="Future_Demand_Score",
    hover_name="Job_Title",
    title="Salary vs AI Replacement Risk"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# --------------------------------------------------
# TOP JOBS IN INDUSTRY
# --------------------------------------------------

st.subheader(f"🏆 Top Jobs in {selected_industry}")

top_jobs = (
    industry_df[
        ["Job_Title",
         "Average_Salary_USD",
         "AI_Replacement_Risk",
         "Future_Demand_Score"]
    ]
    .sort_values(
        by="Average_Salary_USD",
        ascending=False
    )
    .head(15)
)

st.dataframe(
    top_jobs,
    use_container_width=True
)

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------

st.subheader("🔍 Industry Insights")

highest_salary = (
    salary_df.iloc[0]["Industry"]
)

highest_risk = (
    risk_df.iloc[0]["Industry"]
)

highest_growth = (
    growth_df.iloc[0]["Industry"]
)

st.info(
    f"💰 Highest Paying Industry: {highest_salary}"
)

st.warning(
    f"⚠ Highest AI Risk Industry: {highest_risk}"
)

st.success(
    f"🚀 Highest Growth Industry: {highest_growth}"
)

# --------------------------------------------------
# DOWNLOAD OPTION
# --------------------------------------------------

csv = industry_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Industry Data",
    data=csv,
    file_name=f"{selected_industry}_analysis.csv",
    mime="text/csv"
)
