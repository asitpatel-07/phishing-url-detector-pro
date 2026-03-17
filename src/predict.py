import joblib
import pandas as pd

from config import MODEL_PATH, FEATURE_COLUMNS_PATH
from src.feature_extractor import extract_url_features


def load_artifacts():
    model = joblib.load(MODEL_PATH)
    feature_columns = joblib.load(FEATURE_COLUMNS_PATH)
    return model, feature_columns


def build_reasons(features):
    reasons = []

    if features["has_ip_address"]:
        reasons.append("URL uses IP address instead of a normal domain")
    if features["has_suspicious_word"]:
        reasons.append("Suspicious words found in URL")
    if features["is_shortened"]:
        reasons.append("Shortened URL detected")
    if features["subdomain_count"] >= 2:
        reasons.append("Too many subdomains present")
    if features["is_long_url"]:
        reasons.append("URL is unusually long")
    if features["is_very_long_url"]:
        reasons.append("URL is extremely long")
    if features["at_count"] > 0:
        reasons.append("Contains @ symbol")
    if features["has_multiple_hyphens"]:
        reasons.append("Contains many hyphens")
    if features["has_https"] == 0:
        reasons.append("HTTPS not used")
    if features["has_brand_misuse"]:
        reasons.append("Trusted brand name looks misused in URL")
    if features["digit_ratio"] > 0.2:
        reasons.append("Too many digits in URL")
    if features["special_char_ratio"] > 0.3:
        reasons.append("Too many special characters")

    return reasons


def get_risk_score(phishing_prob):
    return int(round(phishing_prob * 100))


def predict_url(url: str):
    model, feature_columns = load_artifacts()

    features = extract_url_features(url)
    X = pd.DataFrame([features])

    for col in feature_columns:
        if col not in X.columns:
            X[col] = 0

    X = X[feature_columns]

    prediction = int(model.predict(X)[0])
    probabilities = model.predict_proba(X)[0]

    phishing_prob = float(probabilities[1])
    legitimate_prob = float(probabilities[0])

    risk_score = get_risk_score(phishing_prob)
    reasons = build_reasons(features)

    if risk_score >= 80:
        severity = "High Risk"
    elif risk_score >= 50:
        severity = "Medium Risk"
    elif risk_score >= 25:
        severity = "Low Risk"
    else:
        severity = "Very Low Risk"

    return {
        "prediction": prediction,
        "prediction_label": "Phishing" if prediction == 1 else "Legitimate",
        "phishing_probability": phishing_prob,
        "legitimate_probability": legitimate_prob,
        "risk_score": risk_score,
        "severity": severity,
        "reasons": reasons,
        "features": features
    }


if __name__ == "__main__":
    user_url = input("Enter URL to predict: ").strip()
    result = predict_url(user_url)
    print(result)