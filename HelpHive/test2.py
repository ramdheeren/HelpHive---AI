import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()

def expand_google_maps_link(short_url):
    try:
        response = requests.get(short_url, allow_redirects=True)
        return response.url  # Returns the full URL
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Example usage
short_link = "https://maps.app.goo.gl/z913aTrajoH4Ruks8"
full_url = expand_google_maps_link(short_link)


def dms_to_decimal(dms):
    """Converts DMS (Degrees, Minutes, Seconds) format to decimal degrees."""
    match = re.match(r"(\d+)°(\d+)'([\d.]+)\"?([NSEW])", dms)
    if not match:
        return None
    
    degrees, minutes, seconds, direction = match.groups()
    decimal = float(degrees) + float(minutes) / 60 + float(seconds) / 3600

    # South and West should be negative
    if direction in ['S', 'W']:
        decimal *= -1

    return decimal


def extract_coordinates(url):
    # Check for standard decimal format
    match = re.search(r'@([-0-9.]+),([-0-9.]+)', url)
    if match:
        return match.groups()

    match = re.search(r'!3d([-0-9.]+)!4d([-0-9.]+)', url)
    if match:
        return match.groups()

    # Check for DMS format
    match = re.findall(r'(\d+°\d+\'[\d.]+\"?[NSEW])', url)
    if len(match) == 2:
        lat, lon = match
        return dms_to_decimal(lat), dms_to_decimal(lon)

    return None  

user_coords = extract_coordinates(expand_google_maps_link('https://maps.app.goo.gl/6VWgpA2ZTpwXtBtt9'))


destination_coords = extract_coordinates(expand_google_maps_link('https://maps.app.goo.gl/QMRfWjSBMGU6L2Te7'))

print(user_coords)
print(destination_coords)

def get_road_distance(user_coords, destination_coords):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": os.getenv('ROUTES_API_KEY_NEW'),
        "X-Goog-FieldMask": "routes.distanceMeters,routes.duration"
    }
    
    body = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": float(user_coords[0]), 
                    "longitude": float(user_coords[1])
                    }
                }
            },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": float(destination_coords[0]), 
                    "longitude": float(destination_coords[1])
                    }
                }
            },
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
        "computeAlternativeRoutes": False,
        "units": "METRIC"
    }
    
    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if "routes" in data and len(data["routes"]) > 0:
            return data['routes']
            return data["routes"][0]["distanceMeters"] / 1000  # Convert meters to km
        
        return None
    return None

print(get_road_distance(user_coords=user_coords, destination_coords=destination_coords))


