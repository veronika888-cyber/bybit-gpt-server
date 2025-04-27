# server.py
from flask import Flask, jsonify
from pybit.unified_trading import HTTP    
import os

app  = Flask(__name__)
api  = HTTP(
    testnet=False,                         
    api_key   = os.getenv("BYBIT_API_KEY"),
    api_secret= os.getenv("BYBIT_API_SECRET"),
    recv_window=5000                       
)

@app.route("/wallet-balance")
def wallet_balance():
    data = api.get_wallet_balance(accountType="UNIFIED")
    bal  = data["result"]["list"][0]["totalEquity"]
    return jsonify(balance=bal)

@app.route("/open-orders")
def open_orders():
    
    data = api.get_open_orders(category="spot")
    return jsonify(data["result"])

@app.route("/market-scan")
def market_scan():
    tickers = api.get_tickers(category="spot")["result"]["list"]
    top10   = sorted(tickers, key=lambda t: float(t["price24hPcnt"]), reverse=True)[:10]
    return jsonify(top_movers=top10)

@app.route("/volatility-scan")
def vol_scan():
    tickers = api.get_tickers(category="spot")["result"]["list"]
    vol10   = sorted(tickers, key=lambda t: abs(float(t["price24hPcnt"])), reverse=True)[:10]
    return jsonify(most_volatile=vol10)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
