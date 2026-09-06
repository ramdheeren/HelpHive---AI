from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from .db import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        lat = data.get('latitude')
        lon = data.get('longitude')

        if not current_user.is_authenticated:
            return jsonify({"message": "Authentication required", "latitude": lat, "longitude": lon}), 401

        if lat is None or lon is None:
            return jsonify({"message": "Latitude and longitude are required", "latitude": lat, "longitude": lon}), 400

        db['users'].update_one(
            {'email': current_user.get_id()},
            {'$set': {'location': {'lat': lat, 'lon': lon}}}
        )
        
        return jsonify({"message": "Location received", "latitude": lat, "longitude": lon})

    
    return render_template('main.html')

