import serial
import sqlite3
from datetime import datetime


puerto = serial.Serial('COM3', 9600)  


conn = sqlite3.connect('mediciones.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS mediciones (
        id_medicion INTEGER PRIMARY KEY AUTOINCREMENT,
        valor_sensor INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

try:
    while True:
      
        linea = puerto.readline().decode('utf-8').strip()
        if linea.isdigit():
            valor = int(linea)
          
            cursor.execute('INSERT INTO mediciones (valor_sensor) VALUES (?)', (valor,))
            conn.commit()
            print(f"Valor {valor} guardado en la base de datos.")
except KeyboardInterrupt:
    print("Interrumpido por el usuario.")
finally:
    conn.close()
    puerto.close()
