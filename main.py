import yfinance as yf
import finnhub
import psycopg2
import psycopg2.pool
import schedule
import time
import os

# List of stocks to track
symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "SPY", "QQQ", "BTC-USD", "ETH-USD"]

# Finnhub API client
finnhub_client = finnhub.Client(api_key="cv7isb1r01qpecig579gcv7isb1r01qpecig57a0")

# Database connection details (Supabase PostgreSQL)
DB_HOST = "db.mkkwerzncbytpvneggzu.supabase.co"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = os.getenv("SUPABASE_PASS")  # Use an environment variable for security
DB_PORT = "5432"

# PostgreSQL Connection Pool
try:
    db_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=5,
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
        sslmode="require"
    )
    print("✅ Database connection pool created successfully!")
except Exception as e:
    print(f"⚠️ Error creating database connection pool: {e}")
    exit()

def fetch_and_store_stock_data():
    conn = None
    cursor = None

    try:
        conn = db_pool.getconn()  # Get connection from pool
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

    except Exception as e:
        print(f"⚠️ Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            db_pool.putconn(conn)  # Return connection to pool

# Schedule job every 5 minutes
schedule.every(5).minutes.do(fetch_and_store_stock_data)

print("🚀 Stock data fetcher is running...")

# Keep running the script
while True:
    schedule.run_pending()
    time.sleep(1)





