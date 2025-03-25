import yfinance as yf
import finnhub
import psycopg2
import schedule
import time

# List of stocks to track
symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "SPY", "QQQ", "BTC-USD", "ETH-USD"]

# Finnhub API client
finnhub_client = finnhub.Client(api_key="YOUR_FINNHUB_API_KEY")

# Database connection details (Supabase PostgreSQL)
DB_HOST = "your-supabase-host"
DB_NAME = "postgres"
DB_USER = "your-supabase-user"
DB_PASS = "your-supabase-password"

def fetch_and_store_stock_data():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            sslmode="require"
        )
        cursor = conn.cursor()

        for symbol in symbols:
            quote = finnhub_client.quote(symbol)
            stock = yf.Ticker(symbol)
            
            try:
                volume = int(stock.history(period="1d")["Volume"].iloc[-1])
            except:
                volume = 0  # If volume data is unavailable

            cursor.execute("""
                INSERT INTO real_time_stocks (symbol, open, high, low, current_price, previous_close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                symbol,
                quote.get("o", 0),
                quote.get("h", 0),
                quote.get("l", 0),
                quote.get("c", 0),
                quote.get("pc", 0),
                volume
            ))

            print(f"✅ Data updated for {symbol} at {time.strftime('%H:%M:%S')}")

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"⚠️ Error: {e}")

# Schedule job every 5 minutes
schedule.every(5).minutes.do(fetch_and_store_stock_data)

# Keep running the script
while True:
    schedule.run_pending()
    time.sleep(1)




