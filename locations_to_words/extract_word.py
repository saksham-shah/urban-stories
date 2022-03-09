import requests
import pickle


discarded_words = {"yes", "common", "general", "commercial", "retail", "station", "rental", "place", "of", "centre",
                   "venue", 'fast', "box", "paving", "stones"}
word_file = "locations_to_words\\London_words.pkl"


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
    amenity_set = set([p["tags"]["amenity"] if "amenity" in p["tags"] else None for p in response.json()["elements"]])
    leisure_set = set([p["tags"]["leisure"] if "leisure" in p["tags"] else None for p in response.json()["elements"]])
    tourism_set = set([p["tags"]["tourism"] if "tourism" in p["tags"] else None for p in response.json()["elements"]])
    natural_set = set(
        [p["tags"]["natural"] if "natural" in p["tags"] and p["tags"]["natural"] != "water" else None for p in
         response.json()["elements"]])
    surface_set = set([p["tags"]["surface"] if "surface" in p["tags"] else None for p in response.json()["elements"]])
    landuse_set = set([p["tags"]["landuse"] if "landuse" in p["tags"] else None for p in response.json()["elements"]])
    shop_set = set([p["tags"]["shop"] if "shop" in p["tags"] else None for p in response.json()["elements"]])
    water_set = set([p["tags"]["water"] if "water" in p["tags"] else None for p in response.json()["elements"]])
    man_made_set = set(
        [p["tags"]["man_made"] if "man_made" in p["tags"] else None for p in response.json()["elements"]])
    barrier_set = set([p["tags"]["barrier"] if "barrier" in p["tags"] else None for p in response.json()["elements"]])
    name_set = set([p["tags"]["name"] if "name" in p["tags"] else None for p in response.json()["elements"]])
    name_set.discard(None)
    return amenity_set.union(leisure_set).union(tourism_set).union(natural_set).union(water_set).union(surface_set).\
               union(landuse_set).union(shop_set).union(man_made_set).union(barrier_set), name_set


def postprocess_words(list_of_words):
    if None in list_of_words:
        list_of_words.remove(None)
    list_of_words = [w.replace('_', ' ') if '_' in w else w for w in list_of_words]
    list_of_words = [w.replace('-', ' ') if '_' in w else w for w in list_of_words]
    list_of_words = [w.split()[0] if ' ' in w else w for w in list_of_words]
    for w in discarded_words:
        if w in list_of_words:
            list_of_words.remove(w)
    return list_of_words


def conclude_words(latitude, longitude, radius=0.001):
    # Query limit is 2, so at maximum try one more time for each user
    query_words, _ = set_usage_by_coords(latitude, longitude, radius=radius)
    if len(query_words) < 6:
        query_words, _ = set_usage_by_coords(latitude, longitude, radius=radius * 2)
    with open(word_file, 'rb') as f:
        sample_dict = pickle.load(f)
    dict_words = {}
    for w in query_words:
        if w in sample_dict:
            dict_words[w] = sample_dict[w]
        else:
            dict_words[w] = 1
    dict_words = {k: v for k, v in sorted(dict_words.items(), key=lambda item: item[1])}
    all_words = list(dict_words.keys())
    all_words = postprocess_words(all_words)[:10]
    return all_words
