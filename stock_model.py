import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def predict_stock_price(symbol):
    # Get historical data
    stock = yf.Ticker(symbol)
    df = stock.history(period="1y")

    # Prepare the data
    df['Target'] = df['Close'].shift(-1)
    df['Target'] = df['Target'].fillna(method='ffill')

    # Create features
    df['SMA_5'] = df['Close'].rolling(window=5).mean()
    df['SMA_20'] = df['Close'].rolling(window=20).mean()

    # Drop NaN values
    df = df.dropna()

    # Prepare features and target
    X = df[['Close', 'SMA_5', 'SMA_20']]
    y = df['Target']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make prediction for next day
    last_data = X.iloc[-1].values.reshape(1, -1)
    prediction = model.predict(last_data)[0]
    return round(prediction, 2)
