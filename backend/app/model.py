import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_training_data(n_samples=1000):
    """
    Generate synthetic training data for CPU usage prediction.
    In a real scenario, this would be replaced with actual historical data.
    """
    np.random.seed(42)
    
    # Generate timestamps
    base_time = datetime.now() - timedelta(days=n_samples)
    timestamps = [base_time + timedelta(minutes=i) for i in range(n_samples)]
    
    # Generate CPU usage with some patterns
    # Base pattern: daily cycle + random noise
    hours = np.array([t.hour + t.minute/60 for t in timestamps])
    daily_pattern = 50 + 30 * np.sin(2 * np.pi * hours / 24)  # Daily cycle
    noise = np.random.normal(0, 5, n_samples)  # Random noise
    cpu_usage = np.clip(daily_pattern + noise, 0, 100)  # Clip to 0-100 range
    
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'cpu_usage': cpu_usage
    })
    
    return df

def prepare_features(df, lookback=5):
    """
    Prepare features for time series prediction.
    Uses previous 'lookback' values to predict the next value.
    """
    # Create lag features
    for i in range(1, lookback + 1):
        df[f'cpu_usage_lag_{i}'] = df['cpu_usage'].shift(i)
    
    # Add time-based features
    df['hour'] = df['timestamp'].dt.hour
    df['minute'] = df['timestamp'].dt.minute
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    
    # Drop rows with NaN values (due to lag features)
    df = df.dropna()
    
    # Prepare X and y
    feature_cols = [f'cpu_usage_lag_{i}' for i in range(1, lookback + 1)] + ['hour', 'minute', 'day_of_week']
    X = df[feature_cols]
    y = df['cpu_usage']
    
    return X, y

def train_model():
    """
    Train a linear regression model for CPU usage prediction.
    Returns the trained model and scaler.
    """
    logger.info("Generating training data...")
    df = generate_training_data()
    
    logger.info("Preparing features...")
    X, y = prepare_features(df)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train model
    logger.info("Training model...")
    model = LinearRegression()
    model.fit(X_scaled, y)
    
    # Save model and scaler
    model_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, 'cpu_predictor.joblib')
    scaler_path = os.path.join(model_dir, 'scaler.joblib')
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    logger.info(f"Model saved to {model_path}")
    logger.info(f"Scaler saved to {scaler_path}")
    
    # Evaluate model
    score = model.score(X_scaled, y)
    logger.info(f"Model R² score: {score:.3f}")
    
    return model, scaler

def load_model():
    """
    Load the trained model and scaler.
    """
    model_dir = os.path.join(os.path.dirname(__file__), 'models')
    model_path = os.path.join(model_dir, 'cpu_predictor.joblib')
    scaler_path = os.path.join(model_dir, 'scaler.joblib')
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        logger.info("Model not found. Training new model...")
        return train_model()
    
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    
    return model, scaler

if __name__ == "__main__":
    train_model() 