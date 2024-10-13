from flask import Flask, request, render_template, jsonify
import openAi as ai  # Assuming openAi.py is available for querying GPT
import json
import map_depen as mp  # Assuming map_pin.py handles the parsing of localities and map logic

app = Flask(__name__)


@app.route('/')
def index():
    # Render the main search page
    return render_template('main_page.html')


@app.route('/search', methods=['POST'])
def search():
    # Get the user input from the search form
    user_interest = request.form.get('user_interest')

    if user_interest:
        # Run OpenAI query with the user interest
        result = ai.run_ai(user_interest)

        # Load and parse suggestions from the JSON file
        json_string = mp.convert_file_to_string('suggestions.json')

        if json_string:
            parsed_data = mp.parse_suggestions(json.loads(json_string))
        else:
            parsed_data = {"localities": []}  # Default to empty if no data

        print("parsed data: ", parsed_data)

        lat, lng = mp.get_local_coordinates()
        origin = mp.get_address_from_coords(lat, lng)

        # Set the necessary map-related arguments
        map_arguments = {
            "radius": 1609.35 * 5,  # Example: 5 miles in meters
            "center_address": origin,  # Replace with logic to dynamically get the address
            "localities": parsed_data['localities']
        }

        # Pass data to the map.html template and render the map
        return render_template('map.html',
                               radius=map_arguments['radius'],
                               center_address=map_arguments['center_address'],
                               localities=map_arguments['localities'])
    else:
        return "Please enter a valid input."


if __name__ == "__main__":
    app.run(debug=True)
