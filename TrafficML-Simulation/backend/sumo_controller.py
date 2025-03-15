import traci
import paho.mqtt.client as mqtt
import json
import time

# MQTT Configuration
BROKER = "localhost"  # Change if using a different broker
TOPIC = "traffic/signal/update"

# SUMO Configuration
SUMO_BINARY = "sumo-gui"  # Use "sumo" for CLI mode
SUMO_CONFIG = "simulation/my_intersection.sumocfg"

# Connect to SUMO
traci.start([SUMO_BINARY, "-c", SUMO_CONFIG])

def update_traffic_light(junction_id, phase_duration):
    """
    Update traffic light timing in SUMO using TraCI.
    """
    try:
        traci.trafficlight.setPhaseDuration(junction_id, phase_duration)
        print(f"Updated {junction_id} to {phase_duration} seconds")
    except Exception as e:
        print(f"Error updating {junction_id}: {e}")

# MQTT Callback Functions
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker.")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    """
    Process received MQTT messages and update SUMO traffic lights.
    """
    data = json.loads(msg.payload)
    junction_id = data["junction_id"]
    phase_duration = data["phase_duration"]
    update_traffic_light(junction_id, phase_duration)

# Start MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_start()

try:
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()  # Advance SUMO simulation
        time.sleep(0.5)  # Adjust for real-time sync
finally:
    traci.close()
    client.loop_stop()
