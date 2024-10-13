from flask import Flask, render_template, redirect
import re
import json
import requests
import geo as g
import openAi as ai
import ipinfo
import map_depen as mp

app = Flask(__name__)

GOOGLE_MAPS_API_KEY = 'AIzaSyAYpgQVL5v22N50qYs4enxq0HSjp3C7yAM'
@app.route('/')
def index():
    return redirect('/home/')

def mile_to_meter_conversion(miles):
    return miles * 1609.35

@app.route('/home/')
def show_map():
    map_arguments = {
        "radius": mile_to_meter_conversion(5),  # Radius in meters
        "center_address": origin,  # Valid address
        "localities": parsed_data['localities']  # Use parsed localities
    }
    return render_template('map.html', radius=map_arguments['radius'],
                           center_address=map_arguments['center_address'],
                           localities=map_arguments['localities'])


if __name__ == "__main__":

    # Execute AI-related functionality (as per your requirements)
    ai.run_ai()

    # Load and parse suggestions from the JSON file
    json_string = mp.convert_file_to_string('suggestions.json')
    if json_string:
        parsed_data = mp.parse_suggestions(json.loads(json_string))
    else:
        parsed_data = {"localities": []}  # Default to an empty list if parsing fails
    print(parsed_data)

    # Retrieve center address (example coordinates provided)
    lat, lon = mp.get_local_coordinates()
    origin = mp.get_address_from_coords(lat, lon)
    app.run()

