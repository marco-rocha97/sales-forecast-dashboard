import pandas as pd
from pycaret.regression import setup, compare_models, finalize_model, predict_model
from category_encoders import TargetEncoder
from utils import prepare_data
import streamlit as st

@st.cache_resource
def train_model(train_df: pd.DataFrame, warehouse: str, material: str):
    """Train and return the finalized PyCaret model, encoder and best model."""
    encoder = TargetEncoder(cols=["location", "sku"])
    train_df = prepare_data(train_df, encoder, fit=True)
    
    features_to_drop = ["location", "sku", "date"]
    train_df_model = train_df.drop(columns=features_to_drop)
    
    s = setup(
        train_df_model,
        target="quantity",
        session_id=123,
        use_gpu=False,
        verbose=False
    )
    
    best = compare_models(include=['lr', 'ada', 'xgboost', 'lightgbm'])
    final_model = finalize_model(best)
    
    return final_model, encoder, best

def forecast(model, encoder, train_df: pd.DataFrame, forecast_df: pd.DataFrame) -> pd.DataFrame:
    """Generate forecasted values."""
    features_to_drop = ["location", "sku", "date"]
    forecast_df = prepare_data(forecast_df, encoder, fit=False)
    forecast_features = forecast_df.drop(columns=features_to_drop + ["quantity"])
    
    predictions = predict_model(model, data=forecast_features)
    
    forecast_df = forecast_df.reset_index()[["date", "location", "sku", "quantity"]]
    forecast_df["predicted_quantity"] = predictions["prediction_label"].values
    
    return forecast_df
