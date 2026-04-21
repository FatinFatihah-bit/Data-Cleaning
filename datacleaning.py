import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

st.set_page_config(page_title="Data Cleaning App", layout="wide")

# ================= Utility Functions ================= #

def detect_missing(df: pd.DataFrame):
    return df.isnull().sum()

def handle_missing(df: pd.DataFrame, method="mean"):
    clean_df = df.copy()
    for col in clean_df.columns:
        if clean_df[col].dtype in ["float64", "int64"]:
            if method == "mean":
                clean_df[col].fillna(clean_df[col].mean(), inplace=True)
            elif method == "median":
                clean_df[col].fillna(clean_df[col].median(), inplace=True)
        else:
            clean_df[col].fillna(clean_df[col].mode()[0], inplace=True)
    return clean_df

def remove_duplicates(df: pd.DataFrame):
    return df.drop_duplicates()

def download_button(df: pd.DataFrame):
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    st.download_button(
        label="📥 Download Cleaned CSV",
        data=buffer,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )


# ================= UI ================= #

st.title("🧹 Data Cleaning App (Advanced)")

uploaded_file = st.file_uploader("📂 Upload CSV / Excel", type=["csv", "xlsx"])

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]

    if file_extension == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📊 Original Data Preview")
    st.dataframe(df.head())

    st.write("---")

    # ========= Missing Stats ========= #
    st.subheader("📉 Missing Value Summary")
    missing_df = detect_missing(df)
    st.write(missing_df)

    st.write(f"👉 Total missing values: **{missing_df.sum()}**")

    # ========= Duplicate Stats ========= #
    dup_count = df.duplicated().sum()
    st.subheader("📦 Duplicate Records")
    st.write(f"Duplicates found: **{dup_count}**")

    st.write("---")

    # ========= Cleaning Options ========= #
    st.header("🧰 Data Cleaning Actions")
    cleaned_df = df.copy()

    # 👉 Remove Missing
    if st.button("❌ Drop Missing Values (Remove Rows)"):
        cleaned_df = df.dropna()
        st.success("Missing values removed.")
        st.dataframe(cleaned_df)

    # 👉 Impute Missing
    method = st.selectbox("🔄 Missing Value Handling Method", ("mean", "median", "mode"))
    if st.button(f"✨ Fill Missing using {method.upper()}"):
        cleaned_df = handle_missing(df, method)
        st.success(f"Missing values handled using {method.upper()}.")
        st.dataframe(cleaned_df)

    # 👉 Remove Duplicates
    if st.button("🚮 Remove Duplicate Rows"):
        cleaned_df = remove_duplicates(df)
        st.success("Duplicates removed.")
        st.dataframe(cleaned_df)

    st.write("---")

    # ========= Download ========= #
    st.subheader("📥 Export Clean File")
    if st.button("Prepare Clean Data for Download"):
        download_button(cleaned_df)
else:
    st.info("📥 Please upload a file to begin.")
