import os
import json
import joblib
import paho.mqtt.client as mqtt
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__) 

model_path = os.path.join("backend", "traffic_signal_model.pkl")
model = joblib.load(model_path)
print("✅ Successfully loaded ML model.")


MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TRAFFIC_TOPIC = "traffic/data"
OPTIMIZED_SIGNAL_TOPIC = "traffic/optimized_signal" 

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker!")
        client.subscribe(TRAFFIC_TOPIC)
    else:
        print(f"⚠️ MQTT Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        traffic_data = json.loads(msg.payload.decode())
        print(f"📥 Received Traffic Data: {traffic_data}")

        input_data = np.array([
            [
                traffic_data["vehicle_count"],
                traffic_data["current_duration"],
                traffic_data["avg_speed"],
                traffic_data["congestion"]
            ]
        ])

        predicted_duration = model.predict(input_data)[0]
        predicted_duration = max(10, min(90, int(predicted_duration)))  # Keep within limits

        optimized_data = {
            "junction_id": traffic_data["junction_id"],
            "optimized_duration": predicted_duration
        }

        client.publish(OPTIMIZED_SIGNAL_TOPIC, json.dumps(optimized_data))
        print(f"🚦 Sent Optimized Signal Data: {optimized_data}")

    except Exception as e:
        print(f"⚠️ Error in processing traffic data: {e}")

client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        input_data = np.array([
            [
                data["vehicle_count"],
                data["current_duration"],
                data["avg_speed"],
                data["congestion"]
            ]
        ])
        predicted_duration = model.predict(input_data)[0]
        predicted_duration = max(10, min(90, int(predicted_duration)))

        return jsonify({"optimized_duration": predicted_duration})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__": 
    app.run(debug=True)
