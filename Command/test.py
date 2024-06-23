import json
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
import numpy as np
from nats.aio.client import Client as NATS
import asyncio

class Pillow:
    def __init__(self, _id, snoringRange, respirationRate, bodyTemperature, limbMovement, bloodOxygen, rem, hoursSleeping, heartRate, stresState, timestamp):
        self._id = _id
        self.snoringRange = snoringRange
        self.respirationRate = respirationRate
        self.bodyTemperature = bodyTemperature
        self.limbMovement = limbMovement
        self.bloodOxygen = bloodOxygen
        self.rem = rem
        self.hoursSleeping = hoursSleeping
        self.heartRate = heartRate
        self.stresState = stresState
        
data_window = []
window_size = 10  # time window size in seconds


NATS_URL = "nats://localhost:4222"
NATS_TOPIC = "processed/data"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker with result code " + str(rc))
        client.subscribe("filtered")
        print("Subscribed to topic 'sensor/data/filtered'")
    else:
        print(f"Failed to connect to MQTT broker with result code {rc}")
    
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")
    try:
        data = json.loads(msg.payload.decode())
        pillow_data = Pillow(**data, timestamp=datetime.utcnow().isoformat())
        # process_sensor_data(pillow_data)
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print(f"Failed to deserialize message: {e}")

def process_sensor_data(sensor_data):
    global data_window
    current_time = datetime.utcnow()
    data_window.append(sensor_data)
    data_window = [data for data in data_window if data.timestamp >= current_time - timedelta(seconds=window_size)]

    if data_window:
        avg_snoringRange = np.mean([data.snoringRange for data in data_window])
        avg_respirationRate = np.mean([data.respirationRate for data in data_window])
        avg_bodyTemperature = np.mean([data.bodyTemperature for data in data_window])
        avg_limbMovement = np.mean([data.limbMovement for data in data_window])
        avg_bloodOxygen = np.mean([data.bloodOxygen for data in data_window])
        avg_rem = np.mean([data.rem for data in data_window])
        avg_hoursSleeping = np.mean([data.hoursSleeping for data in data_window])
        avg_heartRate = np.mean([data.heartRate for data in data_window])
        avg_stresState = np.mean([data.stresState for data in data_window])

        average_data = {
            'avg_snoringRange': avg_snoringRange,
            'avg_respirationRate': avg_respirationRate,
            'avg_bodyTemperature': avg_bodyTemperature,
            'avg_limbMovement': avg_limbMovement,
            'avg_bloodOxygen': avg_bloodOxygen,
            'avg_rem': avg_rem,
            'avg_hoursSleeping': avg_hoursSleeping,
            'avg_heartRate': avg_heartRate,
            'avg_stresState': avg_stresState,
            'timestamp': datetime.utcnow().isoformat()
        }

        asyncio.run(publish_average_value(average_data))

async def publish_average_value(average_data):
    try:
        nc = NATS()
        await nc.connect(servers=[NATS_URL])
        message = json.dumps(average_data)
        await nc.publish(NATS_TOPIC, message.encode('utf-8'))
        await nc.drain()
        print("Published data to NATS")
    except Exception as e:
        print(f"Failed to publish data to NATS: {e}")

def main():
    client = mqtt.Client(client_id="MqttClientApp", clean_session=True, userdata=None, protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message

    # client.connect("mosquitto", 1883, 60)
    client.connect("localhost", 1883, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()


# def on_message(client, userdata, msg):
#     print(f"Received message: {msg.payload.decode()}")
#     try:
#         data = json.loads(msg.payload.decode())
#         pillow_data = Pillow(**data)
        
#         if pillow_data.heartRate < 70:
#             alert_message = {"Alert": "Heart rate is less than 70"}
#             #client.publish("analysed/alert", json.dumps(alert_message))
#             client.publish("analysed/alert", msg.payload)
#             print("Published alert message")
#     except (json.JSONDecodeError, KeyError, TypeError) as e:
#         print(f"Failed to deserialize message: {e}")



