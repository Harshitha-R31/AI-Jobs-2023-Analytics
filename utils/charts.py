import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns


# -----------------------------
# KPI CARD COLORS
# -----------------------------

PLOTLY_TEMPLATE = "plotly_dark"


# -----------------------------
# AI RISK DISTRIBUTION
# -----------------------------

def risk_distribution_chart(df):

    fig = px.histogram(
        df,
        x="AI_Replacement_Risk",
        nbins=25,
        title="AI Replacement Risk Distribution",
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        height=500
    )

    return fig


# -----------------------------
# SALARY DISTRIBUTION
# -----------------------------

def salary_distribution_chart(df):

    fig = px.histogram(
        df,
        x="Average_Salary_USD",
        nbins=30,
        title="Salary Distribution",
        template=PLOTLY_TEMPLATE
    )

    return fig


# -----------------------------
# INDUSTRY AI RISK
# -----------------------------

def industry_risk_chart(df):

    data = (
        df.groupby("Industry")["AI_Replacement_Risk"]
        .mean()
        .reset_index()
        .sort_values(
            by="AI_Replacement_Risk",
            ascending=False
        )
    )

    fig = px.bar(
        data,
        x="Industry",
        y="AI_Replacement_Risk",
        color="AI_Replacement_Risk",
        title="Average AI Risk by Industry",
        template=PLOTLY_TEMPLATE
    )

    return fig


# -----------------------------
# FUTURE DEMAND
# -----------------------------

def future_demand_chart(df):

    data = (
        df.groupby("Industry")["Future_Demand_Score"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        data,
        x="Industry",
        y="Future_Demand_Score",
        color="Future_Demand_Score",
        title="Future Demand by Industry",
        template=PLOTLY_TEMPLATE
    )

    return fig


# -----------------------------
# SALARY VS AI RISK
# -----------------------------

def salary_vs_risk_chart(df):

    fig = px.scatter(
        df,
        x="Average_Salary_USD",
        y="AI_Replacement_Risk",
        color="Industry",
        title="Salary vs AI Risk",
        template=PLOTLY_TEMPLATE
    )

    return fig


# -----------------------------
# EXPERIENCE VS SALARY
# -----------------------------

def experience_salary_chart(df):

    fig = px.scatter(
        df,
        x="Years_Experience",
        y="Average_Salary_USD",
        color="Industry",
        title="Experience vs Salary",
        template=PLOTLY_TEMPLATE
    )

    return fig


# -----------------------------
# COUNTRY SALARY MAP
# -----------------------------

def country_salary_map(df):

    country_salary = (
        df.groupby("Country")
        ["Average_Salary_USD"]
        .mean()
        .reset_index()
    )

    fig = px.choropleth(
        country_salary,
        locations="Country",
        locationmode="country names",
        color="Average_Salary_USD",
        title="Average Salary Across Countries",
        template=PLOTLY_TEMPLATE
    )

    return fig


# -----------------------------
# COUNTRY AI RISK MAP
# -----------------------------

def country_risk_map(df):

    country_risk = (
        df.groupby("Country")
        ["AI_Replacement_Risk"]
        .mean()
        .reset_index()
    )

    fig = px.choropleth(
        country_risk,
        locations="Country",
        locationmode="country names",
        color="AI_Replacement_Risk",
        title="AI Risk by Country"
    )

    return fig


# -----------------------------
# JOB GROWTH CHART
# -----------------------------

def job_growth_chart(df):

    data = (
        df.groupby("Industry")
        ["Job_Growth_2030"]
        .mean()
        .reset_index()
        .sort_values(
            by="Job_Growth_2030",
            ascending=False
        )
    )

    fig = px.bar(
        data,
        x="Industry",
        y="Job_Growth_2030",
        color="Job_Growth_2030",
        title="Projected Job Growth by 2030",
        template=PLOTLY_TEMPLATE
    )

    return fig


# -----------------------------
# EDUCATION LEVEL ANALYSIS
# -----------------------------

def education_chart(df):

    if "Education_Level" not in df.columns:
        return None

    data = (
        df["Education_Level"]
        .value_counts()
        .reset_index()
    )

    data.columns = [
        "Education_Level",
        "Count"
    ]

    fig = px.pie(
        data,
        names="Education_Level",
        values="Count",
        title="Education Level Distribution"
    )

    return fig


# -----------------------------
# CORRELATION HEATMAP
# -----------------------------

def correlation_heatmap(df):

    numeric_df = df.select_dtypes(
        include="number"
    )

    corr = numeric_df.corr()

    fig, ax = plt.subplots(
        figsize=(12, 8)
    )

    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        ax=ax
    )

    plt.title(
        "Correlation Matrix"
    )

    return fig


# -----------------------------
# TOP INDUSTRIES
# -----------------------------

def top_industries_chart(df):

    data = (
        df["Industry"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    data.columns = [
        "Industry",
        "Count"
    ]

    fig = px.bar(
        data,
        x="Industry",
        y="Count",
        color="Count",
        title="Top Industries",
        template=PLOTLY_TEMPLATE
    )

    return fig


# -----------------------------
# AI RISK CATEGORIES
# -----------------------------

def risk_category_chart(df):

    bins = [0, 0.3, 0.6, 1]

    labels = [
        "Low Risk",
        "Medium Risk",
        "High Risk"
    ]

    df["Risk_Category"] = pd.cut(
        df["AI_Replacement_Risk"],
        bins=bins,
        labels=labels
    )

    risk_data = (
        df["Risk_Category"]
        .value_counts()
        .reset_index()
    )

    risk_data.columns = [
        "Risk_Category",
        "Count"
    ]

    fig = px.pie(
        risk_data,
        names="Risk_Category",
        values="Count",
        title="AI Risk Categories"
    )

    return fig


# -----------------------------
# DEMAND VS RISK
# -----------------------------

def demand_vs_risk_chart(df):

    fig = px.scatter(
        df,
        x="Future_Demand_Score",
        y="AI_Replacement_Risk",
        color="Industry",
        size="Average_Salary_USD",
        hover_name="Job_Title",
        title="Future Demand vs AI Risk",
        template=PLOTLY_TEMPLATE
    )

    return fig


# -----------------------------
# DASHBOARD INSIGHTS
# -----------------------------

def generate_insights(df):

    insights = {}

    insights["Highest Salary Industry"] = (
        df.groupby("Industry")
        ["Average_Salary_USD"]
        .mean()
        .idxmax()
    )

    insights["Highest AI Risk Industry"] = (
        df.groupby("Industry")
        ["AI_Replacement_Risk"]
        .mean()
        .idxmax()
    )

    insights["Highest Future Demand Industry"] = (
        df.groupby("Industry")
        ["Future_Demand_Score"]
        .mean()
        .idxmax()
    )

    insights["Highest Growth Industry"] = (
        df.groupby("Industry")
        ["Job_Growth_2030"]
        .mean()
        .idxmax()
    )

    return insights
