import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from train_lstm import CropDataset, LSTMModel, INPUT_FILE, MODEL_FILE, BATCH_SIZE, SEQ_LENGTH

# Configuration
PLOT_FILE = "models/lstm_evaluation_plot.png"

def evaluate_lstm():
    print("Evaluating LSTM model...")
    
    # 1. Load Data
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return
        
    df = pd.read_csv(INPUT_FILE)
    
    # 2. Prepare Features and Target (Same as training)
    features = [col for col in df.columns if col not in ['Date', 'Crop', 'Market', 'Price', 'Unit']]
    target = 'Price'
    
    X = df[features].values
    y = df[target].values
    
    # 3. Split Data (Same seed to ensure same test set)
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
    
    test_dataset = CropDataset(X_test, y_test)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    # 4. Load Model
    input_dim = X.shape[1]
    hidden_dim = 64
    model = LSTMModel(input_dim, hidden_dim)
    
    if not os.path.exists(MODEL_FILE):
        print(f"Error: {MODEL_FILE} not found. Please train the model first.")
        return
        
    model.load_state_dict(torch.load(MODEL_FILE))
    model.eval()
    
    # 5. Make Predictions
    predictions = []
    actuals = []
    
    with torch.no_grad():
        for X_batch, y_batch in test_loader:
            outputs = model(X_batch)
            predictions.extend(outputs.numpy().flatten())
            actuals.extend(y_batch.numpy().flatten())
            
    predictions = np.array(predictions)
    actuals = np.array(actuals)
    
    # 6. Calculate Metrics
    mae = mean_absolute_error(actuals, predictions)
    rmse = np.sqrt(mean_squared_error(actuals, predictions))
    
    print(f"Mean Absolute Error (MAE): {mae:.5f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.5f}")
    
    # 7. Visualize
    plt.figure(figsize=(12, 6))
    plt.plot(actuals, label='Actual Price', alpha=0.7)
    plt.plot(predictions, label='Predicted Price', alpha=0.7)
    plt.title('LSTM Model Evaluation: Actual vs Predicted Prices')
    plt.xlabel('Sample Index')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.savefig(PLOT_FILE)
    print(f"Evaluation plot saved to {PLOT_FILE}")

if __name__ == "__main__":
    evaluate_lstm()
