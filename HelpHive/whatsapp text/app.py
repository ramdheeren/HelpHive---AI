from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enable CORS for all routes with debugging
CORS(app)
logger.info("CORS configured to allow all origins")

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")
logger.info("SocketIO initialized for real-time communication")

# Sample data storage
requests_data = []  # List of requests from seekers
matches = {}  # Dictionary to store matched volunteers
volunteer_matches = {}  # Stores matches for each volunteer

@app.route('/api/requests', methods=['GET'])
def get_requests():
    logger.info(f"GET /api/requests - Returning {len(requests_data)} requests")
    return jsonify(requests_data)

@app.route('/api/requests', methods=['POST'])
def add_request():
    try:
        data = request.json
        logger.info(f"POST /api/requests - Received data: {data}")
        
        if 'name' in data and 'requestDetails' in data:
            new_request = {"id": len(requests_data) + 1, "name": data["name"], "requestDetails": data["requestDetails"]}
            requests_data.append(new_request)
            logger.info(f"Request added successfully: {new_request}")
            
            return jsonify({"message": "Request added", "request": new_request}), 201
        else:
            logger.warning("Invalid request data received")
            return jsonify({"error": "Invalid request data"}), 400
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/matches/<int:request_id>', methods=['POST'])
def match_volunteers(request_id):
    try:
        data = request.json
        selected_volunteers = data.get("volunteers", [])
        matches[request_id] = selected_volunteers
        
        for volunteer in selected_volunteers:
            if volunteer not in volunteer_matches:
                volunteer_matches[volunteer] = []
            volunteer_matches[volunteer].append(request_id)
            socketio.emit("match_notification", {"volunteer": volunteer, "request_id": request_id})
        
        return jsonify({"message": "Volunteers matched", "matches": selected_volunteers}), 200
    except Exception as e:
        logger.error(f"Error matching volunteers: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/volunteers/<string:volunteer_name>/matches', methods=['GET'])
def get_volunteer_matches(volunteer_name):
    volunteer_requests = volunteer_matches.get(volunteer_name, [])
    return jsonify({"matches": volunteer_requests})

@app.route('/api/matches/<int:request_id>/accept', methods=['PATCH'])
def accept_match(request_id):
    try:
        volunteer = request.json.get("volunteer")
        if request_id in matches and volunteer in matches[request_id]:
            whatsapp_url = f"https://wa.me/?text=I'm accepting your volunteer request: {request_id}"
            socketio.emit("match_notification", {"volunteer": volunteer, "message": "Match accepted"})
            return jsonify({"message": "Match accepted", "redirect_url": whatsapp_url}), 200
        return jsonify({"error": "Match not found"}), 404
    except Exception as e:
        logger.error(f"Error accepting match: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/matches/<int:request_id>/reject', methods=['PATCH'])
def reject_match(request_id):
    try:
        volunteer = request.json.get("volunteer")
        if request_id in matches and volunteer in matches[request_id]:
            matches[request_id].remove(volunteer)
            socketio.emit("match_notification", {"volunteer": volunteer, "message": "Match rejected"})
            return jsonify({"message": "Match rejected"}), 200
        return jsonify({"error": "Match not found"}), 404
    except Exception as e:
        logger.error(f"Error rejecting match: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Check which port we're using and print it
    port = 5000  # You can change this to 8080 if needed
    logger.info(f"Starting Flask server on port {port}")
    print(f"API is available at: http://127.0.0.1:{port}/api")
    socketio.run(app, host="0.0.0.0", port=port, debug=True)
