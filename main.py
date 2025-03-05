from database import create_connection, create_table, register_users, user_details, user_signin
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import serial
import time

app = Flask(__name__)
app.secret_key = 'adm'
CORS(app, origins=["http://localhost:3000"])

ser = serial.Serial('COM4', 115200)

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        register_users(name, email, password)
        return jsonify({'message': 'Registered Successfully'}), 201

@app.route('/signin', methods=['POST'])
def signin():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if user_signin(email, password):
            session['email'] = email  
            return jsonify({'message': 'Login Successful'}), 200
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/details', methods=['POST'])
def user_details_path():
    
    try:
        data = request.get_json()
        email = data.get("email")

        if email:
            user_info = user_details(email)
            if user_info:
                return jsonify(user_info), 200
            else:
                return jsonify({"message": "User not found"}), 404
        else:
            return jsonify({"message": "Email is required"}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

@app.route('/results', methods=['GET'])
def read_sensor_data():
    while True:
        if ser.in_waiting > 0:  
            data = ser.readline().decode('utf-8').strip()
            print(f"vales: {data}")
            return jsonify({"data": '576'}), 200
        return jsonify({"data": "No data"}), 404


if __name__ == '__main__':
    conn = create_connection()
    create_table(conn)
    app.run(debug=True)