import requests
import json
import re

def get_local_coordinates():
    try:
        API_KEY = ''
        response = requests.get(f'http://ipinfo.io?token={API_KEY}')
        data = response.json()

        coordinates = data.get('loc')
        if coordinates:
            latitude, longitude = coordinates.split(',')
            lat = float(latitude)
            lon = float(longitude)
            return lat, lon
        else:
            print("Unable to retrieve location.")
            return None, None
    except Exception as e:
        print(F"Error occurred: {e}")
        return None, None

def get_address_from_coords(lat, lon):
    API_KEY = ''  # Your Google Maps API key
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


def parse_suggestions(data):
    suggestions = data['suggestions']
    localities = []

    # Regex patterns to match names and addresses
    name_pattern = r'"([^"]+)"'
    address_pattern = r'\[([^\]]+)\]'

    # Loop through each suggestion
    for suggestion in suggestions:
        if suggestion.strip():  # Skip empty strings
            # Extract name and address
            name_match = re.search(name_pattern, suggestion)
            address_match = re.search(address_pattern, suggestion)

            if name_match and address_match:
                name = name_match.group(1)
                address = address_match.group(1)
                localities.append({"name": name, "address": address})

    return {"localities": localities}


def convert_file_to_string(file_path):
    try:
        # Check if the file exists and is not empty
        with open(file_path, 'r') as file:
            content = file.read()

            # Print the raw file content for debugging
            if content.strip() == "":
                print("Error: The file is empty.")
                return None

            print(f"Raw File Content:\n{content}")  # Print the raw content for debugging

            # Attempt to load the content as JSON
            try:
                data = json.loads(content)  # Ensure the content is valid JSON
                json_string = json.dumps(data, indent=2)
                return json_string
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return None
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
