import serial
import threading

def read_force_sensors():
    try:
        ser_force = serial.Serial('COM4', 115200, timeout=1)  # Adjust 'COM4' as needed
        print(f"Connected to ESP32 (Force Sensors) on {ser_force.port}")
        
        while True:
            if ser_force.in_waiting > 0:
                data = ser_force.readline().decode('utf-8').strip()
                print(f"Raw Force Sensor Data: {data}")  # Debug log
                try:
                    # Assuming the data is a comma-separated string of 7 values
                    sensor_values = [float(value) for value in data.split(',')]
                    if len(sensor_values) == 7:
                        print(f"Force Sensor Readings: {sensor_values}")
                    else:
                        print(f"Unexpected data format (Force Sensors): {data}")
                except ValueError:
                    print(f"Error parsing data (Force Sensors): {data}")
    except serial.SerialException as e:
        print(f"Serial error (Force Sensors): {e}")
    except KeyboardInterrupt:
        print("Exiting Force Sensors thread.")
    finally:
        if 'ser_force' in locals() and ser_force.is_open:
            ser_force.close()
            print("Force Sensors serial connection closed.")

def read_dht22_sensors():
    try:
        ser_dht = serial.Serial('COM5', 115200, timeout=1)  # Adjust 'COM5' as needed
        print(f"Connected to ESP32 (DHT22 Sensors) on {ser_dht.port}")
        
        while True:
            if ser_dht.in_waiting > 0:
                data = ser_dht.readline().decode('utf-8').strip()
                print(f"Raw DHT22 Sensor Data: {data}")  # Debug log
                try:
                    # Assuming the data is a comma-separated string of 3 values
                    sensor_values = [float(value) for value in data.split(',')]
                    if len(sensor_values) == 3:
                        # Validate the range of sensor values
                        if all(0 <= value <= 100 for value in sensor_values):
                            print(f"Valid DHT22 Sensor Readings: {sensor_values}")
                        else:
                            print(f"Invalid DHT22 value range: {sensor_values}")
                    else:
                        print(f"Unexpected data format (DHT22 Sensors): {data}")
                except ValueError:
                    print(f"Error parsing data (DHT22 Sensors): {data}")
    except serial.SerialException as e:
        print(f"Serial error (DHT22 Sensors): {e}")
    except KeyboardInterrupt:
        print("Exiting DHT22 Sensors thread.")
    finally:
        if 'ser_dht' in locals() and ser_dht.is_open:
            ser_dht.close()
            print("DHT22 Sensors serial connection closed.")

# Run both threads
try:
    force_thread = threading.Thread(target=read_force_sensors, daemon=True)
    dht_thread = threading.Thread(target=read_dht22_sensors, daemon=True)
    
    force_thread.start()
    dht_thread.start()
    
    # Keep the main thread alive
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting program.")
