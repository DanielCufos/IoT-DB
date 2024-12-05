from flask import Flask, request
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "sensor_datos.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperatura REAL,
            humedad REAL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/guardar_datos', methods=['GET'])
def guardar_datos():
    try:
        temperatura = request.args.get('temperatura')
        humedad = request.args.get('humedad')
        
        if not temperatura or not humedad:
            return "Faltan datos", 400

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO datos (temperatura, humedad) VALUES (?, ?)", (float(temperatura), float(humedad)))
        conn.commit()
        conn.close()

        return "Datos guardados correctamente", 200
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
