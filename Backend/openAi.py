import openai
import requests
import googlemaps
import json
import map_pin as mp
import webbrowser
import os
import time
from flask import Flask, render_template, redirect, request

# Initialize API keys
openai.api_key = ''
google_maps_api_key = ''

# Initialize Google Maps Client
gmaps = googlemaps.Client(key=google_maps_api_key)

# Define location and search parameters
miles = 5
radius = miles * 1609.35  # converting miles to meters
store_type = 'store and restaurants'

app = Flask(__name__)

def get_location():
    try:
        # Use IPinfo to get location based on IP
        response = requests.get("https://ipinfo.io")
        data = response.json()
        if "loc" in data:
            latitude, longitude = map(float, data["loc"].split(","))
            return latitude, longitude
        else:
            print("Could not retrieve location coordinates.")
            return None
    except requests.RequestException as e:
        print("Error fetching location:", e)
        return None


def get_all_nearby_stores(lat, lng, radius=radius):
    # Fetch all nearby stores within the specified radius using Google Maps Places API
    places_result = gmaps.places_nearby(
        location=(lat, lng),
        radius=radius,
        type=store_type
    )

    # Extract the names of all nearby stores
    store_names = [place['name'] for place in places_result.get('results', [])]
    return store_names


def get_product_suggestions(location, stores, user_interest):
    store_list = ", ".join(stores)
    messages = [
        {"role": "system",
         "content": "You are a helpful assistant providing product suggestions based on nearby products, ensure that the title of the establishment is in quotations, the address in [], and the numerical price in ()"},
        {"role": "user",
         "content": f"Suggest unique {user_interest} ideas for consumers in {location}, based on the season, culture, trends, and nearby stores: {store_list}. Only list top 3 stores or restaurants that are relevant to the item the user is interested in. Only say the top 3 stores with one item suggested or restertants (only if they ask something related to food). Don't talk anything more then it is necessary"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=500,
        n=1,
        temperature=0.7
    )

    return response['choices'][0]['message']['content'].strip().split('\n')
#
# @app.route('/search', nethods=['POST'])
# def search():
#     user_interest = request.form.get('user_interest')
#     if user_interest:
#         location = get_location()
#         if location:
#             latitude, longitude = location
#             nearby_stores = get_all_nearby_stores(latitude, longitude)
#             suggestions = get_product_suggestions("your area", nearby_stores, user_interest)
#
#             with open("suggestions.json", "w") as json_file:
#                 json.dump({"suggestions": suggestions}, json_file, indent=4)
#             return render_template('results.html', suggestions=suggestions, interest=user_interest)
#         else:
#             return "Could not determine a location"
#     else:
#         return "Please enter a valid search."

def run_ai(user_interest):
    # print('Running query....')
    # Ask the user what kind of products they are looking for
    # user_interest = input("What type of products are you interested in? (e.g., clothing, electronics, food): ")

    # Main program to find location, get all nearby stores, and suggest products
    location = get_location()
    if location:
        latitude, longitude = location
        nearby_stores = get_all_nearby_stores(latitude, longitude)  # Using the updated radius
        suggestions = get_product_suggestions("your area", nearby_stores, user_interest)

        with open("suggestions.json", "w") as json_file:
            json.dump({"suggestions": suggestions}, json_file, indent=4)

        for i, suggestion in enumerate(suggestions, start=1):
            print(f"{suggestion}")
    else:
        print("Could not determine location.")


# if __name__ == "__main__":
#     run_ai()
