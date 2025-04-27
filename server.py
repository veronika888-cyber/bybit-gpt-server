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

@app.route('/wallet-balance', methods=['GET'])
def wallet_balance():
    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"

    param_str = f"api_key={API_KEY}&recv_window={recv_window}&timestamp={timestamp}"
    sign = hmac.new(
        bytes(API_SECRET, "utf-8"),
        bytes(param_str, "utf-8"),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "api_key": API_KEY,
        "recv_window": recv_window,
        "timestamp": timestamp,
        "sign": sign
    }

    url = f"{BASE_URL}/v5/account/wallet-balance"
    response = requests.get(url, params=params, headers=headers)

    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
