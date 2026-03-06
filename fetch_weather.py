import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import os

# Configuration
NASA_POWER_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
START_DATE = (datetime.now() - timedelta(days=365*5)).strftime("%Y%m%d") # 5 years ago
END_DATE = datetime.now().strftime("%Y%m%d")
# Coordinates for Kampala, Uganda (approximate central location for now)
LAT = 0.3476
LON = 32.5825
PARAMETERS = "T2M,PRECTOTCORR,RH2M" # Temperature, Precipitation, Relative Humidity
OUTPUT_FILE = "data/raw/weather_data.csv"

def fetch_weather_data():
    print(f"Fetching weather data from {START_DATE} to {END_DATE}...")
    
    params = {
        "parameters": PARAMETERS,
        "community": "AG",
        "longitude": LON,
        "latitude": LAT,
        "start": START_DATE,
        "end": END_DATE,
        "format": "JSON"
    }
    
    try:
        response = requests.get(NASA_POWER_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Parse the nested JSON structure
        # Structure: properties -> parameter -> {date: value}
        properties = data.get("properties", {}).get("parameter", {})
        
        if not properties:
            print("No data found in response.")
            return

        # Convert to DataFrame
        dates = sorted(list(properties["T2M"].keys()))
        records = []
        
        for date_str in dates:
            record = {
                "date": date_str,
                "temperature_2m": properties["T2M"].get(date_str),
                "precipitation": properties["PRECTOTCORR"].get(date_str),
                "humidity_2m": properties["RH2M"].get(date_str)
            }
            records.append(record)
            
        df = pd.DataFrame(records)
        
        # Format date
        df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        
        # Save to CSV
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Weather data saved to {OUTPUT_FILE}")
        print(df.head())
        
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_weather_data()
