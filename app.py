import streamlit as st
import pandas as pd

st.title("CPA Payroll Dashboard")

uploaded_file = st.file_uploader(
    "Upload Payroll File",
    type=["xlsx"]
)

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    df["Overtime Hours"] = df["Overtime Hours"].fillna(0)

    df["Regular Pay"] = (
        df["Regular Hours"] *
        df["Hourly Rate"]
    )

    df["Overtime Pay"] = (
        df["Overtime Hours"] *
        df["Hourly Rate"] *
        1.5
    )

    df["Gross Pay"] = (
        df["Regular Pay"] +
        df["Overtime Pay"]
    )

    st.subheader("Payroll Summary")

    st.metric(
        "Employees",
        len(df)
    )

    st.metric(
        "Gross Payroll",
        f"${df['Gross Pay'].sum():,.2f}"
    )

    st.dataframe(df)
