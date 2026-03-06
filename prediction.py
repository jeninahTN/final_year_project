import torch
import torch.nn as nn
import numpy as np
import os
from pathlib import Path

# Define the LSTM Model class (must match training)
class LSTMModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim=1, num_layers=2):
        super(LSTMModel, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        # LSTM layer
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        
        # Fully connected layer
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # x shape: (batch_size, seq_length, input_dim)
        # Here we are feeding 1 timestep with all features
        x = x.unsqueeze(1) 
        
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
        
        out, _ = self.lstm(x, (h0, c0))
        
        # Decode the hidden state of the last time step
        out = self.fc(out[:, -1, :])
        return out

class PredictionService:
    def __init__(self):
        self.model = None
        self.model_path = Path(__file__).resolve().parent.parent / "models" / "lstm_model.pth"
        self.input_dim = 11 # Based on features used in training: temperature_2m, precipitation, humidity_2m, sentiment_score, price_lag_1...7
        self.hidden_dim = 64
        self._load_model()

    def _load_model(self):
        if not self.model_path.exists():
            print(f"Warning: Model file not found at {self.model_path}")
            return

        try:
            self.model = LSTMModel(self.input_dim, self.hidden_dim)
            self.model.load_state_dict(torch.load(self.model_path))
            self.model.eval()
            print("LSTM model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")

    def predict(self, features):
        """
        Predicts crop price based on input features.
        Features should be a list or numpy array of length 11.
        """
        if self.model is None:
            return None

        try:
            input_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0) # Add batch dimension
            with torch.no_grad():
                prediction = self.model(input_tensor)
            return prediction.item()
        except Exception as e:
            print(f"Prediction error: {e}")
            return None

# Singleton instance
prediction_service = PredictionService()
