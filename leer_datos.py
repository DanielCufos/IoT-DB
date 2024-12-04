import serial
import sqlite3
import time

# Configuración del puerto serie 
SERIAL_PORT = '/dev/ttyUSB0' 
BAUD_RATE = 9600
TIMEOUT = 1 

DB_NAME = "sensor_dht11.db"

# Inicializar la base de datos SQLite
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

def save_data(temperatura, humedad):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO datos (temperatura, humedad) VALUES (?, ?)", (temperatura, humedad))
    conn.commit()
    conn.close()

# Conectar al puerto serie
def connect_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
        print(f"Conectado a {SERIAL_PORT} con {BAUD_RATE} baudrate.")
        return ser
    except serial.SerialException as e:
        print(f"Error al conectar al puerto serie: {e}")
        return None

# Función principal
def main():
    init_db()  # Inicializar la base de datos

    ser = connect_serial()
    if ser is None:
        return  

    while True:
        try:

            data = ser.readline().decode('utf-8').strip()
            if data:
                print(f"Datos recibidos: {data}")

                parts = data.split(',')
                if len(parts) == 2:
                    temperatura = float(parts[0].split(':')[1].strip())
                    humedad = float(parts[1].split(':')[1].strip())

                    
                    save_data(temperatura, humedad)
                    print(f"Datos guardados: Temperatura: {temperatura}, Humedad: {humedad}")

            time.sleep(1)  # Esperar un segundo antes de la siguiente lectura

        except KeyboardInterrupt:
            print("Interrupción del programa por el usuario.")
            break

if __name__ == '__main__':
    main()
