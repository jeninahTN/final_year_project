import requests
import json

def test_prediction_endpoint():
    url = "http://localhost:8000/predict"
    
    # Sample features (must match input_dim=11)
    # temperature_2m, precipitation, humidity_2m, sentiment_score, price_lag_1...7
    features = [25.0, 0.0, 60.0, 0.5, 100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0]
    
    payload = {"features": features}
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print("Success! Prediction received:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: Status Code {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the app is running.")

if __name__ == "__main__":
    test_prediction_endpoint()
