# server.py

from flask import Flask, request, jsonify
import time
import hmac
import hashlib
import requests

app = Flask(__name__)

# Твої API ключі
API_KEY = "IM6FxtDsEq7WtrL8oq"
API_SECRET = "AqWNvLHG2OudggzvuFvyWZinxheEZozxDkKy"

BASE_URL = "https://api.bybit.com"

# Функція для підпису параметрів
def sign_request(params):
    param_str = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
    sign = hmac.new(bytes(API_SECRET, "utf-8"), bytes(param_str, "utf-8"), hashlib.sha256).hexdigest()
    return sign

@app.route('/wallet-balance', methods=['GET'])
def wallet_balance():
    timestamp = str(int(time.time() * 1000))
    params = {
        "api_key": API_KEY,
        "timestamp": timestamp,
        "recv_window": "5000"
    }
    params["sign"] = sign_request(params)
    response = requests.get(f"{BASE_URL}/v5/account/wallet-balance", params=params)
    return jsonify(response.json())

@app.route('/positions', methods=['GET'])
def get_positions():
    timestamp = str(int(time.time() * 1000))
    params = {
        "api_key": API_KEY,
        "timestamp": timestamp,
        "recv_window": "5000"
    }
    params["sign"] = sign_request(params)
    response = requests.get(f"{BASE_URL}/v5/position/list", params=params)
    return jsonify(response.json())

@app.route('/open-orders', methods=['GET'])
def get_open_orders():
    timestamp = str(int(time.time() * 1000))
    params = {
        "api_key": API_KEY,
        "timestamp": timestamp,
        "recv_window": "5000"
    }
    params["sign"] = sign_request(params)
    response = requests.get(f"{BASE_URL}/v5/order/realtime", params=params)
    return jsonify(response.json())

@app.route('/market-ticker', methods=['GET'])
def get_market_ticker():
    response = requests.get(f"{BASE_URL}/v5/market/tickers?category=spot")
    return jsonify(response.json())

@app.route('/top-volatility', methods=['GET'])
def get_top_volatility():
    market_data = requests.get(f"{BASE_URL}/v5/market/tickers?category=spot").json()
    tickers = market_data.get("result", {}).get("list", [])
    sorted_tickers = sorted(tickers, key=lambda x: abs(float(x.get("price24hPcnt", 0))), reverse=True)
    return jsonify(sorted_tickers[:5])

@app.route('/top-volume', methods=['GET'])
def get_top_volume():
    market_data = requests.get(f"{BASE_URL}/v5/market/tickers?category=spot").json()
    tickers = market_data.get("result", {}).get("list", [])
    sorted_tickers = sorted(tickers, key=lambda x: float(x.get("turnover24h", 0)), reverse=True)
    return jsonify(sorted_tickers[:5])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
