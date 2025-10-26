"""
Data Preprocessing Script
Prepares and cleans data for model training
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATASETS_DIR = 'datasets'


def preprocess_price_data(df):
    """
    Preprocess price data
    - Handle missing values
    - Remove outliers
    - Feature engineering
    """
    logger.info("Preprocessing price data...")
    
    # Handle missing values
    df = df.dropna()
    
    # Remove outliers (3 sigma rule)
    for energy_type in df['energy_type'].unique():
        mask = df['energy_type'] == energy_type
        prices = df.loc[mask, 'price']
        mean, std = prices.mean(), prices.std()
        df = df[~((mask) & ((prices < mean - 3*std) | (prices > mean + 3*std)))]
    
    # Add time features
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['month'] = df['timestamp'].dt.month
    
    # Add moving averages
    for window in [24, 168]:  # 24h and 7 days
        df[f'price_ma_{window}'] = df.groupby('energy_type')['price'].transform(
            lambda x: x.rolling(window=window, min_periods=1).mean()
        )
    
    # Add volatility
    df['price_volatility'] = df.groupby('energy_type')['price'].transform(
        lambda x: x.rolling(window=24, min_periods=1).std()
    )
    
    logger.info(f"Preprocessed {len(df)} records")
    
    return df


def preprocess_demand_data(df):
    """
    Preprocess demand data
    """
    logger.info("Preprocessing demand data...")
    
    # Handle missing values
    df = df.fillna(method='ffill')
    
    # Add lag features
    for lag in [1, 24, 168]:
        df[f'demand_lag_{lag}'] = df.groupby('energy_type')['demand'].shift(lag)
    
    # Add rolling statistics
    df['demand_rolling_mean'] = df.groupby('energy_type')['demand'].transform(
        lambda x: x.rolling(window=24, min_periods=1).mean()
    )
    
    df['demand_rolling_std'] = df.groupby('energy_type')['demand'].transform(
        lambda x: x.rolling(window=24, min_periods=1).std()
    )
    
    logger.info(f"Preprocessed {len(df)} records")
    
    return df


def create_features(df, target_col='price'):
    """
    Create additional features for better predictions
    """
    logger.info("Creating features...")
    
    # Price change
    if target_col in df.columns:
        df['price_change'] = df.groupby('energy_type')[target_col].pct_change()
        df['price_change_abs'] = df['price_change'].abs()
    
    # Interaction features
    if 'hour' in df.columns and 'day_of_week' in df.columns:
        df['is_peak_hour'] = ((df['hour'] >= 9) & (df['hour'] <= 21)).astype(int)
        df['is_weekday'] = (df['day_of_week'] < 5).astype(int)
        df['peak_weekday'] = df['is_peak_hour'] * df['is_weekday']
    
    logger.info("Features created")
    
    return df


def save_processed_data(df, filename):
    """Save processed data"""
    filepath = f'{DATASETS_DIR}/{filename}'
    df.to_csv(filepath, index=False)
    logger.info(f"Saved processed data to {filepath}")


if __name__ == '__main__':
    # Example usage
    logger.info("Data preprocessing complete")
