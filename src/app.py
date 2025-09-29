import os
import streamlit as st
import pandas as pd
import altair as alt

from data_loader import load_data
from plots import plot_line
from model import train_model, forecast

# ----------------------------- Streamlit UI -----------------------------
st.title("📊 Sales Forecast Dashboard")

# Load dataset
daily_sales_df = load_data()

# Filters
warehouses = sorted(daily_sales_df["warehouse"].dropna().unique())
materials = sorted(daily_sales_df["material"].dropna().unique())

selected_warehouse = st.selectbox("Select Warehouse", warehouses, index=warehouses.index("São Paulo"))
selected_material = st.selectbox("Select Material", materials)

filtered_df = daily_sales_df[
    (daily_sales_df["warehouse"] == selected_warehouse) &
    (daily_sales_df["material"] == selected_material)
]

# Split date (UI configurable)
split_prediction_date = st.date_input(
    "Train/Test Split Date",
    pd.to_datetime("2025-08-31")
)
split_prediction_date = pd.to_datetime(split_prediction_date)

# Raw data
st.subheader("Raw Daily Sales")
plot_line(filtered_df, y_col="quantity", split_date=split_prediction_date)

# Train model
train_df = filtered_df[filtered_df["date"] <= split_prediction_date].copy()
train_df.set_index("date", inplace=True)

try:
    if train_df.empty:
        st.warning("❌ Data not found for the combination of Warehouse, Material and Date. Please choose another one.")
    else:
        model, encoder, best = train_model(train_df, selected_warehouse, selected_material)
        st.success(f"✅ Best model: {best.__class__.__name__}")

        # Forecast
        future_df = filtered_df[filtered_df["date"] > split_prediction_date].copy()
        future_df.set_index("date", inplace=True)

        if future_df.empty:
            st.warning("⚠️ No future data available for this Warehouse/Material after the split date.")
        else:
            final_forecast_df = forecast(model, encoder, train_df, future_df)

            # Plot results
            st.subheader("Forecast vs Actual Sales")

            chart = (
                alt.Chart(final_forecast_df)
                .transform_fold(
                    ["quantity", "predicted_quantity"],
                    as_=["Type", "Sales"]
                )
                .mark_line()
                .encode(
                    x=alt.X("date:T", axis=alt.Axis(title=None)),
                    y=alt.Y("Sales:Q", axis=alt.Axis(title=None)),
                    color=alt.Color(
                        "Type:N",
                        legend=alt.Legend(
                            title="Sales Type",
                            labelExpr="datum.value == 'quantity' ? 'Actual' : 'Forecast'"
                        )
                    )
                )
                .properties(width=700, height=400)
            )

            st.altair_chart(chart, use_container_width=True)

except KeyError:
    st.error("❌ Data not found for the combination of Warehouse, Material and Date. Please choose another one.")
