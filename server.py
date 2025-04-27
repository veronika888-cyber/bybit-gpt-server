import requests
from flask import Flask, jsonify
import os

app = Flask(__name__)

# API-ключі беремо із середовища для безпеки
BYBIT_API_KEY = os.getenv('BYBIT_API_KEY')
BYBIT_API_SECRET = os.getenv('BYBIT_API_SECRET')

@app.route('/wallet-balance', methods=['GET'])
def get_wallet_balance():
    if not BYBIT_API_KEY:
        return jsonify({'error': 'API ключ не заданий'}), 400

    url = "https://api.bybit.com/v5/account/wallet-balance?accountType=UNIFIED"
    headers = {
        'X-BYBIT-API-KEY': BYBIT_API_KEY,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        try:
            balance = data['result']['list'][0]['totalEquity']
        except (KeyError, IndexError):
            return jsonify({'error': 'Помилка в структурі відповіді'}), 500

        return jsonify({'balance': balance})
    else:
        return jsonify({'error': f'Помилка запиту до Bybit: {response.text}'}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
