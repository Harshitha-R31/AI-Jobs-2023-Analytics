import pandas as pd


def executive_summary(df):
    """
    Generate executive-level insights.
    """

    insights = []

    insights.append(
        f"Dataset contains {len(df):,} job records."
    )

    insights.append(
        f"Average salary is ${df['Average_Salary_USD'].mean():,.0f}."
    )

    insights.append(
        f"Average AI replacement risk is {df['AI_Replacement_Risk'].mean():.2f}."
    )

    insights.append(
        f"Average future demand score is {df['Future_Demand_Score'].mean():.2f}."
    )

    return insights


def industry_insights(df):
    """
    Industry-level insights.
    """

    insights = {}

    salary_industry = (
        df.groupby("Industry")
        ["Average_Salary_USD"]
        .mean()
        .idxmax()
    )

    risk_industry = (
        df.groupby("Industry")
        ["AI_Replacement_Risk"]
        .mean()
        .idxmax()
    )

    growth_industry = (
        df.groupby("Industry")
        ["Job_Growth_2030"]
        .mean()
        .idxmax()
    )

    demand_industry = (
        df.groupby("Industry")
        ["Future_Demand_Score"]
        .mean()
        .idxmax()
    )

    insights["Highest Paying Industry"] = salary_industry
    insights["Highest AI Risk Industry"] = risk_industry
    insights["Fastest Growing Industry"] = growth_industry
    insights["Highest Demand Industry"] = demand_industry

    return insights


def country_insights(df):
    """
    Country-level insights.
    """

    insights = {}

    salary_country = (
        df.groupby("Country")
        ["Average_Salary_USD"]
        .mean()
        .idxmax()
    )

    demand_country = (
        df.groupby("Country")
        ["Future_Demand_Score"]
        .mean()
        .idxmax()
    )

    insights["Highest Salary Country"] = salary_country
    insights["Highest Demand Country"] = demand_country

    return insights


def future_ready_jobs(df):
    """
    Jobs with high demand and low AI risk.
    """

    jobs = df[
        (df["Future_Demand_Score"] >= 0.7)
        &
        (df["AI_Replacement_Risk"] <= 0.4)
    ]

    return jobs[
        [
            "Job_Title",
            "Industry",
            "Average_Salary_USD",
            "Future_Demand_Score",
            "AI_Replacement_Risk"
        ]
    ].sort_values(
        by="Future_Demand_Score",
        ascending=False
    )


def high_risk_jobs(df):
    """
    Jobs at high risk of automation.
    """

    jobs = df[
        df["AI_Replacement_Risk"] >= 0.8
    ]

    return jobs[
        [
            "Job_Title",
            "Industry",
            "AI_Replacement_Risk",
            "Average_Salary_USD"
        ]
    ].sort_values(
        by="AI_Replacement_Risk",
        ascending=False
    )


def top_paying_jobs(df, top_n=10):
    """
    Highest salary jobs.
    """

    return (
        df[
            [
                "Job_Title",
                "Industry",
                "Average_Salary_USD"
            ]
        ]
        .sort_values(
            by="Average_Salary_USD",
            ascending=False
        )
        .head(top_n)
    )


def future_ready_industries(df):
    """
    Calculate future readiness score.
    """

    industry_df = (
        df.groupby("Industry")
        .agg({
            "Future_Demand_Score": "mean",
            "Job_Growth_2030": "mean",
            "AI_Replacement_Risk": "mean"
        })
        .reset_index()
    )

    industry_df["Future_Readiness"] = (
        industry_df["Future_Demand_Score"]
        +
        industry_df["Job_Growth_2030"]
        -
        industry_df["AI_Replacement_Risk"]
    )

    return industry_df.sort_values(
        by="Future_Readiness",
        ascending=False
    )


def salary_recommendations(df):
    """
    Salary recommendations.
    """

    avg_salary = df["Average_Salary_USD"].mean()

    if avg_salary > 100000:
        return (
            "Dataset indicates strong earning potential "
            "across industries."
        )

    elif avg_salary > 70000:
        return (
            "Most industries provide competitive salaries."
        )

    else:
        return (
            "Salary growth opportunities may require "
            "specialized skill development."
        )


def automation_recommendations(df):
    """
    AI automation recommendations.
    """

    avg_risk = df["AI_Replacement_Risk"].mean()

    if avg_risk > 0.7:
        return (
            "Many jobs face significant automation risk. "
            "Upskilling is strongly recommended."
        )

    elif avg_risk > 0.5:
        return (
            "Moderate automation risk exists. "
            "Continuous learning is beneficial."
        )

    else:
        return (
            "Automation risk remains relatively low."
        )


def future_demand_recommendations(df):
    """
    Future demand recommendations.
    """

    avg_demand = df["Future_Demand_Score"].mean()

    if avg_demand > 0.7:
        return (
            "Strong future job demand is expected."
        )

    elif avg_demand > 0.5:
        return (
            "Moderate demand growth is expected."
        )

    else:
        return (
            "Demand growth may be limited."
        )


def generate_dashboard_report(df):
    """
    Complete dashboard report.
    """

    report = {
        "Total Jobs": len(df),
        "Average Salary":
            round(
                df["Average_Salary_USD"].mean(),
                2
            ),
        "Average AI Risk":
            round(
                df["AI_Replacement_Risk"].mean(),
                2
            ),
        "Average Future Demand":
            round(
                df["Future_Demand_Score"].mean(),
                2
            )
    }

    return report
