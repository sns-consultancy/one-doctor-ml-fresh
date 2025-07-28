from sklearn.linear_model import LogisticRegression
import joblib
import os

# Sample training data
X = [[0, 0], [1, 1], [1, 0], [0, 1]]
y = [0, 1, 1, 0]

model = LogisticRegression()
model.fit(X, y)

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/model.pkl")
print("✅ Model saved to models/model.pkl")
