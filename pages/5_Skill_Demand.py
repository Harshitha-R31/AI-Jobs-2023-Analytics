import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

from utils.data_loader import load_data

# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="Skill Demand Analysis",
    page_icon="🧠",
    layout="wide"
)

# ----------------------------------
# LOAD DATA
# ----------------------------------

df = load_data("data/AI_Impact_on_Jobs_2030.csv")

st.title("🧠 Skill Demand Analysis")

st.markdown("""
Analyze the most valuable and future-proof skills in the AI-driven job market.
""")

# ----------------------------------
# CHECK COLUMN EXISTS
# ----------------------------------

if "Required_Skills" not in df.columns:
    st.error("Required_Skills column not found in dataset.")
    st.stop()

# ----------------------------------
# EXTRACT SKILLS
# ----------------------------------

skills = []

for row in df["Required_Skills"].dropna():
    skill_list = str(row).split(",")

    for skill in skill_list:
        skills.append(skill.strip())

skill_counter = Counter(skills)

skill_df = pd.DataFrame(
    skill_counter.items(),
    columns=["Skill", "Frequency"]
)

skill_df = skill_df.sort_values(
    by="Frequency",
    ascending=False
)

# ----------------------------------
# KPI SECTION
# ----------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Skills",
    len(skill_df)
)

col2.metric(
    "Most Demanded Skill",
    skill_df.iloc[0]["Skill"]
)

col3.metric(
    "Occurrences",
    int(skill_df.iloc[0]["Frequency"])
)

st.divider()

# ----------------------------------
# TOP SKILLS BAR CHART
# ----------------------------------

st.subheader("🔥 Top 20 Most Demanded Skills")

top_skills = skill_df.head(20)

fig = px.bar(
    top_skills,
    x="Skill",
    y="Frequency",
    color="Frequency",
    title="Top Skills in Demand"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# PIE CHART
# ----------------------------------

st.subheader("📊 Skill Demand Distribution")

fig_pie = px.pie(
    top_skills,
    names="Skill",
    values="Frequency",
    title="Top Skill Share"
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)

# ----------------------------------
# SEARCH SKILL
# ----------------------------------

st.subheader("🔍 Search a Skill")

selected_skill = st.selectbox(
    "Choose a Skill",
    sorted(skill_df["Skill"].unique())
)

skill_jobs = df[
    df["Required_Skills"]
    .str.contains(
        selected_skill,
        case=False,
        na=False
    )
]

# ----------------------------------
# KPI FOR SELECTED SKILL
# ----------------------------------

avg_salary = skill_jobs[
    "Average_Salary_USD"
].mean()

avg_risk = skill_jobs[
    "AI_Replacement_Risk"
].mean()

avg_demand = skill_jobs[
    "Future_Demand_Score"
].mean()

c1, c2, c3 = st.columns(3)

c1.metric(
    "Average Salary",
    f"${avg_salary:,.0f}"
)

c2.metric(
    "Average AI Risk",
    f"{avg_risk:.2f}"
)

c3.metric(
    "Future Demand",
    f"{avg_demand:.2f}"
)

# ----------------------------------
# INDUSTRIES USING THIS SKILL
# ----------------------------------

st.subheader(
    f"🏭 Industries Using {selected_skill}"
)

industry_count = (
    skill_jobs["Industry"]
    .value_counts()
    .reset_index()
)

industry_count.columns = [
    "Industry",
    "Count"
]

fig_industry = px.bar(
    industry_count,
    x="Industry",
    y="Count",
    color="Count",
    title=f"{selected_skill} Across Industries"
)

st.plotly_chart(
    fig_industry,
    use_container_width=True
)

# ----------------------------------
# SALARY ANALYSIS
# ----------------------------------

st.subheader(
    f"💰 Salary Distribution for {selected_skill}"
)

fig_salary = px.histogram(
    skill_jobs,
    x="Average_Salary_USD",
    nbins=20,
    title=f"Salary Distribution ({selected_skill})"
)

st.plotly_chart(
    fig_salary,
    use_container_width=True
)

# ----------------------------------
# AI RISK ANALYSIS
# ----------------------------------

st.subheader(
    f"⚠ AI Risk Distribution for {selected_skill}"
)

fig_risk = px.box(
    skill_jobs,
    y="AI_Replacement_Risk",
    title=f"AI Risk ({selected_skill})"
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)

# ----------------------------------
# TOP JOBS
# ----------------------------------

st.subheader(
    f"🏆 Top Jobs Requiring {selected_skill}"
)

top_jobs = (
    skill_jobs[
        [
            "Job_Title",
            "Industry",
            "Average_Salary_USD",
            "AI_Replacement_Risk",
            "Future_Demand_Score"
        ]
    ]
    .sort_values(
        by="Average_Salary_USD",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_jobs,
    use_container_width=True
)

# ----------------------------------
# FUTURE READY SKILLS
# ----------------------------------

st.subheader("🚀 Future Ready Skills")

future_skills = []

for skill in skill_df["Skill"]:

    temp = df[
        df["Required_Skills"]
        .str.contains(
            skill,
            case=False,
            na=False
        )
    ]

    if len(temp) > 0:

        future_skills.append({
            "Skill": skill,
            "Demand Score":
            temp["Future_Demand_Score"].mean()
        })

future_df = pd.DataFrame(
    future_skills
)

future_df = future_df.sort_values(
    by="Demand Score",
    ascending=False
).head(15)

fig_future = px.bar(
    future_df,
    x="Skill",
    y="Demand Score",
    color="Demand Score",
    title="Top Future Ready Skills"
)

st.plotly_chart(
    fig_future,
    use_container_width=True
)

# ----------------------------------
# DOWNLOAD
# ----------------------------------

csv = skill_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Skill Report",
    data=csv,
    file_name="skill_demand_report.csv",
    mime="text/csv"
)

# ----------------------------------
# INSIGHTS
# ----------------------------------

st.subheader("📌 Insights")

st.success(
    f"Most demanded skill: {skill_df.iloc[0]['Skill']}"
)

st.info(
    f"Highest future-ready skill: {future_df.iloc[0]['Skill']}"
)

st.warning(
    f"Selected skill appears in {len(skill_jobs)} job records."
)
