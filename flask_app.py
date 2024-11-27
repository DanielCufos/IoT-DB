from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

@app.route('/datos')
def obtener_datos():
    conn = sqlite3.connect('mediciones.db')
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, valor_sensor FROM mediciones')
    datos = cursor.fetchall()
    conn.close()
    return jsonify(datos)

@app.route('/')
def index():
    return render_template('grafico.html')  

if __name__ == '__main__':
    app.run(debug=True)
