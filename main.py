from flask import Flask
import yfinance as yf
import finnhub
import mysql.connector
import schedule
import time

app = Flask(__name__)

finnhub_client = finnhub.Client(api_key="cv7isb1r01qpecig579gcv7isb1r01qpecig57a0")

def fetch_and_store_stock_data():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="#Falguniak1979",
            database="stock_data"
        )
        cursor = conn.cursor()

        symbol = "AAPL"

        quote = finnhub_client.quote(symbol)

        stock = yf.Ticker(symbol)
        volume = int(stock.history(period="1d")["Volume"].iloc[-1])

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

        conn.commit()
        conn.close()
        print(f"✅ Data updated for {symbol} at {time.strftime('%H:%M:%S')}")

    except Exception as e:
        print(f"⚠️ Error: {e}")

schedule.every(5).minutes.do(fetch_and_store_stock_data)

@app.route("/")
def home():
    return "Stock Data Fetcher is Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


