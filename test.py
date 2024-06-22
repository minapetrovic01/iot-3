from influxdb_client import InfluxDBClient, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB server details
url = "http://localhost:8086"
token = "mytoken"
org = "mina.org"
bucket = "sensor_data"

# Connect to InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

def check_and_set_retention_policy():
    try:
        # Check existing retention policies
        rp_service = client.retention_policies_api()
        rps = rp_service.find_retention_policies(bucket=bucket)
        
        default_rp_set = False
        for rp in rps:
            if rp.default:
                default_rp_set = True
                print(f"Default retention policy '{rp.name}' is already set for '{bucket}'")
                break
        
        # If default retention policy is not set, set it to 'autogen'
        if not default_rp_set:
            print(f"Setting 'autogen' as default retention policy for '{bucket}'")
            rp_service.create_retention_policy(bucket=bucket, body={
                "name": "autogen",
                "duration": "0d",
                "shard_group_duration": "7d",
                "replication_factor": 1,
                "default": True
            })

            print("Default retention policy set successfully.")
        else:
            print("Default retention policy is already set.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_and_set_retention_policy()
