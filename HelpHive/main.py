import flask
import os
import sys
from pathlib import Path

from app import db, views, auth, models
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_login import LoginManager, current_user
from flask_cors import CORS

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bert_matching import find_matching_providers


load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.register_blueprint(views.views, url_prefix='/')
app.register_blueprint(auth.auth, url_prefix='/')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

db = db.db 

@login_manager.user_loader
def load_user(email):
    user_details = db['users'].find_one({'email': email})
    
    user = models.User(
        email=email,
        phone=user_details['phone'],
        password=user_details['password'],
        first_name=user_details['first_name'],
        last_name=user_details['last_name'],
        is_volunteer=user_details['is_volunteer'],
        skills=user_details['skills'],
        radius=user_details['radius'],
        days=user_details['days'],
        location=user_details['location']
    )
    
    return user


CORS(app, resources={r"/api/*": {"origins": "*"}})


requests_data = []


@app.route('/requests', methods=['GET', 'POST'])
def get_requests():
    if request.method == 'POST':
        data = request.json
        if 'name' in data and 'requestDetails' in data:
            new_request = {"id": len(requests_data) + 1, "name": data["name"], "requestDetails": data["requestDetails"]}
            requests_data.append(new_request)

            matches = []
            if current_user.is_authenticated:
                user_details = db["users"].find_one({"email": current_user.get_id()})
                location = user_details.get("location") if user_details else None
                if isinstance(location, dict):
                    latitude = location.get("lat")
                    longitude = location.get("lon")
                    valid_location = (
                        not isinstance(latitude, bool)
                        and not isinstance(longitude, bool)
                        and isinstance(latitude, (int, float))
                        and isinstance(longitude, (int, float))
                    )
                    if valid_location:
                        try:
                            matches = find_matching_providers(data["requestDetails"], location)
                        except Exception as error:
                            print(f"Matcher error: {error}")

            return jsonify({"message": "Request added", "request": new_request, "matches": matches}), 201
        return jsonify({"error": "Invalid request data"}), 400
    
    else:
        return jsonify(requests_data)


@app.route('/requests/<int:request_id>/accept', methods=['PATCH'])
def accept_request(request_id):
    for req in requests_data:
        if req['id'] == request_id:
            return jsonify({"message": "Request accepted"}), 200
        
    return jsonify({"error": "Request not found"}), 404


@app.route('/requests/<int:request_id>/reject', methods=['PATCH'])
def reject_request(request_id):
    for req in requests_data:
        if req['id'] == request_id:
            requests_data.remove(req)
            return jsonify({"message": "Request rejected"}), 200

    return jsonify({"error": "Request not found"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8000)
