import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# File to store sensor data
data_file = "latest_sensor_data.json"

# Precautions for anomalies
precautions = {
    "BPM": "Consult a doctor if BPM is too high or low.",
    "SpO2": "Increase oxygen intake or consult a healthcare provider.",
    "Temperature": "Drink water, rest, or seek medical advice if fever persists.",
    "Humidity": "Use a humidifier or dehumidifier as needed.",
    "Steps": "Reduce excessive physical activity."
}

# Initialize the JSON file if it doesn't exist
if not os.path.exists(data_file):
    with open(data_file, 'w') as file:
        json.dump({}, file)

# Function to write data to the file
def write_to_file(data):
    with open(data_file, 'w') as file:
        json.dump(data, file)

# Function to read data from the file
def read_from_file():
    with open(data_file, 'r') as file:
        return json.load(file)

@app.route('/data', methods=['POST', 'GET'])
def receive_data():
    if request.method == 'POST':
        try:
            # Log incoming JSON payload
            incoming_data = request.json
            print("Received Data:", incoming_data)

            # Simulate anomaly detection
            anomalies = {}
            if incoming_data.get('BPM', 0) < 60 or incoming_data.get('BPM', 0) > 120:
                anomalies['BPM'] = "Anomalous BPM detected!"
            if incoming_data.get('SpO2', 0) < 92 or incoming_data.get('SpO2', 0) > 100:
                anomalies['SpO2'] = "Anomalous SpO2 level detected!"
            if incoming_data.get('Temperature', 0) < 35 or incoming_data.get('Temperature', 0) > 38:
                anomalies['Temperature'] = "Temperature out of range!"
            if incoming_data.get('Humidity', 0) < 20 or incoming_data.get('Humidity', 0) > 60:
                anomalies['Humidity'] = "Humidity out of acceptable range!"
            if incoming_data.get('Steps', 0) > 10000:
                anomalies['Steps'] = "Unusual step count!"

            # Log anomalies
            if anomalies:
                print("Anomalies Detected:", anomalies)

            # Add anomalies to the data
            incoming_data["anomalies"] = anomalies

            # Write data to the file
            write_to_file(incoming_data)

            return jsonify({"status": "success", "anomalies": anomalies}), 200
        except Exception as e:
            print("Error:", e)
            return jsonify({"status": "error", "message": str(e)}), 500

    elif request.method == 'GET':
        try:
            # Read data from the file
            data = read_from_file()

            # Prepare response with anomalies and precautions
            response = {
                "data": data,
                "anomalies": data.get("anomalies", {}),
                "precautions": {
                    key: precautions[key] for key in data.get("anomalies", {}).keys()
                }
            }
            return jsonify(response), 200
        except Exception as e:
            print("Error reading data:", e)
            return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "running", "message": "Flask server is running!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

