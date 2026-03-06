import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split

# Configuration
INPUT_FILE = "data/processed/merged_data.csv"
MODEL_FILE = "models/lstm_model.pth"
BATCH_SIZE = 64
EPOCHS = 20
LEARNING_RATE = 0.001
SEQ_LENGTH = 1 # We are using lag features, so sequence length is effectively handled by features, but for LSTM we might want a sequence of rows. 
# However, since we already engineered lag features (price_lag_1...7), we can treat this as a standard regression problem or reshape for LSTM.
# For simplicity and given the lag features, we will treat each row as a timestep with features.
# A better LSTM approach would be to take a sequence of raw features (price, weather, sentiment) over T days to predict T+1.
# But let's use the current engineered features as input for now.

class CropDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32).view(-1, 1)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

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

def train_lstm():
    print("Training LSTM model...")
    
    # 1. Load Data
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return
        
    df = pd.read_csv(INPUT_FILE)
    
    # 2. Prepare Features and Target
    features = [col for col in df.columns if col not in ['Date', 'Crop', 'Market', 'Price', 'Unit']]
    target = 'Price'
    
    print(f"Features: {features}")
    
    X = df[features].values
    y = df[target].values
    
    # 3. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
    
    train_dataset = CropDataset(X_train, y_train)
    test_dataset = CropDataset(X_test, y_test)
    
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    # 4. Initialize Model
    input_dim = X.shape[1]
    hidden_dim = 64
    model = LSTMModel(input_dim, hidden_dim)
    
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    # 5. Training Loop
    best_loss = float('inf')
    
    for epoch in range(EPOCHS):
        model.train()
        train_loss = 0
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            
        avg_train_loss = train_loss / len(train_loader)
        
        # Validation
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for X_batch, y_batch in test_loader:
                outputs = model(X_batch)
                loss = criterion(outputs, y_batch)
                val_loss += loss.item()
        
        avg_val_loss = val_loss / len(test_loader)
        
        print(f"Epoch {epoch+1}/{EPOCHS}, Train Loss: {avg_train_loss:.5f}, Val Loss: {avg_val_loss:.5f}")
        
        if avg_val_loss < best_loss:
            best_loss = avg_val_loss
            os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)
            torch.save(model.state_dict(), MODEL_FILE)
            
    print(f"Best Validation Loss: {best_loss:.5f}")
    print(f"LSTM model saved to {MODEL_FILE}")

if __name__ == "__main__":
    train_lstm()
