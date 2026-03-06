import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from app.prediction import prediction_service

def generate_price_history(start_price=1000, days=30):
    """Generates a realistic-looking price history with trend and noise."""
    dates = [datetime.now() - timedelta(days=i) for i in range(days)]
    dates.reverse()
    
    # Create a trend (sine wave + linear trend + random noise)
    x = np.linspace(0, 4 * np.pi, days)
    trend = np.linspace(0, 500, days) # General upward trend
    seasonal = 200 * np.sin(x)
    noise = np.random.normal(0, 50, days)
    
    prices = start_price + trend + seasonal + noise
    prices = np.maximum(prices, 100) # Ensure no negative prices
    
    return [{"date": d.strftime("%Y-%m-%d"), "price": int(p)} for d, p in zip(dates, prices)]

def get_monitored_crops():
    """Returns the list of crops for the dashboard."""
    return [
        {
            "name": "Matooke",
            "market": "Nakawa Market",
            "price": "15,000",
            "unit": "UGX/bunch",
            "image": "https://images.unsplash.com/photo-1603052875302-d376b7c0638a?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60",
            "id": "matooke",
            "region": "nakawa"
        },
        {
            "name": "Cassava",
            "market": "Gulu Market",
            "price": "2,500",
            "unit": "UGX/kg",
            "image": "https://images.unsplash.com/photo-1596097635121-14b63b7a0c19?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60",
            "id": "cassava",
            "region": "gulu"
        },
        {
            "name": "Coffee",
            "market": "Mbale Market",
            "price": "8,000",
            "unit": "UGX/kg",
            "image": "https://images.unsplash.com/photo-1552346988-186312d44647?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60",
            "id": "coffee",
            "region": "mbale"
        },
        {
            "name": "Maize",
            "market": "Kasese Market",
            "price": "1,200",
            "unit": "UGX/kg",
            "image": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60",
            "id": "maize",
            "region": "kasese"
        }
    ]

def get_crop_detail(crop_id, region):
    """Returns detailed data for a specific crop."""
    # Mock logic to return specific data based on ID
    base_prices = {
        "matooke": 14000,
        "cassava": 2000,
        "coffee": 7500,
        "maize": 1000
    }
    
    start_price = base_prices.get(crop_id, 1000)
    history = generate_price_history(start_price=start_price)
    
    # Prediction logic (simple mock)
    # Prediction logic (Real Model)
    current_price = history[-1]['price']
    
    # Construct features: [temp, precip, humidity, sentiment, lag_1...lag_7]
    # Using mock weather/sentiment for now, but real lags from history
    # Note: Lags should be in reverse chronological order (t-1, t-2...)
    lags = [h['price'] for h in history[-8:-1]] # Get last 7 prices before current (or including current if we predict next day)
    # Actually, to predict T+1, we need prices at T, T-1...T-6
    lags = [h['price'] for h in history[-7:]] 
    lags.reverse() # lag_1 is most recent
    
    # Ensure we have 7 lags
    if len(lags) < 7:
        lags = [current_price] * 7 # Fallback
        
    features = [25.0, 5.0, 70.0, 0.5] + lags # Mock weather/sentiment
    
    predicted_val = prediction_service.predict(features)
    
    if predicted_val:
        predicted_price = int(predicted_val)
        prediction_source = "AI Model (LSTM)"
    else:
        predicted_price = int(current_price * 1.05) # Fallback
        prediction_source = "Simple Projection"
    
    return {
        "name": crop_id.capitalize(),
        "region": region.capitalize(),
        "current_price": f"{current_price:,}",
        "predicted_price": f"{predicted_price:,}",
        "prediction_source": prediction_source,
        "unit": "UGX/kg" if crop_id != "matooke" else "UGX/bunch",
        "history": history,
        "advice": "SELL NOW",
        "advice_desc": "Prices are at a peak. Sell your produce now for the best return.",
        "weather": "Good Rains Expected",
        "weather_desc": "Good rains are coming. This may mean more crops and stable prices for farmers."
    }
