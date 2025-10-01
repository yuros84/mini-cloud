from flask import Flask, request, jsonify
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "sensors")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route("/data", methods=["POST"])
def insert_data():
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON payload"}), 400

    # Validación FIWARE NGSI-v2 básica
    entity_id = data.get("id")
    entity_type = data.get("type")
    temperature_attr = data.get("temperature", {})
    location_attr = data.get("location", {})

    if not all([entity_id, entity_type, temperature_attr.get("value")]):
        return jsonify({"error": "Invalid FIWARE entity format"}), 400

    temperature = temperature_attr["value"]
    location = location_attr.get("value", "unknown")
    timestamp = data.get("timestamp", {}).get("value", datetime.utcnow().isoformat())

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO readings (entity_id, entity_type, temperature, location, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (entity_id, entity_type, temperature, location, timestamp))
        conn.commit()
        cur.close()
        conn.close()

        print(f"✅ Stored: {entity_id} {temperature}°C @ {timestamp}")
        return jsonify({
            "status": "ok",
            "entity_id": entity_id,
            "temperature": temperature,
            "timestamp": timestamp
        })
    except Exception as e:
        print(f"❌ Database error: {e}")
        return jsonify({"error": "Database insertion failed"}), 500

@app.route("/data", methods=["GET"])
def get_data():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT entity_id, entity_type, temperature, location, created_at
            FROM readings
            ORDER BY created_at DESC
            LIMIT 10;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        return jsonify([
            {
                "id": r[0],
                "type": r[1],
                "temperature": {"value": r[2], "type": "Float"},
                "location": {"value": r[3], "type": "Text"},
                "created_at": r[4].isoformat() if hasattr(r[4], 'isoformat') else r[4]
            } for r in rows
        ])
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return jsonify({"error": "Failed to fetch data"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
