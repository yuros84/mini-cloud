import requests
import time
import random
import os
import datetime

API_URL = os.getenv("API_URL", "http://api:5000/data")

SENSOR_ID = os.getenv("SENSOR_ID", "Sensor001")
LOCATION = os.getenv("SENSOR_LOCATION", "living-room")

print(f"📡 Starting simulator for {SENSOR_ID}, sending to {API_URL}")

while True:
    value = round(random.uniform(20, 30), 2)  # Simula °C
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    # Construir payload en formato FIWARE NGSI-v2
    payload = {
        "id": SENSOR_ID,
        "type": "TemperatureSensor",
        "temperature": {
            "value": value,
            "type": "Float"
        },
        "location": {
            "value": LOCATION,
            "type": "Text"
        },
        "timestamp": {
            "value": timestamp,
            "type": "DateTime"
        }
    }

    try:
        r = requests.post(API_URL, json=payload)
        print(f"✅ Sent value {value}°C at {timestamp}, response: {r.status_code} -> {r.text}")
    except Exception as e:
        print(f"❌ Error sending data: {e}")

    time.sleep(5)
