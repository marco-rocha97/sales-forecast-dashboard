import altair as alt
import pandas as pd
import streamlit as st

def plot_line(df: pd.DataFrame, y_col: str, split_date: pd.Timestamp = None):
    """Interactive Altair line chart with optional vertical split date line."""
    base = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("date:T", axis=alt.Axis(title=None)),
            y=alt.Y(f"{y_col}:Q", axis=alt.Axis(title=None))
        )
        .properties(width=700, height=400)
    )
    
    if split_date:
        rule = (
            alt.Chart(pd.DataFrame({"date": [split_date]}))
            .mark_rule(color="red", strokeDash=[5, 5])
            .encode(x="date:T")
        )
        chart = base + rule
    else:
        chart = base
    
    st.altair_chart(chart, use_container_width=True)
