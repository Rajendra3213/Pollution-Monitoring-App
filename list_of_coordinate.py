import asyncio
import aiohttp

async def query_overpass(session, data):
    overpass_url = "https://overpass-api.de/api/interpreter"
    async with session.get(overpass_url, params=data) as response:
        return await response.json()

async def get_coordinates_nearby(session, latitude, longitude, amenity):
    query = f"""
    [out:json];
    (
        node["amenity"="{amenity}"](around:1000, {latitude}, {longitude});
        way["amenity"="{amenity}"](around:1000, {latitude}, {longitude});
        relation["amenity"="{amenity}"](around:100, {latitude}, {longitude});
    );
    out center;
    """
    data = {
        'data': query
    }
    response = await query_overpass(session, data)
    coordinates = []
    for element in response['elements']:
        if 'lat' in element and 'lon' in element:
            lat = element['lat']
            lon = element['lon']
            coordinates.append({'latitude': lat, 'longitude': lon})
    return amenity, coordinates

latitude = 27.683119
longitude = 85.335269
amenities = [
    'park', 'industrial', 'marketplace',
    'sisdol_landfill', 'drainage_canal', 'religious_site', 'tourist_area',
    'construction_site', 'hospital',
    'festival_ground','composting_facility', 'brick_kiln'
]

async def main():
    coordinates = {}
    async with aiohttp.ClientSession() as session:
        tasks = []
        for amenity in amenities:
            task = asyncio.create_task(get_coordinates_nearby(session, latitude, longitude, amenity))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        for amenity, coords in results:
            if coords:
                coordinates[amenity] = coords
    
    print(coordinates)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())