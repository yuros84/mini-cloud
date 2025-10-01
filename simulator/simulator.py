import requests
import time
import random
import os

API_URL = os.getenv("API_URL", "http://api:5000/data")

while True:
    value = round(random.uniform(20, 30), 2)  # Simula °C
    try:
        r = requests.post(API_URL, json={"value": value})
        print(f"Sent value {value}, response: {r.json()}")
    except Exception as e:
        print(f"Error sending data: {e}")
    time.sleep(5)
