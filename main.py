from flask import Flask, jsonify
from flask_cors import CORS
import serial
import threading
import time

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Global variables for sensor data
latest_force_data = [0, 0, 0, 0, 0, 0, 0]  # 7 zeros for force sensors
latest_dht_data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # 6 floats for DHT sensors
force_serial = None
dht_serial = None
force_connected = False
dht_connected = False

def read_force_serial():
    global latest_force_data, force_serial, force_connected
    
    while True:
        try:
            if not force_serial or not force_serial.is_open:
                force_serial = serial.Serial('COM6', 115200, timeout=1)
                force_connected = True
                print("Force sensors connected on COM6")
            
            if force_serial.in_waiting > 0:
                data = force_serial.readline().decode('utf-8').strip()
                print(f"Raw force data: {data}")
                
                try:
                    # Expecting format: "0,0,0,0,0,0,0"
                    values = list(map(int, data.split(',')))
                    if len(values) == 7:
                        latest_force_data = values
                    else:
                        print(f"Expected 7 force values, got {len(values)}")
                except ValueError as e:
                    print(f"Force data parsing error: {e}")
            
        except serial.SerialException as e:
            print(f"Force serial error: {e}")
            force_connected = False
            if force_serial and force_serial.is_open:
                force_serial.close()
            time.sleep(2)

def read_dht_serial():
    global latest_dht_data, dht_serial, dht_connected
    
    while True:
        try:
            if not dht_serial or not dht_serial.is_open:
                dht_serial = serial.Serial('COM3', 115200, timeout=1)
                dht_connected = True
                print("DHT sensors connected on COM3")
            
            if dht_serial.in_waiting > 0:
                data = dht_serial.readline().decode('utf-8').strip()
                print(f"Raw DHT data: {data}")
                
                try:
                    # Expecting format: "49.80,26.80,47.90,27.20,49.30,26.80"
                    values = list(map(float, data.split(',')))
                    if len(values) == 6:
                        latest_dht_data = values
                    else:
                        print(f"Expected 6 DHT values, got {len(values)}")
                except ValueError as e:
                    print(f"DHT data parsing error: {e}")
            
        except serial.SerialException as e:
            print(f"DHT serial error: {e}")
            dht_connected = False
            if dht_serial and dht_serial.is_open:
                dht_serial.close()
            time.sleep(2)

# Start threads
force_thread = threading.Thread(target=read_force_serial, daemon=True)
dht_thread = threading.Thread(target=read_dht_serial, daemon=True)
force_thread.start()
dht_thread.start()

@app.route('/sensor-data', methods=['GET'])
def get_sensor_data():
    return jsonify({
        "force_sensors": latest_force_data,
        "dht_sensors": latest_dht_data,
        "status": {
            "force_connected": force_connected,
            "dht_connected": dht_connected,
            "timestamp": time.time()
        }
    })

if __name__ == '__main__':
    app.run(debug=True)