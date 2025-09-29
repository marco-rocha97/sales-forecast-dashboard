import os
import pandas as pd
import streamlit as st

@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and clean sales, SKU, and location data."""
    
    base_path = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_path, "data", "raw")
    
    # Sales
    sales_file_path = os.path.join(data_path, "sales.csv")
    df = pd.read_csv(sales_file_path, sep=";")
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df["sku"] = df["sku"].astype(str)
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
    df = df.groupby(["date", "location", "sku"], as_index=False)["quantity"].sum()
    
    # SKU data
    sku_file_path = os.path.join(data_path, "sku_data.csv")
    sku_df = pd.read_csv(sku_file_path, sep=";")
    sku_df.dropna(inplace=True)
    sku_df['SKU'] = sku_df['SKU'].astype(str)
    sku_df['SKU'] = sku_df['SKU'].str.split('.').str[0]
    sku_df.columns = sku_df.columns.str.lower().str.replace(" ", "_")
    sku_df = sku_df[["sku", "material"]]
    
    # Location data
    location_file_path = os.path.join(data_path, "location_data.csv")
    location_df = pd.read_csv(location_file_path, sep=";")
    location_df.columns = location_df.columns.str.lower().str.replace(" ", "_")
    location_df = location_df[["location", "warehouse"]]
    
    # Merge
    df = df.merge(sku_df, on="sku", how="left")
    df = df.merge(location_df, on="location", how="left")
    df.sort_values(by=["date", "location", "sku"], inplace=True)
    
    return df
