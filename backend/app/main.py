from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import PlainTextResponse
import psutil
import time
from datetime import datetime
import joblib
import os
from typing import Dict, List
import numpy as np

from .metrics import (
    cpu_usage_gauge,
    memory_usage_gauge,
    prediction_gauge,
    scaling_action_counter
)
from .predict import load_model, make_prediction
from .autoscaler import get_scaling_decision

app = FastAPI(
    title="Smart Cloud Autoscaler API",
    description="API for intelligent cloud resource autoscaling with ML predictions",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
model = None
last_prediction = None
last_scaling_action = None

@app.on_event("startup")
async def startup_event():
    global model
    try:
        model = load_model()
    except Exception as e:
        print(f"Warning: Could not load ML model: {e}")
        model = None

@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "Smart Cloud Autoscaler API",
        "version": "1.0.0"
    }

@app.get("/metrics")
async def metrics():
    """Expose Prometheus metrics"""
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/system/current")
async def get_current_metrics():
    """Get current system metrics"""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    # Update Prometheus metrics
    cpu_usage_gauge.labels(instance='smartscaling').set(cpu_percent)
    memory_usage_gauge.labels(instance='smartscaling').set(memory.percent)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu_usage": cpu_percent,
        "memory_usage": memory.percent,
        "memory_available": memory.available
    }

@app.get("/predict")
async def predict_load():
    """Get load prediction for next 5 minutes"""
    global model, last_prediction
    
    if model is None:
        raise HTTPException(status_code=503, detail="ML model not loaded")
    
    try:
        # Get current metrics
        current_metrics = await get_current_metrics()
        
        # Make prediction
        prediction = make_prediction(model, current_metrics["cpu_usage"])
        last_prediction = prediction
        
        # Update Prometheus metric
        prediction_gauge.labels(instance='smartscaling').set(prediction)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "current_cpu": current_metrics["cpu_usage"],
            "predicted_cpu": float(prediction),
            "prediction_horizon": "5 minutes"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    """Get current system status and last scaling action"""
    global last_prediction, last_scaling_action
    
    current_metrics = await get_current_metrics()
    
    if last_prediction is not None:
        scaling_decision = get_scaling_decision(current_metrics["cpu_usage"], last_prediction)
        last_scaling_action = scaling_decision
        scaling_action_counter.labels(action=scaling_decision, instance='smartscaling').inc()
    else:
        scaling_decision = "No prediction available"
    
    return {
        "timestamp": datetime.now().isoformat(),
        "current_metrics": current_metrics,
        "last_prediction": float(last_prediction) if last_prediction is not None else None,
        "scaling_decision": scaling_decision,
        "model_status": "loaded" if model is not None else "not loaded"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": model is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 