import streamlit as st
import pandas as pd
import numpy as np


@st.cache_data
def load_data(file_path):
    """
    Load CSV dataset with caching.
    """

    try:
        df = pd.read_csv(file_path)

        # Remove duplicate rows
        df = df.drop_duplicates()

        return df

    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return pd.DataFrame()


@st.cache_data
def get_dataset_summary(df):
    """
    Generate dataset overview.
    """

    summary = {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum())
    }

    return summary


@st.cache_data
def get_numeric_columns(df):
    """
    Return all numeric columns.
    """

    return df.select_dtypes(
        include=np.number
    ).columns.tolist()


@st.cache_data
def get_categorical_columns(df):
    """
    Return all categorical columns.
    """

    return df.select_dtypes(
        include=["object"]
    ).columns.tolist()


@st.cache_data
def missing_value_report(df):
    """
    Missing value analysis.
    """

    report = pd.DataFrame({
        "Column": df.columns,
        "Missing_Count": df.isnull().sum().values,
        "Missing_Percentage":
            round(
                (df.isnull().sum()/len(df))*100,
                2
            ).values
    })

    return report.sort_values(
        by="Missing_Count",
        ascending=False
    )


@st.cache_data
def correlation_matrix(df):
    """
    Generate correlation matrix.
    """

    numeric_df = df.select_dtypes(include=np.number)

    return numeric_df.corr()


@st.cache_data
def salary_statistics(df):
    """
    Salary insights.
    """

    if "Average_Salary_USD" not in df.columns:
        return {}

    return {
        "Average Salary":
            round(df["Average_Salary_USD"].mean(), 2),

        "Maximum Salary":
            round(df["Average_Salary_USD"].max(), 2),

        "Minimum Salary":
            round(df["Average_Salary_USD"].min(), 2),

        "Median Salary":
            round(df["Average_Salary_USD"].median(), 2)
    }


@st.cache_data
def risk_statistics(df):
    """
    AI Risk analytics.
    """

    if "AI_Replacement_Risk" not in df.columns:
        return {}

    return {
        "Average Risk":
            round(df["AI_Replacement_Risk"].mean(), 2),

        "Maximum Risk":
            round(df["AI_Replacement_Risk"].max(), 2),

        "Minimum Risk":
            round(df["AI_Replacement_Risk"].min(), 2)
    }


@st.cache_data
def future_demand_statistics(df):
    """
    Future demand insights.
    """

    if "Future_Demand_Score" not in df.columns:
        return {}

    return {
        "Average Demand":
            round(df["Future_Demand_Score"].mean(), 2),

        "Maximum Demand":
            round(df["Future_Demand_Score"].max(), 2),

        "Minimum Demand":
            round(df["Future_Demand_Score"].min(), 2)
    }


@st.cache_data
def industry_summary(df):
    """
    Industry-wise aggregation.
    """

    if "Industry" not in df.columns:
        return pd.DataFrame()

    return (
        df.groupby("Industry")
        .agg({
            "Average_Salary_USD": "mean",
            "AI_Replacement_Risk": "mean",
            "Future_Demand_Score": "mean"
        })
        .reset_index()
    )


@st.cache_data
def country_summary(df):
    """
    Country-wise aggregation.
    """

    if "Country" not in df.columns:
        return pd.DataFrame()

    return (
        df.groupby("Country")
        .agg({
            "Average_Salary_USD": "mean",
            "AI_Replacement_Risk": "mean",
            "Future_Demand_Score": "mean"
        })
        .reset_index()
    )


def validate_required_columns(df):
    """
    Validate dataset columns.
    """

    required_columns = [
        "Industry",
        "Country",
        "Average_Salary_USD",
        "AI_Replacement_Risk",
        "Future_Demand_Score"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    return missing
