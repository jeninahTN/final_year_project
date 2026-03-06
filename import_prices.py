import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Configuration
INPUT_FILE = "data/raw/crop_prices_raw.csv"
OUTPUT_FILE = "data/processed/crop_prices_clean.csv"

def generate_dummy_data():
    """Generates realistic dummy data if no input file exists."""
    print("Generating realistic dummy price data...")
    
    crops = ["Maize", "Beans", "Coffee", "Matooke", "Cassava"]
    markets = ["Owino", "Nakawa", "Kalerwe", "Masaka", "Mbale"]
    
    start_date = datetime.now() - timedelta(days=365*2) # 2 years of data
    dates = [start_date + timedelta(days=i) for i in range(365*2)]
    
    data = []
    
    for crop in crops:
        # Base price and volatility per crop
        if crop == "Maize": base, vol = 1200, 200
        elif crop == "Beans": base, vol = 3500, 500
        elif crop == "Coffee": base, vol = 8000, 1000
        elif crop == "Matooke": base, vol = 15000, 3000
        elif crop == "Cassava": base, vol = 1000, 150
        
        for market in markets:
            # Market variation
            market_factor = np.random.uniform(0.9, 1.1)
            
            # Generate price series with seasonality and trend
            t = np.arange(len(dates))
            trend = t * 0.5 # Slight inflation
            seasonality = np.sin(t / 50) * vol # Seasonal fluctuation
            noise = np.random.normal(0, vol * 0.2, len(dates))
            
            prices = base * market_factor + trend + seasonality + noise
            prices = np.maximum(prices, base * 0.5) # Prevent unrealistic lows
            
            for date, price in zip(dates, prices):
                data.append({
                    "Date": date.strftime("%Y-%m-%d"),
                    "Crop": crop,
                    "Market": market,
                    "Price": int(price),
                    "Unit": "kg" if crop != "Matooke" else "bunch"
                })
                
    df = pd.DataFrame(data)
    df.to_csv(INPUT_FILE, index=False)
    print(f"Generated {len(df)} rows of dummy data at {INPUT_FILE}")

def import_and_clean_prices():
    if not os.path.exists(INPUT_FILE):
        generate_dummy_data()

    print(f"Loading data from {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE)
        
        # Basic cleaning
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        
        df.dropna(inplace=True)
        
        if 'Price' in df.columns:
            df['Price'] = df['Price'].astype(str).str.replace(',', '').astype(float)

        # Save processed data
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Cleaned data saved to {OUTPUT_FILE}")
        print(df.head())
        print(f"Total records: {len(df)}")

    except Exception as e:
        print(f"Error processing price data: {e}")

if __name__ == "__main__":
    import_and_clean_prices()
