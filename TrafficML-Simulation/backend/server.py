import paho.mqtt.client as mqtt
import json
import joblib
import numpy as np

# Load Trained ML Model
model = joblib.load("backend/traffic_signal_model.pkl")

# MQTT Configuration
BROKER = "localhost"  # Change if needed
TRAFFIC_DATA_TOPIC = "traffic/data"
SIGNAL_UPDATE_TOPIC = "traffic/signal/update"

client = mqtt.Client()

def predict_signal(data):
    """
    Predict the optimal signal duration using the ML model.
    """
    features = np.array([[data["vehicle_count"], data["current_duration"], data["avg_speed"], data["congestion"]]])
    predicted_time = model.predict(features)[0]
    return max(10, min(90, predicted_time))  # Ensuring valid duration range

def on_connect(client, userdata, flags, rc):
    print("Server connected to MQTT broker.")
    client.subscribe(TRAFFIC_DATA_TOPIC)

def on_message(client, userdata, msg):
    """
    Process incoming traffic data and send optimized signal timings.
    """
    traffic_data = json.loads(msg.payload)
    junction_id = traffic_data["junction_id"]

    new_duration = predict_signal(traffic_data)

    signal_update = {"junction_id": junction_id, "phase_duration": new_duration}
    
    client.publish(SIGNAL_UPDATE_TOPIC, json.dumps(signal_update))
    print(f"Updated Signal for {junction_id}: {new_duration} sec")

# Set up MQTT
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_forever()
