function getStockData() {
    const symbol = document.getElementById('stockSymbol').value.toUpperCase();
    const period = document.getElementById('timePeriod').value;

    if (!symbol) {
        alert('Please enter a stock symbol');
        return;
    }

    fetch('/get_stock_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ symbol: symbol, period: period })
    })
    .then(response => response.json())
    .then(data => {
        Plotly.newPlot('stockChart', JSON.parse(data));
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error fetching stock data');
    });
}
