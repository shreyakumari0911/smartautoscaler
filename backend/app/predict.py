import numpy as np
import pandas as pd
from datetime import datetime
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

def prepare_prediction_input(current_cpu: float, lookback: int = 5) -> np.ndarray:
    """
    Prepare input features for prediction using current CPU usage.
    In a real scenario, we would use actual historical data.
    """
    # Create a simple feature vector with current CPU and time features
    now = datetime.now()
    
    # For demo purposes, we'll use the current CPU value for all lag features
    # In production, you would use actual historical values
    features = np.array([current_cpu] * lookback)  # Lag features
    
    # Add time features
    features = np.append(features, [
        now.hour,
        now.minute,
        now.weekday()
    ])
    
    return features.reshape(1, -1)

def make_prediction(model_and_scaler: Tuple, current_cpu: float) -> float:
    """
    Make a prediction for the next CPU usage value.
    
    Args:
        model_and_scaler: Tuple of (model, scaler)
        current_cpu: Current CPU usage percentage
    
    Returns:
        Predicted CPU usage percentage
    """
    try:
        model, scaler = model_and_scaler
        
        # Prepare input features
        X = prepare_prediction_input(current_cpu)
        
        # Scale features
        X_scaled = scaler.transform(X)
        
        # Make prediction
        prediction = model.predict(X_scaled)[0]
        
        # Ensure prediction is within valid range
        prediction = np.clip(prediction, 0, 100)
        
        logger.info(f"Made prediction: {prediction:.2f}% (current: {current_cpu:.2f}%)")
        return prediction
        
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        # Return current CPU as fallback
        return current_cpu

def load_model():
    """
    Load the trained model and scaler.
    This is a wrapper around model.load_model() to maintain separation of concerns.
    """
    from .model import load_model as load_ml_model
    return load_ml_model() 