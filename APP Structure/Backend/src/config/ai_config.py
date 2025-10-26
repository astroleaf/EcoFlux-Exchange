"""
AI Configuration
AI/ML model configuration
"""

import os


class AIConfig:
    """
    AI and ML configuration
    """
    
    # Model directories
    MODELS_DIR = os.getenv('AI_MODELS_DIR', 'ai-models/trained_models')
    DATASETS_DIR = os.getenv('AI_DATASETS_DIR', 'ai-models/datasets')
    NOTEBOOKS_DIR = 'ai-models/notebooks'
    
    # Model training
    TRAINING_ENABLED = os.getenv('AI_TRAINING_ENABLED', 'True').lower() == 'true'
    TRAINING_BATCH_SIZE = 32
    TRAINING_EPOCHS = 100
    TRAINING_VALIDATION_SPLIT = 0.2
    
    # Price Predictor
    PRICE_PREDICTOR_MODEL = 'LSTM'
    PRICE_PREDICTOR_VERSION = 'v1.0'
    PRICE_PREDICTOR_FEATURES = ['price', 'volume', 'volatility', 'demand', 'supply']
    PRICE_PREDICTOR_SEQUENCE_LENGTH = 24  # hours
    PRICE_PREDICTOR_HORIZON = 24  # hours ahead
    
    # Demand Forecaster
    DEMAND_FORECASTER_MODEL = 'Random Forest'
    DEMAND_FORECASTER_VERSION = 'v1.0'
    DEMAND_FORECASTER_FEATURES = ['hour', 'day_of_week', 'month', 'weather', 'historical_demand']
    DEMAND_FORECASTER_N_ESTIMATORS = 100
    DEMAND_FORECASTER_MAX_DEPTH = 10
    
    # Trend Analyzer
    TREND_ANALYZER_MODEL = 'XGBoost'
    TREND_ANALYZER_VERSION = 'v1.0'
    TREND_ANALYZER_FEATURES = ['momentum', 'volume', 'price_change', 'market_sentiment']
    TREND_ANALYZER_LEARNING_RATE = 0.1
    TREND_ANALYZER_N_ESTIMATORS = 200
    
    # Model performance thresholds
    MIN_ACCURACY = 0.85
    MIN_PRECISION = 0.80
    MIN_RECALL = 0.75
    MIN_F1_SCORE = 0.80
    
    # Data preprocessing
    FEATURE_SCALING = 'StandardScaler'
    HANDLE_MISSING = 'interpolate'
    OUTLIER_DETECTION = True
    OUTLIER_THRESHOLD = 3.0  # standard deviations
    
    # Prediction settings
    PREDICTION_CONFIDENCE_THRESHOLD = 0.7
    PREDICTION_CACHE_TTL = 300  # 5 minutes
    
    # Auto-retraining
    AUTO_RETRAIN_ENABLED = True
    AUTO_RETRAIN_FREQUENCY_DAYS = 7
    AUTO_RETRAIN_MIN_SAMPLES = 1000
    
    @classmethod
    def get_model_path(cls, model_name: str) -> str:
        """
        Get full path to model file
        """
        return os.path.join(cls.MODELS_DIR, f"{model_name}.pkl")
    
    @classmethod
    def get_dataset_path(cls, dataset_name: str) -> str:
        """
        Get full path to dataset file
        """
        return os.path.join(cls.DATASETS_DIR, dataset_name)
    
    @classmethod
    def get_config(cls) -> dict:
        """
        Get AI configuration dictionary
        """
        return {
            'models_dir': cls.MODELS_DIR,
            'datasets_dir': cls.DATASETS_DIR,
            'training_enabled': cls.TRAINING_ENABLED,
            'price_predictor': {
                'model': cls.PRICE_PREDICTOR_MODEL,
                'version': cls.PRICE_PREDICTOR_VERSION,
                'horizon': cls.PRICE_PREDICTOR_HORIZON
            },
            'demand_forecaster': {
                'model': cls.DEMAND_FORECASTER_MODEL,
                'version': cls.DEMAND_FORECASTER_VERSION
            },
            'trend_analyzer': {
                'model': cls.TREND_ANALYZER_MODEL,
                'version': cls.TREND_ANALYZER_VERSION
            }
        }
