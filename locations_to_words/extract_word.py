import requests
import gensim.downloader

discarded_words = ["yes", "common", "general", "commercial", "retail", "station", "rental", "place", "of", "centre",
                   "venue", 'fast', "box", "paving", "stones"]
glove_vectors = gensim.downloader.load("glove-wiki-gigaword-50")


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


def postprocess_words(set_of_words):
    set_of_words.discard(None)
    phrases = set({})
    temp_set = set_of_words.copy()
    for w in temp_set:
        if 'mixed' in w:
            set_of_words.remove(w)
    for w in temp_set:
        if '_' in w:
            set_of_words.remove(w)
            phrases.add(w.replace('_', ' '))
    temp_set = set_of_words.copy()
    for w in temp_set:
        if ' ' in w:
            set_of_words.remove(w)
            phrases.add(w)
    temp_set = set_of_words.copy()
    for w in temp_set:
        if '-' in w:
            set_of_words.remove(w)
            phrases.add(w)
    for w in discarded_words:
        set_of_words.discard(w)
    return set_of_words, phrases


def generate_similar_words(target_word):
    sims = set([p[0] for p in glove_vectors.most_similar(target_word, topn=1)])
    return sims.union(set(target_word))


def conclude_words(latitude, longitude, radius=0.0005):
    # Query limit is 2, so at maximum try one more time for each user
    query_words, name_words = set_usage_by_coords(latitude, longitude, radius=radius)
    if len(query_words) <= 3:
        query_words, name_words = set_usage_by_coords(latitude, longitude, radius=radius * 2)
    elif len(query_words) >= 10:
        query_words, name_words = set_usage_by_coords(latitude, longitude, radius=radius / 4)
    processed_words, phrases = postprocess_words(query_words)
    all_words = generate_similar_words(processed_words).union(name_words).union(phrases)
    return all_words


print(conclude_words(22.15186612658251, 113.56672739616229, radius=0.0005))
