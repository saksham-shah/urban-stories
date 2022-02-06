import requests
import pprint


# Example 1: Given coordinates, query for all nearby buildings
def query_buildings_by_coords(latitude, longitude):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    nwr({latitude-0.001}, {longitude-0.001}, {latitude+0.001}, {longitude+0.001})["building"]["name"];
    out center;
    """
    response = requests.get(overpass_url,
                            params={'data': overpass_query})
    print("query complete")
    data = response.json()
    for e in data["elements"]:
        print(e["tags"]["name"] + ", " + e["tags"]["building"])


# Example 2: Given coordinates, query for all nearby services and types
def query_amenity_by_coords(latitude, longitude):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
        [out:json];
        nwr({latitude - 0.001}, {longitude - 0.001}, {latitude + 0.001}, {longitude + 0.001})["amenity"]["name"];
        out center;
        """
    response = requests.get(overpass_url,
                            params={'data': overpass_query})
    print("query complete")
    data = response.json()
    for e in data["elements"]:
        print(e["tags"]["name"] + ", " + e["tags"]["amenity"])


# Example 3: Given coordinates, query for all nearby highways and their max speed (Unduplicated)
def query_highways_by_coords(latitude, longitude):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
        [out:json];
        nwr({latitude - 0.01}, {longitude - 0.01}, {latitude + 0.01}, {longitude + 0.01})["highway"]["name"];
        out center;
        """
    response = requests.get(overpass_url,
                            params={'data': overpass_query})
    print("query complete")
    data = response.json()
    list_of_roads = [(e["tags"]["name"] + (", " + e["tags"]["maxspeed"] if "maxspeed" in e["tags"] else "")) for e in data["elements"]]
    list_of_roads = list(set(list_of_roads))
    for r in list_of_roads:
        print(r)


query_highways_by_coords(52.21097338360007, 0.09147706269886703)
