import pandas as pd
from category_encoders import TargetEncoder

def daily_resample(df: pd.DataFrame) -> pd.DataFrame:
    """Resample sales data to daily frequency per location and SKU."""
    return (
        df.groupby(['location', 'sku'])
        .resample('D')['quantity']
        .sum()
        .fillna(0)
        .reset_index()
    )

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add calendar features from 'date'."""
    df = df.copy()
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_of_year'] = df['date'].dt.dayofyear
    df['week_of_year'] = df['date'].dt.isocalendar().week.astype(int)
    df['is_weekend'] = (df['day_of_week'].isin([5, 6])).astype(int)
    return df

def prepare_data(df: pd.DataFrame, encoder: TargetEncoder = None, fit: bool = False) -> pd.DataFrame:
    """Resample, add features, and encode categorical variables."""
    df = daily_resample(df)
    df = create_features(df)
    
    if encoder:
        if fit:
            df[['location_encoded', 'sku_encoded']] = encoder.fit_transform(
                df[['location', 'sku']], df['quantity']
            )
        else:
            df[['location_encoded', 'sku_encoded']] = encoder.transform(
                df[['location', 'sku']]
            )
    
    return df
