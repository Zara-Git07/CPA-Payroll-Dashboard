import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CPA Payroll Dashboard",
    layout="wide"
)

st.title("CPA Payroll Dashboard")

tab1, tab2 = st.tabs([
    "Payroll Dashboard",
    "AI Email Assistant"
])

with tab1:

    uploaded_file = st.file_uploader(
        "Upload Payroll File",
        type=["xlsx", "csv"]
    )

    if uploaded_file:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("Payroll Data")
        st.dataframe(df)

        # Convert numeric columns
        df["Hourly Rate"] = pd.to_numeric(
            df["Hourly Rate"],
            errors="coerce"
        )

        df["Regular Hours"] = pd.to_numeric(
            df["Regular Hours"],
            errors="coerce"
        ).fillna(0)

        df["Overtime Hours"] = pd.to_numeric(
            df["Overtime Hours"],
            errors="coerce"
        ).fillna(0)

        # Payroll calculations
        df["Regular Pay"] = (
            df["Hourly Rate"] *
            df["Regular Hours"]
        )

        df["OT Pay"] = (
            df["Hourly Rate"] *
            df["Overtime Hours"] *
            1.5
        )

        df["Gross Pay"] = (
            df["Regular Pay"] +
            df["OT Pay"]
        )

        st.subheader("Payroll Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Employees",
            len(df)
        )

        col2.metric(
            "Total Payroll",
            f"${df['Gross Pay'].sum():,.2f}"
        )

        col3.metric(
            "Overtime Hours",
            round(df["Overtime Hours"].sum(), 2)
        )

        col4.metric(
            "Average Pay",
            f"${df['Gross Pay'].mean():,.2f}"
        )

        st.subheader("Overtime Alerts")

        overtime_df = df[
            df["Overtime Hours"] > 5
        ]

        if len(overtime_df) > 0:
            st.dataframe(
                overtime_df[
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
                "No overtime alerts found."
            )

        st.subheader("Payroll By Job Title")

        job_summary = (
            df.groupby("Job Title")["Gross Pay"]
            .sum()
            .reset_index()
        )

        st.dataframe(job_summary)

        st.bar_chart(
            job_summary.set_index("Job Title")
        )

        st.subheader("Top Paid Employees")

        top_paid = (
            df.sort_values(
                "Gross Pay",
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

        st.subheader("Payroll Register")

        st.dataframe(
            df[
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

        csv = df.to_csv(index=False)

        st.download_button(
            label="Download Payroll Report",
            data=csv,
            file_name="Payroll_Report.csv",
            mime="text/csv"
        )

    else:
        st.info(
            "Upload a payroll file to begin."
        )

with tab2:

    st.header("AI Email Assistant")

    email_text = st.text_area(
        "Paste Client Email",
        height=200
    )

    if st.button("Generate Reply"):

        if email_text:

            reply = f"""
Hello,

Thank you for contacting us.

We have received your request and our team is reviewing it.

Summary:
{email_text[:150]}

Best Regards,
CPA Team
"""

            st.text_area(
                "Suggested Reply",
                reply,
                height=250
            )
