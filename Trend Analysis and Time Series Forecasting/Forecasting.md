# FastAPI Stock Forecast API

## Setup & Run

### Install Dependencies
Ensure you have Python installed, then run:
```sh
pip install fastapi uvicorn yfinance prophet matplotlib
```

### Start the Server
Run the following command to start the FastAPI server:
```sh
uvicorn main:app --reload
```
This will start the server at `http://127.0.0.1:8000/`.

## Using Postman

### Sending a Forecast Request
- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/forecast/`
- **Headers:** `Content-Type: application/json`
- **Body (JSON):**
```json
{
    "symbol": "AAPL",
    "periods": 30
}
```

### Expected Response
The API returns a JSON response with forecasted stock prices, including estimated values and confidence intervals.

Example Response:
```json
{
    "symbol": "AAPL",
    "forecast": [
        {"ds": "2025-04-01", "yhat": 170.5, "yhat_lower": 165.2, "yhat_upper": 175.8},
        {"ds": "2025-04-02", "yhat": 171.2, "yhat_lower": 166.0, "yhat_upper": 176.5}
    ]
}
```

