from flask import Flask, request, jsonify
from flask_cors import CORS
from .services.predictor import Predictor
import os

app = Flask(__name__)
CORS(app)

predictor = Predictor()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/predict', methods=['GET'])
def predict():
    symbol = request.args.get('symbol', 'BTC/USDT')
    
    try:
        prediction = predictor.predict(symbol)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({
            "prediction": "hold",
            "confidence": 0.5,
            "symbol": symbol,
            "error": str(e)
        }), 500

@app.route('/train', methods=['POST'])
def train_model():
    # Endpoint to trigger model training
    try:
        symbol = request.json.get('symbol')
        data = request.json.get('data', [])
        predictor.train(symbol, data)
        return jsonify({"status": "training_started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('DEBUG', 'false').lower() == 'true')