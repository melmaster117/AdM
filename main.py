# from database import create_connection, create_table, register_users, user_details, user_signin
# from flask import Flask, request, jsonify, session
# from flask_cors import CORS
import serial
import time

# app = Flask(__name__)
# app.secret_key = 'adm'
# CORS(app, origins=["http://localhost:3000"])

ser = serial.Serial('COM4', 115200)

def read_sensor_data():
    while True:
        if ser.in_waiting > 0:  
            data = ser.readline().decode('utf-8').strip()
            print(f"vales: {data}")
            return data

        time.sleep(1)

if __name__ == '__main__':
    while True:
        sensor_value = read_sensor_data() 
        time.sleep(0.5)
    # conn = create_connection()
    # create_table(conn)
    # app.run(debug=True)