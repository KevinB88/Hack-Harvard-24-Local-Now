import re
import json
import requests
import time
import webbrowser
import os


def write_to_html_file(parsed_data_list, file_name='output.html'):
    # HTML template with embedded links and table structure
    html_content = """
    <html>
    <head>
        <title>Establishments</title>
        <style>
            table {
                font-family: Arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }
            td, th {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h2>List of Establishments</h2>
        <table>
            <tr>
                <th>Establishment</th>
                <th>Address</th>
                <th>Price</th>
                <th>Description</th>
                <th>Google Maps Link</th>
            </tr>
    """

    # Add a row for each parsed result
    for parsed_data in parsed_data_list:
        maps_url = generate_maps_url_from_address(parsed_data['address'])
        html_content += f"""
        <tr>
            <td>{parsed_data['establishment']}</td>
            <td>{parsed_data['address']}</td>
            <td>{parsed_data['price']}</td>
            <td>{parsed_data['description']}</td>
            <td><a href="{maps_url}" target="_blank">View on Google Maps</a></td>
        </tr>
        """

    # Close the HTML tags
    html_content += """
        </table>
    </body>
    </html>
    """

    # Write the HTML content to a file
    with open(file_name, 'w') as file:
        file.write(html_content)


# Function to extract establishment, address, and price from a suggestion string
def parse_suggestion(suggestion):
    # Establishment is in double quotes
    establishment_pattern = r'\"(.*?)\"'

    # Address is in square brackets
    address_pattern = r'\[(.*?)\]'

    # Price is in parentheses (matching any number inside parentheses)
    price_pattern = r'\((\$\d+)\)'

    # Search for establishment, address, and price using the updated patterns
    establishment_match = re.search(establishment_pattern, suggestion)
    address_match = re.search(address_pattern, suggestion)
    price_match = re.search(price_pattern, suggestion)

    establishment = establishment_match.group(1) if establishment_match else None
    address = address_match.group(1) if address_match else None
    price = price_match.group(1) if price_match else None

    description = suggestion.strip()  # Use the whole suggestion as the description

    # Ensure all fields are present before returning the result
    if establishment and address and price:
        return {
            'establishment': establishment,
            'address': address,
            'price': price,
            'description': description
        }
    return None


# Function to get coordinates using Google Geocoding API
def get_coordinates(address, api_key):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': address, 'key': api_key}
    response = requests.get(base_url, params=params)
    location_data = response.json()

    if location_data['status'] == 'OK':
        coordinates = location_data['results'][0]['geometry']['location']
        return coordinates['lat'], coordinates['lng']
    else:
        print(f"Error fetching coordinates for address: {address}")
        return None


# Function to generate Google Maps URL
def generate_maps_url_from_address(address):
    # Replace spaces with "+" and other URL encoding for addresses
    address_encoded = address.replace(" ", "+")
    return f"https://www.google.com/maps/search/?api=1&query={address_encoded}"


# Function to process suggestions and output information

def process_suggestions(data, api_key):
    suggestions = data.get('suggestions', [])
    for suggestion in suggestions:
        if suggestion.strip():  # Ignore empty strings
            parsed_entry = parse_suggestion(suggestion)
            if parsed_entry:
                establishment = parsed_entry['establishment']
                address = parsed_entry['address']
                description = parsed_entry['description']

                # Get coordinates from address
                coordinates = get_coordinates(address, api_key)
                if coordinates:
                    maps_url = generate_maps_url_from_address(address)

                    # Display the original description and map URL
                    print(f"Establishment: {establishment}")
                    print(f"Address: {address}")
                    print(f"Description: {description}")
                    print(f"Google Maps URL: {maps_url}")
                    print("\n")

# Convert JSON file to JSON string


def convert_file_to_string(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)  # Read the JSON from file
    json_string = json.dumps(data, indent=2)  # Convert it to a JSON string
    return json_string


# Load JSON from a string (for testing or after converting from a file)
def load_json_data_from_string(json_string):
    try:
        data = json.loads(json_string)  # Parse the string into a JSON object
        return data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None


# Replace with your actual Google Maps API key
google_api_key = ''

# Example: Loading data from a JSON string
# json_string = '''{
#     "suggestions": [
#         "1. Berry Delight Milkshake at \\"Russell House Tavern\\" [Address: 14 JFK St, Cambridge, MA 02138, USA, Approximate Price: $8]. This milkshake combines the freshness of seasonal berries with creamy dairy, providing a refreshing and flavorful option for those with peanut allergies.",
#         "",
#         "2. Tropical Bliss Milkshake at \\"Middle East Restaurant and Club\\" [Address: 472-480 Massachusetts Ave, Cambridge, MA 02139, USA, Approximate Price: $7]. This milkshake features a blend of tropical fruits like mango and pineapple, aligning with the trend for exotic, vibrant flavors.",
#         "",
#         "3. Classic Vanilla Milkshake at \\"The Sinclair\\" [Address: 52 Church St, Cambridge, MA 02138, USA, Approximate Price: $7]. For those who prefer a traditional milkshake, this is a safe and delicious option, ensuring that those with peanut allergies can enjoy a classic treat worry-free."
#     ]
# }'''


def mapify(json_file):
    json_string = convert_file_to_string(json_file)
    data = json.loads(json_string)
    suggestions = data.get('suggestions', [])
    print(suggestions)
    parsed_data_list = [parse_suggestion(suggestion) for suggestion in suggestions if parse_suggestion(suggestion)]
    print(parsed_data_list)
    write_to_html_file(parsed_data_list, file_name='../temp/output.html')

    time.sleep(6)
    webbrowser.open('file://' + os.path.realpath('../temp/output.html'))

    # Load and parse the JSON string
    data = load_json_data_from_string(json_string)

    # print(data)

    # Process the suggestions and output the information
    if data:
        process_suggestions(data, google_api_key)
    else:
        print('Error loading data from json.')


if __name__ == "__main__":
    # suggestions = convert_file_to_string('suggestions.json')
    # print(suggestions)
    # parsed_data_list = [parse_suggestion(suggestion) for suggestion in suggestions if parse_suggestion(suggestion)]
    # print(parsed_data_list)
    mapify('suggestions.json')
