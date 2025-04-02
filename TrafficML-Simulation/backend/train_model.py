import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Load real traffic data
df = pd.read_csv("backend/traffic_data.csv")  # Use your real dataset

# Define features (X) and target (y)
X = df[["vehicle_count", "current_duration", "avg_speed", "congestion"]]
y = df["signal_duration"]  # Target variable

# Split into training & test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Save the trained model
model_path = "backend/traffic_signal_model.pkl"
joblib.dump(model, model_path)

print(f"✅ Model trained and saved as {model_path}")
print(f"📊 Model Evaluation - MAE: {mae:.2f}, R² Score: {r2:.2f}")
