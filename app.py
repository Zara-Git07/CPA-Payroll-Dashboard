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

    st.header("Payroll Dashboard")

    uploaded_file = st.file_uploader(
        "Upload Payroll Excel File",
        type=["xlsx", "csv"]
    )

    if uploaded_file:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully")

        st.subheader("Columns Found")

        st.write(df.columns.tolist())

        st.subheader("Payroll Data")

        st.dataframe(df)

    else:
        st.info("Please upload a payroll file.")

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

Thank you for your email.

We have received your request and our team will review it shortly.

Summary:
{email_text[:100]}

Best Regards,
CPA Team
"""

            st.text_area(
                "Suggested Reply",
                reply,
                height=250
            )
