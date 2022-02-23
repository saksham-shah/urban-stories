import requests
import pickle


latitude, longitude, radius = 52.2, 0.12, 0.1
overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = f"""
    [out:json];
    (
        nwr({latitude - radius}, {longitude - radius}, {latitude + radius}, {longitude + radius})["amenity"];
        nwr({latitude - radius}, {longitude - radius}, {latitude + radius}, {longitude + radius})["leisure"];
        nwr({latitude - radius}, {longitude - radius}, {latitude + radius}, {longitude + radius})["natural"];
        nwr({latitude - radius}, {longitude - radius}, {latitude + radius}, {longitude + radius})["tourism"];
        nwr({latitude - radius}, {longitude - radius}, {latitude + radius}, {longitude + radius})["surface"];
        nwr({latitude - radius}, {longitude - radius}, {latitude + radius}, {longitude + radius})["landuse"];
        nwr({latitude - radius}, {longitude - radius}, {latitude + radius}, {longitude + radius})["shop"];
    );
    out;
    """
response = requests.get(overpass_url, params={'data': overpass_query})
dict_w = {}


for w in [p["tags"]["amenity"] if "amenity" in p["tags"] else None for p in response.json()["elements"]]:
    if w in dict_w:
        dict_w[w] += 1
    else:
        dict_w[w] = 1

for w in [p["tags"]["leisure"] if "leisure" in p["tags"] else None for p in response.json()["elements"]]:
    if w in dict_w:
        dict_w[w] += 1
    else:
        dict_w[w] = 1

for w in [p["tags"]["natural"] if "natural" in p["tags"] and p["tags"]["natural"] != "water" else None for p in response.json()["elements"]]:
    if w in dict_w:
        dict_w[w] += 1
    else:
        dict_w[w] = 1

for w in [p["tags"]["surface"] if "surface" in p["tags"] else None for p in response.json()["elements"]]:
    if w in dict_w:
        dict_w[w] += 1
    else:
        dict_w[w] = 1

for w in [p["tags"]["landuse"] if "landuse" in p["tags"] else None for p in response.json()["elements"]]:
    if w in dict_w:
        dict_w[w] += 1
    else:
        dict_w[w] = 1

for w in [p["tags"]["shop"] if "shop" in p["tags"] else None for p in response.json()["elements"]]:
    if w in dict_w:
        dict_w[w] += 1
    else:
        dict_w[w] = 1

for w in [p["tags"]["water"] if "water" in p["tags"] else None for p in response.json()["elements"]]:
    if w in dict_w:
        dict_w[w] += 1
    else:
        dict_w[w] = 1

for w in [p["tags"]["man_made"] if "man_made" in p["tags"] else None for p in response.json()["elements"]]:
    if w in dict_w:
        dict_w[w] += 1
    else:
        dict_w[w] = 1

for w in [p["tags"]["barrier"] if "barrier" in p["tags"] else None for p in response.json()["elements"]]:
    if w in dict_w:
        dict_w[w] += 1
    else:
        dict_w[w] = 1

with open('Cambridge_words.pkl', 'wb') as f:
    pickle.dump(dict_w, f)



