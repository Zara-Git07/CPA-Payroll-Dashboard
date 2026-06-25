import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="CPA Payroll Dashboard",
    layout="wide"
)

st.title("CPA Payroll Dashboard")

uploaded_file = st.file_uploader(
    "Upload Payroll Excel File",
    type=["xlsx"]
)

if uploaded_file:

    # Read Excel File
    df = pd.read_excel(uploaded_file)
    st.write(df.columns.tolist())

    st.subheader("Raw Payroll Data")
    st.dataframe(df)

    # Convert Hourly Rate
    def convert_rate(rate):

        try:

            if pd.isna(rate):
                return np.nan

            rate = str(rate)

            if "Salary" in rate.upper():
                return np.nan

            return float(
                rate.replace("$", "")
                .replace(",", "")
                .strip()
            )

        except:
            return np.nan

    # Clean Data
    df["Numeric Rate"] = df["Hourly Rate"].apply(convert_rate)

    df["Regular Hours"] = pd.to_numeric(
        df["Regular Hours"],
        errors="coerce"
    ).fillna(0)

    df["Overtime Hours"] = pd.to_numeric(
        df["Overtime Hours"],
        errors="coerce"
    ).fillna(0)

    # Hourly Employees Only
    hourly_df = df[
        df["Numeric Rate"].notna()
    ].copy()

    # Payroll Calculations
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

    # Dashboard KPIs
    st.subheader("Payroll Summary")

    col1, col2, col3, col4 = st.columns(4)

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
        round(
            hourly_df["Overtime Hours"].sum(),
            2
        )
    )

    col4.metric(
        "OT Employees",
        len(
            hourly_df[
                hourly_df["Overtime Hours"] > 0
            ]
        )
    )

    # Overtime Alerts
    st.subheader("🚨 Overtime Alerts")

    overtime_alerts = hourly_df[
        hourly_df["Overtime Hours"] > 5
    ]

    if len(overtime_alerts) > 0:

        st.dataframe(
            overtime_alerts[
                [
                    "First Name",
                    "Last Name",
                    "Job Title",
                    "Overtime Hours",
                    "Gross Pay"
                ]
            ]
        )

    else:

        st.success(
            "No overtime alerts found"
        )

    # Payroll by Job Title
    st.subheader("📊 Payroll by Job Title")

    job_summary = (
        hourly_df
        .groupby("Job Title")["Gross Pay"]
        .sum()
        .reset_index()
    )

    st.dataframe(job_summary)

    st.bar_chart(
        job_summary.set_index("Job Title")
    )

    # Top Employees
    st.subheader("🏆 Top Payroll Employees")

    top_paid = (
        hourly_df
        .sort_values(
            by="Gross Pay",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_paid[
            [
                "First Name",
                "Last Name",
                "Job Title",
                "Gross Pay"
            ]
        ]
    )

    # Payroll Register
    st.subheader("📋 Payroll Register")

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

    # Download Report
    csv = hourly_df.to_csv(
        index=False
    )

    st.download_button(
        label="⬇ Download Payroll Report",
        data=csv,
        file_name="Payroll_Report.csv",
        mime="text/csv"
    )

else:

    st.info(
        "Please upload a payroll Excel file to begin."
    )
