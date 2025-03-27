from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yfinance as yf
import pandas as pd
from prophet import Prophet
import json
import matplotlib.pyplot as plt

app = FastAPI()

class ForecastRequest(BaseModel):
    symbol: str
    periods: int = 30  # Default: 30-day forecast

def fetch_yfinance_data(symbol):
    """Fetch historical stock data from Yahoo Finance."""
    df = yf.download(symbol, period="1y", interval="1d")
    if df.empty:
        return None
    df = df.reset_index()[["Date", "Close"]]
    df.columns = ["ds", "y"]
    return df

def train_prophet(df):
    """Train Prophet model for forecasting."""
    model = Prophet()
    model.fit(df)
    return model

def forecast_future(model, periods):
    """Generate forecast for given periods."""
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]

def plot_forecast(df, forecast, symbol):
    """Plot actual vs forecasted stock prices."""
    plt.figure(figsize=(10, 5))
    plt.plot(df["ds"], df["y"], label="Actual Prices", color="blue")
    plt.plot(forecast["ds"], forecast["yhat"], label="Forecast", color="red")
    plt.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"], color="pink", alpha=0.3)
    plt.title(f"{symbol} Stock Price Forecast")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.show()

@app.post("/forecast/")
def get_forecast(request: ForecastRequest):
    """Fetch stock data, generate forecast, and display the result."""
    df = fetch_yfinance_data(request.symbol)
    if df is None:
        raise HTTPException(status_code=400, detail="Invalid stock symbol or data unavailable")

    model = train_prophet(df)
    forecast = forecast_future(model, request.periods)

    # Display the forecasted plot
    plot_forecast(df, forecast, request.symbol)

    # Return JSON response
    result = {
        "symbol": request.symbol,
        "forecast": forecast.to_dict(orient="records"),
    }
    return result
