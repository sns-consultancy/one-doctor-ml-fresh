import joblib
import numpy as np

model = joblib.load("models/heart_risk_model.pkl")

def predict_risk(data: dict) -> str:
    features = np.array([
        data["age"],
        data["cholesterol"],
        data["blood_pressure"],
        data["glucose"]
    ]).reshape(1, -1)
    prediction = model.predict(features)[0]
    return "High Risk" if prediction == 1 else "Low Risk"
