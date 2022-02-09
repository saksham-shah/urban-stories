import requests

discarded_words = ["common", "general", "commercial", "retail", "station", "rental", "place", "of", "centre", "venue", 'fast', "box", "paving", "stones"]


def set_usage_by_coords(latitude, longitude, radius=0.001):
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
    response = requests.get(overpass_url,
                            params={'data': overpass_query})
    print("query complete")
    amenity_set = set([p["tags"]["amenity"] if "amenity" in p["tags"] else None for p in response.json()["elements"]])
    leisure_set = set([p["tags"]["leisure"] if "leisure" in p["tags"] else None for p in response.json()["elements"]])
    tourism_set = set([p["tags"]["tourism"] if "tourism" in p["tags"] else None for p in response.json()["elements"]])
    natural_set = set([p["tags"]["natural"] if "natural" in p["tags"] and p["tags"]["natural"] != "water" else None for p in response.json()["elements"]])
    surface_set = set([p["tags"]["surface"] if "surface" in p["tags"] else None for p in response.json()["elements"]])
    landuse_set = set([p["tags"]["landuse"] if "landuse" in p["tags"] else None for p in response.json()["elements"]])
    shop_set = set([p["tags"]["shop"] if "shop" in p["tags"] else None for p in response.json()["elements"]])
    water_set = set([p["tags"]["water"] if "water" in p["tags"] else None for p in response.json()["elements"]])
    return amenity_set.union(leisure_set).union(tourism_set).union(natural_set).union(water_set).union(surface_set).union(landuse_set).union(shop_set)


def preprocess_words(set_of_words):
    set_of_words.discard(None)
    temp_set = set_of_words.copy()
    for w in temp_set:
        if 'mixed' in w:
            set_of_words.remove(w)
    for w in temp_set:
        if '_' in w:
            set_of_words.remove(w)
            set_of_words = set_of_words.union(set(w.split('_')))
    temp_set = set_of_words.copy()
    for w in temp_set:
        if ' ' in w:
            set_of_words.remove(w)
            set_of_words = set_of_words.union(set(w.split(' ')))
    temp_set = set_of_words.copy()
    for w in temp_set:
        if '-' in w:
            set_of_words.remove(w)
            set_of_words = set_of_words.union(set(w.split('-')))
    for w in discarded_words:
        set_of_words.discard(w)
    return set_of_words


print(preprocess_words(set_usage_by_coords(43, -0.12, radius=0.0005)))