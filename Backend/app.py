from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# Load the trained model
model = joblib.load("model/phishing_model.pkl")

# Optional: define the feature extraction logic
def extract_features(url: str) -> pd.DataFrame:
    """Extract simple features from the input URL for prediction."""
    return pd.DataFrame([{
        "url_length": len(url),
        "has_https": int("https" in url),
        "has_ip": int(bool(re.match(r'^http[s]?://(?:[0-9]{1,3}\.){3}[0-9]{1,3}', url))),
        "num_dots": url.count("."),
        "has_at": int("@" in url),
        "has_hyphen": int("-" in url),
        "has_suspicious_words": int(any(word in url.lower() for word in ["login", "verify", "bank", "secure"]))
    }])

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "PhishGuard Flask API is running."})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if "url" not in data:
        return jsonify({"error": "No URL provided"}), 400

    url = data["url"]

    try:
        features = extract_features(url)
        prediction = model.predict(features)[0]
        result = "phishing" if prediction == 1 else "legitimate"
        return jsonify({"url": url, "prediction": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
