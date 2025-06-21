# streamlit_app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os
st.set_page_config(page_title="📊 CSV File Analyzer", layout="wide")

st.title("📊 CSV File Analyzer")
st.markdown("""
Upload your CSV file and select what you want to explore from the dropdown menu below.  
This tool helps you analyze your dataset quickly and interactively 🚀
""")

# Upload CSV File
uploaded_file = st.file_uploader("📂 Upload CSV", type=["csv", "xlsx", "xls"])


try:
    filename = uploaded_file.name
    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext == ".csv":
        df = pd.read_csv(uploaded_file)
    elif file_ext in [".xlsx", ".xls"]:
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file format.")
        st.stop()

    st.success(f"✅ File '{filename}' uploaded and processed successfully!")


    # Navigation Dropdown
    choice = st.selectbox(
        "Choose an operation",
        [
            "🔍 Data Preview",
            "📝 Summary Report",
            "📈 Basic Statistics",
            "📋 Data Types",
            "⚠️ Missing Values",
            "📉 Correlation Heatmap",
            "📊 Pairplot",
            "📦 Distribution Plot",
            "🧹 Data Cleaning",
            "🧠 Custom Query"
        ]
    )

    numeric_cols = df.select_dtypes(include=['int64', 'float64'])

    # Handle each choice
    if choice == "🔍 Data Preview":
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

    elif choice == "📈 Basic Statistics":
        st.subheader("📈 Basic Statistics")
        st.write(df.describe())

    elif choice == "📋 Data Types":
        st.subheader("📋 Data Types")
        st.write(df.dtypes)

    elif choice == "⚠️ Missing Values":
        st.subheader("⚠️ Missing Values")
        st.write(df.isnull().sum())

    elif choice == "📉 Correlation Heatmap":
        st.subheader("📉 Correlation Heatmap")
        if not numeric_cols.empty:
            fig = plt.figure(figsize=(10, 6))
            sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm")
            st.pyplot(fig)
        else:
            st.warning("No numeric columns available.")

    elif choice == "📊 Pairplot":
        st.subheader("📊 Pairplot")
        if len(numeric_cols.columns) >= 2:
            fig = sns.pairplot(numeric_cols)
            st.pyplot(fig)
        else:
            st.info("Need at least 2 numeric columns for pairplot.")

    elif choice == "📦 Distribution Plot":
        st.subheader("📦 Distribution Plot")
        if not numeric_cols.empty:
            col = st.selectbox("Select a column", numeric_cols.columns)
            fig2 = px.histogram(df, x=col, nbins=30, title=f'Distribution of {col}')
            st.plotly_chart(fig2)
        else:
            st.warning("No numeric columns found.")

    elif choice == "🧹 Data Cleaning":
        st.subheader("🧹 Data Cleaning Options")
        df1=df.copy()
        if st.button("Drop Missing Values"):
            df1.dropna(inplace=True)
            st.dataframe(df1)
            st.success("Missing values removed.")
        if st.button("Drop Duplicates"):
            df1.drop_duplicates(inplace=True)
            st.dataframe(df1)
            st.success("Duplicate rows removed.")
             # ✅ Download button for cleaned CSV
        cleaned_csv = df1.to_csv(index=False)
        st.download_button(
            label="📥 Download Cleaned CSV",
            data=cleaned_csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )

    elif choice == "🧠 Custom Query":
        st.subheader("🧠 Custom Query")
        query = st.text_input("Enter your query (e.g., age > 25 and gender == 'Male')")
        if query:
            try:
                result = df.query(query)
                st.dataframe(result)
                st.write(result.size)
                csv = result.to_csv(index=False)
                st.download_button(
                    label="📥 Download Cleaned CSV",
                    data=csv,
                    file_name="query_csv.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Invalid query: {e}")

    elif choice == "📝 Summary Report":
        st.subheader("📝 Summary Report")
        st.markdown(f"""
        - Total Rows: `{df.shape[0]}`
        - Total Columns: `{df.shape[1]}`
        - Numeric Columns: `{len(numeric_cols.columns)}`
        - Missing Values: `{df.isnull().sum().sum()}`
        - Duplicate Rows: `{df.duplicated().sum()}`
        """)

except Exception as e:
    st.error(f"Failed to load file: {e}")
    st.stop()