import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Future Predictions",
    page_icon="🚀",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = load_data("data/AI_Impact_on_Jobs_2030.csv")

st.title("🚀 Future Workforce Predictions")

st.markdown("""
Analyze future job demand, workforce growth trends,
and identify careers that will thrive in the AI era.
""")

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

avg_demand = df["Future_Demand_Score"].mean()
avg_growth = df["Job_Growth_2030"].mean()
avg_risk = df["AI_Replacement_Risk"].mean()

high_growth_jobs = len(
    df[df["Job_Growth_2030"] > df["Job_Growth_2030"].mean()]
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Avg Future Demand",
    f"{avg_demand:.2f}"
)

col2.metric(
    "Avg Job Growth",
    f"{avg_growth:.2f}%"
)

col3.metric(
    "Avg AI Risk",
    f"{avg_risk:.2f}"
)

col4.metric(
    "High Growth Jobs",
    high_growth_jobs
)

st.divider()

# --------------------------------------------------
# FUTURE DEMAND BY INDUSTRY
# --------------------------------------------------

st.subheader("📈 Future Demand by Industry")

industry_demand = (
    df.groupby("Industry")
    ["Future_Demand_Score"]
    .mean()
    .reset_index()
    .sort_values(
        by="Future_Demand_Score",
        ascending=False
    )
)

fig1 = px.bar(
    industry_demand,
    x="Industry",
    y="Future_Demand_Score",
    color="Future_Demand_Score",
    title="Industry Future Demand"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# --------------------------------------------------
# JOB GROWTH FORECAST
# --------------------------------------------------

st.subheader("🚀 Job Growth Forecast by Industry")

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

fig2 = px.bar(
    growth_df,
    x="Industry",
    y="Job_Growth_2030",
    color="Job_Growth_2030",
    title="Projected Job Growth by 2030"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# --------------------------------------------------
# AI RISK VS DEMAND
# --------------------------------------------------

st.subheader("⚖ Future Demand vs AI Risk")

fig3 = px.scatter(
    df,
    x="AI_Replacement_Risk",
    y="Future_Demand_Score",
    color="Industry",
    size="Average_Salary_USD",
    hover_name="Job_Title",
    title="Future Demand vs Automation Risk"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# --------------------------------------------------
# TOP FUTURE JOBS
# --------------------------------------------------

st.subheader("🏆 Top Future-Proof Careers")

future_jobs = (
    df.sort_values(
        by="Future_Demand_Score",
        ascending=False
    )
    [
        [
            "Job_Title",
            "Industry",
            "Average_Salary_USD",
            "Future_Demand_Score",
            "AI_Replacement_Risk",
            "Job_Growth_2030"
        ]
    ]
    .head(20)
)

st.dataframe(
    future_jobs,
    use_container_width=True
)

# --------------------------------------------------
# FUTURE READY INDUSTRIES
# --------------------------------------------------

st.subheader("🌟 Future Ready Industries")

industry_score = (
    df.groupby("Industry")
    .agg({
        "Future_Demand_Score":"mean",
        "Job_Growth_2030":"mean",
        "AI_Replacement_Risk":"mean"
    })
    .reset_index()
)

industry_score["Future_Readiness"] = (
    industry_score["Future_Demand_Score"]
    +
    industry_score["Job_Growth_2030"]
    -
    industry_score["AI_Replacement_Risk"]
)

industry_score = industry_score.sort_values(
    by="Future_Readiness",
    ascending=False
)

fig4 = px.bar(
    industry_score.head(10),
    x="Industry",
    y="Future_Readiness",
    color="Future_Readiness",
    title="Top Future Ready Industries"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# --------------------------------------------------
# SALARY VS FUTURE DEMAND
# --------------------------------------------------

st.subheader("💰 Salary vs Future Demand")

fig5 = px.scatter(
    df,
    x="Average_Salary_USD",
    y="Future_Demand_Score",
    color="Industry",
    hover_name="Job_Title",
    title="Salary vs Future Demand"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# --------------------------------------------------
# HIGH GROWTH JOBS TABLE
# --------------------------------------------------

st.subheader("📋 High Growth Careers")

high_growth = (
    df.sort_values(
        by="Job_Growth_2030",
        ascending=False
    )
    [
        [
            "Job_Title",
            "Industry",
            "Job_Growth_2030",
            "Future_Demand_Score",
            "Average_Salary_USD"
        ]
    ]
    .head(25)
)

st.dataframe(
    high_growth,
    use_container_width=True
)

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------

st.subheader("🔍 AI Generated Insights")

highest_demand_industry = (
    industry_demand.iloc[0]["Industry"]
)

highest_growth_industry = (
    growth_df.iloc[0]["Industry"]
)

lowest_risk_industry = (
    industry_score.sort_values(
        by="AI_Replacement_Risk"
    ).iloc[0]["Industry"]
)

st.success(
    f"🚀 Highest Future Demand Industry: {highest_demand_industry}"
)

st.info(
    f"📈 Fastest Growing Industry: {highest_growth_industry}"
)

st.warning(
    f"🛡 Lowest Automation Risk Industry: {lowest_risk_industry}"
)

# --------------------------------------------------
# DOWNLOAD REPORT
# --------------------------------------------------

report = industry_score.to_csv(index=False)

st.download_button(
    label="⬇ Download Future Prediction Report",
    data=report,
    file_name="future_predictions_report.csv",
    mime="text/csv"
)

# --------------------------------------------------
# CONCLUSION
# --------------------------------------------------

st.markdown("---")

st.markdown("""
### 📌 Key Takeaways

- Industries with high future demand are likely to create more jobs by 2030.
- Careers with low AI replacement risk remain valuable in the long term.
- Future-ready industries combine:
    - High demand
    - Strong growth
    - Lower automation risk
- Upskilling in emerging technologies can significantly improve career resilience.
""")
