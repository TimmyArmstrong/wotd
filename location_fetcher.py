import json
import requests

def parse_last_entry(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
        if not lines:
            raise ValueError("File is empty")
        last_line = lines[-1].strip()

    # Remove trailing semicolon if present
    if last_line.endswith(";"):
        last_line = last_line[:-1]

    # Split into parts: city_state_region_altitude_lat_long
    parts = last_line.split("_")
    if len(parts) < 6:
        raise ValueError("Line format incorrect, expected at least 6 parts separated by '_'")

    city = parts[0].strip()
    state = parts[1].strip()
    region = parts[2].strip()

    try:
        altitude = float(parts[3])
        altitude_rounded = round(altitude)
    except ValueError:
        raise ValueError("Altitude is not a valid float")

    try:
        latitude = float(parts[4])
    except ValueError:
        raise ValueError("Latitude is not a valid float")

    try:
        longitude = float(parts[5])
    except ValueError:
        raise ValueError("Longitude is not a valid float")

    # Bundle into dict and return
    return {
        "city": city,
        "state": state,
        "region": region,
        "altitude_metres": altitude_rounded,
        "latitude": latitude,
        "longitude": longitude
    }

# File to read from
input_file = "location-data.txt"
output_file = "location_data_output.json"

# Parse and save
location_data = parse_last_entry(input_file)

# Save to JSON
with open(output_file, "w") as f:
    json.dump(location_data, f, indent=2)

print("Location data saved to", output_file)



def get_weather_sentence(lat, long):
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": "09b60f57eed648d5ad6124035251906",
        "q": f"{lat},{long}",
        "aqi": "no"
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()  # Raise error for bad HTTP status
        data = response.json()
        
        feels_like = data['current']['feelslike_c']
        humidity = data['current']['humidity']
        condition = data['current']['condition']['text']
        
        return f"Condtion is {condition}. Temperature feels like {feels_like}°C with {humidity}% humidity."
    
    except (requests.RequestException, KeyError, ValueError):
        # Handle network errors, missing keys, or invalid JSON
        return ""

def get_lat_long(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    return latitude, longitude

input_json = "location_data_output.json"

lat, long = get_lat_long(input_json)
print(f"Latitude: {lat}, Longitude: {long}")

sentence = get_weather_sentence(lat, long)
print(sentence or "")

with open("weather_output.json", "w") as f:
    json.dump({"weather_summary": sentence}, f)
