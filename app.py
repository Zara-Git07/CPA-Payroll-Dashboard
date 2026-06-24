import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="CPA Payroll Dashboard", layout="wide")

st.title("CPA Payroll Dashboard")

uploaded_file = st.file_uploader(
    "Upload Payroll Excel File",
    type=["xlsx"]
)

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.subheader("Raw Payroll Data")
    st.dataframe(df)

    def convert_rate(rate):

        try:
            if pd.isna(rate):
                return np.nan

            rate = str(rate)

            if "Salary" in rate or "SALARY" in rate:
                return np.nan

            return float(
                rate.replace("$", "")
                .replace(",", "")
                .strip()
            )

        except:
            return np.nan

    df["Numeric Rate"] = df["Hourly Rate"].apply(convert_rate)

    df["Regular Hours"] = pd.to_numeric(
        df["Regular Hours"],
        errors="coerce"
    ).fillna(0)

    df["Overtime Hours"] = pd.to_numeric(
        df["Overtime Hours"],
        errors="coerce"
    ).fillna(0)

    hourly_df = df[df["Numeric Rate"].notna()].copy()

    hourly_df["Regular Pay"] = (
        hourly_df["Regular Hours"]
        * hourly_df["Numeric Rate"]
    )

    hourly_df["OT Pay"] = (
        hourly_df["Overtime Hours"]
        * hourly_df["Numeric Rate"]
        * 1.5
    )

    hourly_df["Gross Pay"] = (
        hourly_df["Regular Pay"]
        + hourly_df["OT Pay"]
    )

    st.subheader("Payroll Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Employees",
        len(hourly_df)
    )

    col2.metric(
        "Total Payroll",
        f"${hourly_df['Gross Pay'].sum():,.2f}"
    )

    col3.metric(
        "Overtime Hours",
        f"{hourly_df['Overtime Hours'].sum():,.2f}"
    )

    st.subheader("Payroll Register")

    st.dataframe(
        hourly_df[
            [
                "Last Name",
                "First Name",
                "Job Title",
                "Regular Hours",
                "Overtime Hours",
                "Gross Pay"
            ]
        ]
    )

    csv = hourly_df.to_csv(index=False)

    st.download_button(
        label="Download Payroll Report",
        data=csv,
        file_name="Payroll_Report.csv",
        mime="text/csv"
    )
