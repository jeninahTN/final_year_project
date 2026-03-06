import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Configuration
INPUT_FILE = "data/processed/merged_data.csv"
MODEL_FILE = "models/baseline_model.pkl"

def train_baseline():
    print("Training baseline Linear Regression model...")
    
    # 1. Load Data
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return
        
    df = pd.read_csv(INPUT_FILE)
    
    # 2. Prepare Features and Target
    # We want to predict 'Price' based on lags, weather, and sentiment
    features = [col for col in df.columns if col not in ['Date', 'Crop', 'Market', 'Price', 'Unit']]
    target = 'Price'
    
    print(f"Features: {features}")
    
    X = df[features]
    y = df[target]
    
    # 3. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
    
    # 4. Train Model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # 5. Evaluate
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mse)
    
    print(f"Model Evaluation:")
    print(f"MSE: {mse:.4f}")
    print(f"MAE: {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    
    # 6. Save Model
    os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)
    print(f"Baseline model saved to {MODEL_FILE}")

if __name__ == "__main__":
    train_baseline()
