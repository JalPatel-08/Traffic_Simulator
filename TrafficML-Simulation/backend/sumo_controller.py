import os
import json
import traci
import time
import paho.mqtt.client as mqtt

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
OPTIMIZED_SIGNAL_TOPIC = "Atraffic/optimized_signal"

# SUMO Configuration
SUMO_CONFIG = "simulation/my_intersection.sumocfg"
sumo_cmd = ["sumo-gui", "-c", SUMO_CONFIG]

# MQTT Callback
def on_message(client, userdata, msg):
    try:
        signal_data = json.loads(msg.payload.decode())
        junction_id = signal_data["junction_id"]
        new_duration = signal_data["optimized_duration"]

        print(f"📥 Received Optimized Signal Data: {signal_data}")

        # Check if SUMO is running and the junction exists
        if junction_id in traci.trafficlight.getIDList():
            current_phase = traci.trafficlight.getPhase(junction_id)
            traci.trafficlight.setPhaseDuration(junction_id, new_duration)
            print(f"🚦 Updated traffic light {junction_id} to {new_duration}s (Current Phase: {current_phase})")
        else:
            print(f"⚠️ Traffic light {junction_id} not found in SUMO!")

    except Exception as e:
        print(f"⚠️ Error in updating SUMO signals: {e}")


# Start SUMO First
traci.start(sumo_cmd)
print("✅ SUMO simulation started.")

# Now Start MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()
client.subscribe(OPTIMIZED_SIGNAL_TOPIC)
print("📡 Subscribed to MQTT topic:", OPTIMIZED_SIGNAL_TOPIC)

# Run SUMO Simulation Loop
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    time.sleep(0.1)  # Control loop

traci.close()
client.loop_stop()
print("✅ SUMO simulation ended.")
