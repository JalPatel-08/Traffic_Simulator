import paho.mqtt.client as mqtt
import json
import random
import time

# MQTT Configuration
BROKER = "localhost"
TOPIC = "traffic/data"

client = mqtt.Client()
client.connect(BROKER, 1883, 60)

junctions = ["clusterJ1", "clusterJ2", "clusterJ3"]

def generate_traffic_data():
    """
    Simulates real-time traffic data.
    """
    return {
        "junction_id": random.choice(junctions),
        "vehicle_count": random.randint(5, 50),
        "current_duration": random.randint(10, 90),
        "avg_speed": round(random.uniform(10, 50), 2),
        "congestion": round(random.uniform(0.1, 1.0), 2)
    }

while True:
    data = generate_traffic_data()
    client.publish(TOPIC, json.dumps(data))
    print(f"Sent Traffic Data: {data}")
    time.sleep(5)
