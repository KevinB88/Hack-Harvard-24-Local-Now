from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GOOGLE_API_KEY = 'AIzaSyAYpgQVL5v22N50qYs4enxq0HSjp3C7yAM'

@app.route('/reverse_geocode', methods=['GET'])
def reverse_geocode():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if lat and lon:
        address = get_address_from_coords(lat, lon)
        return jsonify({"address": address})
    else:
        return jsonify({"error": "Missing coordinates"}), 400


def get_address_from_coords(lat, lon):
    API_KEY = GOOGLE_API_KEY  # Your Google Maps API key
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={API_KEY}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]['formatted_address']
        else:
            return "No address found"
    else:
        return "Error in reverse geocoding"


if __name__ == '__main__':
    app.run(debug=True)
