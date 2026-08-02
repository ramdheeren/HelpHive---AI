from flask import Blueprint, render_template, request, jsonify

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        lat = data.get('latitude')
        lon = data.get('longitude')
        
        return jsonify({"message": "Location received", "latitude": lat, "longitude": lon})

    
    return render_template('test.html')

