import requests

def get_street_name(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json"
    response = requests.get(url)
    data = response.json()
    if 'address' in data:
        address = data['address']
        print(address)
        if 'road' in address:
            return address['road']
    return None

# Example usage
latitude = 27.660361
longitude =85.316299
street_name = get_street_name(latitude, longitude)
if street_name:
    print(f"Street Name: {street_name}")
else:
    print("Street name not found.")