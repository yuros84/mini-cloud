from flask import Flask, request, jsonify
import psycopg2
import os

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
    
    entity_id = data.get("id")
    entity_type = data.get("type")
    temperature = data.get("temperature", {}).get("value")
    location = data.get("location", {}).get("value")

    if not entity_id or not entity_type or temperature is None:
        return jsonify({"error": "Invalid FIWARE entity format"}), 400
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO readings (entity_id, entity_type, temperature, location) 
        VALUES (%s, %s, %s, %s)
    """, (entity_id, entity_type, temperature, location))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "ok", "entity_id": entity_id, "temperature": temperature})

@app.route("/data", methods=["GET"])
def get_data():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, entity_id, entity_type, temperature, location, created_at FROM readings ORDER BY created_at DESC LIMIT 10;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([
        {
            "id": r[1],
            "type": r[2],
            "temperature": {"value": r[3], "type": "Float"},
            "location": {"value": r[4], "type": "Text"},
            "created_at": r[5].isoformat()
        } for r in rows
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
