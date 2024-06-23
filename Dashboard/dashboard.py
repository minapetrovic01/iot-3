import asyncio
import json
from nats.aio.client import Client as NATS
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# NATS connection details
# NATS_URL = "nats://localhost:4222"
NATS_URL = "nats://nats-server:4222"
NATS_TOPIC = "processed/data"

# InfluxDB connection details
# INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_URL = "http://influxdb:8086"
INFLUXDB_TOKEN = "mytoken"
INFLUXDB_ORG = "mina.org"
INFLUXDB_BUCKET = "sensor_data"

async def subscribe_to_nats_and_store_in_influxdb():
    try:
        # Connect to NATS
        nc = NATS()
        await nc.connect(servers=[NATS_URL])

        # Connect to InfluxDB
        client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        write_api = client.write_api(write_options=SYNCHRONOUS)

        async def message_handler(msg):
            nonlocal write_api
            payload = msg.data.decode()
            try:
                data = json.loads(payload)
                # Prepare data for InfluxDB
                point = Point("sensor_data") \
                    .tag("sensor_id", data.get("_id")) \
                    .field("avg_snoringRange", data.get("avg_snoringRange")) \
                    .field("avg_respirationRate", data.get("avg_respirationRate")) \
                    .field("avg_bodyTemperature", data.get("avg_bodyTemperature")) \
                    .field("avg_limbMovement", data.get("avg_limbMovement")) \
                    .field("avg_bloodOxygen", data.get("avg_bloodOxygen")) \
                    .field("avg_rem", data.get("avg_rem")) \
                    .field("avg_hoursSleeping", data.get("avg_hoursSleeping")) \
                    .field("avg_heartRate", data.get("avg_heartRate")) \
                    .field("avg_stresState", data.get("avg_stresState")) \
                    .time(data.get("timestamp"))

                # Write data to InfluxDB
                write_api.write(INFLUXDB_BUCKET, INFLUXDB_ORG, point)
                print(f"Stored data in InfluxDB: {data}")

            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
            except Exception as e:
                print(f"Error storing data in InfluxDB: {e}")

        # Subscribe to NATS topic
        await nc.subscribe(NATS_TOPIC, cb=message_handler)

        print(f"Subscribed to NATS topic '{NATS_TOPIC}'")

        # Keep the asyncio event loop running
        while True:
            await asyncio.sleep(1)

    except Exception as e:
        print(f"Error subscribing to NATS or storing data: {e}")

if __name__ == "__main__":
    asyncio.run(subscribe_to_nats_and_store_in_influxdb())
