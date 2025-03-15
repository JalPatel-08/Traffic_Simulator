import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Generate synthetic data
np.random.seed(42)
data_size = 1000

df = pd.DataFrame({
    "vehicle_count": np.random.randint(5, 50, data_size),
    "current_duration": np.random.randint(10, 90, data_size),
    "avg_speed": np.random.uniform(10, 50, data_size),
    "congestion": np.random.uniform(0.1, 1.0, data_size),
    "optimal_duration": np.random.randint(10, 90, data_size)  # Target variable
})

# Split into train & test
X = df[["vehicle_count", "current_duration", "avg_speed", "congestion"]]
y = df["optimal_duration"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "backend/traffic_signal_model.pkl")
print("Model trained and saved as traffic_signal_model.pkl")
