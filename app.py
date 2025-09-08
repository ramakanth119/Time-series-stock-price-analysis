from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd
import plotly
import json
import plotly.graph_objs as go
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    data = request.get_json()
    symbol = data['symbol']
    period = data['period']

    # Fetch stock data using yfinance
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period)

    # Create candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                         open=hist['Open'],
                                         high=hist['High'],
                                         low=hist['Low'],
                                         close=hist['Close'])])

    # Calculate moving averages
    hist['MA20'] = hist['Close'].rolling(window=20).mean()
    hist['MA50'] = hist['Close'].rolling(window=50).mean()

    # Add moving average lines
    fig.add_trace(go.Scatter(x=hist.index, y=hist['MA20'], name='20 Day MA'))
    fig.add_trace(go.Scatter(x=hist.index, y=hist['MA50'], name='50 Day MA'))

    # Update layout
    fig.update_layout(title=f'{symbol} Stock Price',
                      xaxis_title='Date',
                      yaxis_title='Price')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify(graphJSON)

if __name__ == '__main__':
    app.run(debug=True)
