import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime
import random

# Configuration
OUTPUT_FILE = "data/raw/sentiment_data.csv"
TARGET_URLS = [
    "https://www.monitor.co.ug/uganda/business/commodities",
    "https://www.newvision.co.ug/category/agriculture"
]

def generate_mock_sentiment():
    """Generates mock sentiment data when scraping fails."""
    print("Generating mock sentiment data (fallback)...")
    
    keywords = ["price", "crop", "maize", "beans", "coffee", "rain", "drought", "bumper harvest", "scarcity"]
    sentiments = [
        "Prices for maize are expected to rise due to scarcity.",
        "Heavy rains in the west promise a bumper harvest for coffee.",
        "Beans prices drop as supply floods the market.",
        "Farmers worried about prolonged drought affecting yields.",
        "Government announces new subsidies for fertilizer.",
        "Transport costs hike food prices in Kampala."
    ]
    
    articles = []
    for _ in range(10):
        articles.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "source": "Mock Source",
            "text": random.choice(sentiments)
        })
    return articles

def scrape_sentiment_signals():
    print("Scraping sentiment signals...")
    articles = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/'
    }

    for url in TARGET_URLS:
        print(f"Accessing {url}...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # More specific selectors could go here
                for item in soup.find_all(['h3', 'h2', 'p']): 
                    text = item.get_text().strip()
                    if len(text) > 20 and any(keyword in text.lower() for keyword in ['price', 'crop', 'maize', 'beans', 'coffee', 'rain', 'drought']):
                        articles.append({
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "source": url,
                            "text": text
                        })
            else:
                print(f"Failed to access {url}: Status {response.status_code}")
                
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    if not articles:
        print("Scraping yielded no results. Using mock data for demonstration.")
        articles = generate_mock_sentiment()

    if articles:
        df = pd.DataFrame(articles)
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        
        # Overwrite for this run to keep it clean, or append if you prefer
        df.to_csv(OUTPUT_FILE, index=False)
            
        print(f"Saved {len(articles)} articles to {OUTPUT_FILE}")
        print(df.head())

if __name__ == "__main__":
    scrape_sentiment_signals()
