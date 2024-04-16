import requests

def get_coordinates(street_name):
    url = f"https://nominatim.openstreetmap.org/search?q={street_name}&format=json"
    response = requests.get(url)
    data = response.json()
    if data:
        first_result = data[0]
        latitude = float(first_result['lat'])
        longitude = float(first_result['lon'])
        return latitude, longitude
    return None

# Example usage
street_name = "Kanti Lokhpath"
coordinates = get_coordinates(street_name)
if coordinates:
    latitude, longitude = coordinates
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print("Coordinates not found.")