import os
import yfinance as yf
import finnhub
import requests
import time
from datetime import datetime

# Load credentials from environment variables
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")  # Example: "https://xyzcompany.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # Service Role Key

# Table name in Supabase
TABLE_NAME = "stock_data"

# Stock symbols to track
symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "SPY", "QQQ", "BTC-USD", "ETH-USD"]

# Initialize Finnhub API client
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

def fetch_and_store_stock_data():
    try:
        for symbol in symbols:
            quote = finnhub_client.quote(symbol)
            stock = yf.Ticker(symbol)

            try:
                volume = int(stock.history(period="1d")["Volume"].iloc[-1])
            except:
                volume = 0  # If volume data is unavailable

            data = {
                "symbol": symbol,
                "date": datetime.utcnow().isoformat(),  # Current timestamp in UTC
                "open": quote.get("o", 0),
                "high": quote.get("h", 0),
                "low": quote.get("l", 0),
                "close": quote.get("c", 0),
                "volume": volume
            }

            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json"
            }

            response = requests.post(f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}", json=data, headers=headers)

            if response.status_code == 201:
                print(f"✅ Data updated for {symbol} at {data['date']}")
            else:
                print(f"⚠️ Error inserting {symbol}: {response.text}")

    except Exception as e:
        print(f"⚠️ Error: {e}")

# Run the function every 5 minutes
while True:
    fetch_and_store_stock_data()
    time.sleep(300)  # 300 seconds = 5 minutes






