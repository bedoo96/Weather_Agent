from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__)

json_directory = r'D:\Internship NARLABS\Weather Agent\Json_files'

@app.route('/api/risk', methods=['GET'])
def index():
    return send_from_directory(json_directory, 'risk.json', mimetype='application/json')

@app.route('/api/weather', methods=['GET'])
def get_risk():
    return send_from_directory(json_directory, 'weather.json', mimetype='application/json')

if __name__ == '__main__':
    if not os.path.exists(json_directory):
        os.makedirs(json_directory)

    app.run(host='0.0.0.0', port=5000)
