"""
Model Training Script
Trains all AI/ML models for the energy trading platform
"""

import argparse
import os
import pickle
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directories
MODELS_DIR = 'trained_models'
DATASETS_DIR = 'datasets'

os.makedirs(MODELS_DIR, exist_ok=True)


def load_price_data():
    """Load historical price data"""
    try:
        df = pd.read_csv(f'{DATASETS_DIR}/historical_prices.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except FileNotFoundError:
        logger.warning("Historical prices not found, generating sample data")
        return generate_sample_price_data()


def generate_sample_price_data():
    """Generate sample price data for testing"""
    dates = pd.date_range(start='2024-01-01', end='2024-10-25', freq='H')
    energy_types = ['solar', 'wind', 'hydro', 'biomass']
    
    data = []
    for date in dates:
        for energy_type in energy_types:
            base_price = {'solar': 0.12, 'wind': 0.10, 'hydro': 0.08, 'biomass': 0.15}[energy_type]
            noise = np.random.normal(0, 0.02)
            trend = 0.00001 * (date - dates).total_seconds() / 3600
            
            data.append({
                'timestamp': date,
                'energy_type': energy_type,
                'price': base_price + noise + trend,
                'volume': np.random.uniform(50, 150)
            })
    
    return pd.DataFrame(data)


def create_sequences(data, sequence_length=24):
    """Create sequences for LSTM"""
    X, y = [], []
    
    for i in range(len(data) - sequence_length):
        X.append(data[i:i + sequence_length])
        y.append(data[i + sequence_length])
    
    return np.array(X), np.array(y)


def train_price_predictor(epochs=100, batch_size=32, validation_split=0.2):
    """
    Train LSTM price predictor
    """
    logger.info("Training Price Predictor (LSTM)...")
    
    # Load data
    df = load_price_data()
    
    # Process each energy type separately
    models = {}
    
    for energy_type in ['solar', 'wind', 'hydro', 'biomass']:
        logger.info(f"Training model for {energy_type}")
        
        # Filter data
        type_data = df[df['energy_type'] == energy_type].sort_values('timestamp')
        prices = type_data['price'].values
        
        # Normalize
        scaler = StandardScaler()
        prices_scaled = scaler.fit_transform(prices.reshape(-1, 1)).flatten()
        
        # Create sequences
        sequence_length = 24
        X, y = create_sequences(prices_scaled, sequence_length)
        
        # Split data
        split = int(len(X) * (1 - validation_split))
        X_train, X_val = X[:split], X[split:]
        y_train, y_val = y[:split], y[split:]
        
        # Reshape for LSTM [samples, timesteps, features]
        X_train = X_train.reshape(X_train.shape, X_train.shape, 1)
        X_val = X_val.reshape(X_val.shape, X_val.shape, 1)
        
        # Build model
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(sequence_length, 1)),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
        
        # Train
        history = model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(X_val, y_val),
            verbose=0
        )
        
        # Evaluate
        val_predictions = model.predict(X_val)
        val_mae = mean_absolute_error(y_val, val_predictions)
        val_rmse = np.sqrt(mean_squared_error(y_val, val_predictions))
        
        logger.info(f"{energy_type} - Validation MAE: {val_mae:.4f}, RMSE: {val_rmse:.4f}")
        
        # Save model
        models[energy_type] = {
            'model': model,
            'scaler': scaler,
            'sequence_length': sequence_length
        }
    
    # Save all models
    model_path = f'{MODELS_DIR}/price_predictor_v1.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(models, f)
    
    logger.info(f"Price predictor saved to {model_path}")
    
    return models


def train_demand_forecaster():
    """
    Train Random Forest demand forecaster
    """
    logger.info("Training Demand Forecaster (Random Forest)...")
    
    # Generate sample demand data
    dates = pd.date_range(start='2024-01-01', end='2024-10-25', freq='H')
    energy_types = ['solar', 'wind', 'hydro', 'biomass']
    
    data = []
    for date in dates:
        for energy_type in energy_types:
            base_demand = {'solar': 1000, 'wind': 800, 'hydro': 1200, 'biomass': 600}[energy_type]
            
            # Add time-based patterns
            hour_factor = 1.3 if 9 <= date.hour <= 21 else 0.7
            weekday_factor = 1.2 if date.weekday() < 5 else 0.9
            
            demand = base_demand * hour_factor * weekday_factor + np.random.normal(0, 100)
            
            data.append({
                'energy_type': energy_type,
                'hour': date.hour,
                'day_of_week': date.dayofweek,
                'month': date.month,
                'demand': max(0, demand)
            })
    
    df = pd.DataFrame(data)
    
    # Train models for each energy type
    models = {}
    
    for energy_type in energy_types:
        logger.info(f"Training forecaster for {energy_type}")
        
        type_data = df[df['energy_type'] == energy_type].copy()
        
        # Features and target
        X = type_data[['hour', 'day_of_week', 'month']]
        y = type_data['demand']
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        val_predictions = model.predict(X_val)
        mae = mean_absolute_error(y_val, val_predictions)
        r2 = r2_score(y_val, val_predictions)
        
        logger.info(f"{energy_type} - MAE: {mae:.2f}, R²: {r2:.4f}")
        
        models[energy_type] = model
    
    # Save models
    model_path = f'{MODELS_DIR}/demand_forecaster_v1.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(models, f)
    
    logger.info(f"Demand forecaster saved to {model_path}")
    
    return models


def train_trend_analyzer():
    """
    Train XGBoost trend analyzer
    """
    logger.info("Training Trend Analyzer (XGBoost)...")
    
    # Generate sample trend data
    n_samples = 5000
    
    data = []
    for _ in range(n_samples):
        momentum = np.random.uniform(0, 1)
        sentiment = np.random.uniform(0, 1)
        volume = np.random.uniform(0, 1)
        price_change = np.random.uniform(-0.1, 0.1)
        
        # Determine trend
        if momentum > 0.6 and sentiment > 0.6:
            trend = 'bullish'
        elif momentum < 0.4 and sentiment < 0.4:
            trend = 'bearish'
        else:
            trend = 'neutral'
        
        data.append({
            'momentum': momentum,
            'sentiment': sentiment,
            'volume': volume,
            'price_change': price_change,
            'trend': trend
        })
    
    df = pd.DataFrame(data)
    
    # Encode labels
    label_map = {'bullish': 2, 'neutral': 1, 'bearish': 0}
    df['trend_encoded'] = df['trend'].map(label_map)
    
    # Features and target
    X = df[['momentum', 'sentiment', 'volume', 'price_change']]
    y = df['trend_encoded']
    
    # Split data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = xgb.XGBClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    val_predictions = model.predict(X_val)
    accuracy = (val_predictions == y_val).mean()
    
    logger.info(f"Validation Accuracy: {accuracy:.4f}")
    
    # Save model
    model_data = {
        'model': model,
        'label_map': label_map,
        'reverse_map': {v: k for k, v in label_map.items()}
    }
    
    model_path = f'{MODELS_DIR}/trend_analyzer_v1.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)
    
    logger.info(f"Trend analyzer saved to {model_path}")
    
    return model


def main():
    """Main training function"""
    parser = argparse.ArgumentParser(description='Train AI models')
    parser.add_argument('--model', type=str, choices=['price_predictor', 'demand_forecaster', 'trend_analyzer', 'all'],
                       default='all', help='Model to train')
    parser.add_argument('--epochs', type=int, default=100, help='Training epochs for LSTM')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size for LSTM')
    
    args = parser.parse_args()
    
    logger.info("Starting model training...")
    
    if args.model in ['price_predictor', 'all']:
        train_price_predictor(epochs=args.epochs, batch_size=args.batch_size)
    
    if args.model in ['demand_forecaster', 'all']:
        train_demand_forecaster()
    
    if args.model in ['trend_analyzer', 'all']:
        train_trend_analyzer()
    
    logger.info("Training complete!")


if __name__ == '__main__':
    main()
