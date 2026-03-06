import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
import pickle

# Configuration
PRICE_FILE = "data/processed/crop_prices_clean.csv"
WEATHER_FILE = "data/raw/weather_data.csv"
SENTIMENT_FILE = "data/raw/sentiment_data.csv"
OUTPUT_DIR = "data/processed"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "merged_data.csv")
SCALER_FILE = os.path.join(OUTPUT_DIR, "scaler.pkl")

def preprocess_and_merge():
    print("Starting data preprocessing and merging...")
    
    # 1. Load Data
    print("Loading datasets...")
    try:
        prices_df = pd.read_csv(PRICE_FILE)
        weather_df = pd.read_csv(WEATHER_FILE)
        sentiment_df = pd.read_csv(SENTIMENT_FILE)
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

    # 2. Process Dates
    prices_df['Date'] = pd.to_datetime(prices_df['Date'])
    weather_df['date'] = pd.to_datetime(weather_df['date'])
    sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])

    # 3. Aggregate Sentiment (Daily Score)
    # Simple sentiment scoring: +1 for positive keywords, -1 for negative (Mock logic for now)
    # In a real scenario, use VADER or TextBlob here.
    print("Processing sentiment...")
    def get_sentiment_score(text):
        text = str(text).lower()
        score = 0
        if any(w in text for w in ['rise', 'bumper', 'good', 'profit', 'subsidy']): score += 1
        if any(w in text for w in ['drop', 'drought', 'scarcity', 'loss', 'flood']): score -= 1
        return score

    sentiment_df['sentiment_score'] = sentiment_df['text'].apply(get_sentiment_score)
    daily_sentiment = sentiment_df.groupby('date')['sentiment_score'].mean().reset_index()

    # 4. Merge Data
    print("Merging datasets...")
    # Merge prices with weather
    merged_df = pd.merge(prices_df, weather_df, left_on='Date', right_on='date', how='left')
    # Merge with sentiment
    merged_df = pd.merge(merged_df, daily_sentiment, left_on='Date', right_on='date', how='left')
    
    # Fill missing values
    # Weather: forward fill then backward fill
    merged_df[['temperature_2m', 'precipitation', 'humidity_2m']] = merged_df[['temperature_2m', 'precipitation', 'humidity_2m']].ffill().bfill()
    # Sentiment: fill with 0 (neutral)
    merged_df['sentiment_score'] = merged_df['sentiment_score'].fillna(0)
    
    # Drop redundant columns
    merged_df.drop(columns=['date_x', 'date_y'], inplace=True, errors='ignore')

    # 5. Feature Engineering (Lag Features)
    print("Generating lag features...")
    # We need to sort by Crop, Market, Date to ensure lags are correct
    merged_df.sort_values(by=['Crop', 'Market', 'Date'], inplace=True)
    
    # Create lags for Price (past 7 days)
    for lag in range(1, 8):
        merged_df[f'price_lag_{lag}'] = merged_df.groupby(['Crop', 'Market'])['Price'].shift(lag)
    
    # Drop rows with NaN from shifting
    merged_df.dropna(inplace=True)

    # 6. Normalization
    print("Normalizing data...")
    scaler = MinMaxScaler()
    cols_to_scale = ['Price', 'temperature_2m', 'precipitation', 'humidity_2m', 'sentiment_score'] + [f'price_lag_{i}' for i in range(1, 8)]
    
    # Fit scaler only on training portion ideally, but for simplicity we scale all and save scaler
    merged_df[cols_to_scale] = scaler.fit_transform(merged_df[cols_to_scale])
    
    # Save Scaler
    with open(SCALER_FILE, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Scaler saved to {SCALER_FILE}")

    # Save Merged Data
    merged_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Merged and processed data saved to {OUTPUT_FILE}")
    print(merged_df.head())
    print(f"Total records: {len(merged_df)}")

if __name__ == "__main__":
    preprocess_and_merge()
