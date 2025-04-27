import requests
from flask import Flask, jsonify
import os

app = Flask(__name__)

BYBIT_API_KEY = os.getenv('BYBIT_API_KEY')
BYBIT_API_SECRET = os.getenv('BYBIT_API_SECRET')
BASE_URL = "https://api.bybit.com"

HEADERS = {
    'X-BYBIT-API-KEY': BYBIT_API_KEY,
}

@app.route('/wallet-balance', methods=['GET'])
def get_wallet_balance():
    url = f"{BASE_URL}/v5/account/wallet-balance?accountType=UNIFIED"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        balance = data['result']['list'][0]['totalEquity']
        return jsonify({'balance': balance})
    else:
        return jsonify({'error': response.text}), response.status_code

@app.route('/open-orders', methods=['GET'])
def get_open_orders():
    url = f"{BASE_URL}/v5/order/realtime"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return jsonify(data['result'])
    else:
        return jsonify({'error': response.text}), response.status_code

@app.route('/market-scan', methods=['GET'])
def market_scan():
    url = f"{BASE_URL}/v5/market/tickers?category=spot"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tickers = data['result']['list']
        top_movers = sorted(tickers, key=lambda x: float(x['price24hPcnt']), reverse=True)[:10]
        return jsonify({'top_movers': top_movers})
    else:
        return jsonify({'error': response.text}), response.status_code

@app.route('/volatility-scan', methods=['GET'])
def volatility_scan():
    url = f"{BASE_URL}/v5/market/tickers?category=spot"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tickers = data['result']['list']
        volatile = sorted(tickers, key=lambda x: abs(float(x['price24hPcnt'])), reverse=True)[:10]
        return jsonify({'most_volatile': volatile})
    else:
        return jsonify({'error': response.text}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
