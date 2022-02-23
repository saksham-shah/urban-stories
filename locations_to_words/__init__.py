import what3words

def w3w_convert(lat, lon):
    geocoder = what3words.Geocoder("L5311VV5")
    words = geocoder.convert_to_3wa(what3words.Coordinates(lat,lon))['words'].split(".")
    return words

def similar_word_convert(lat, lon):
    return ["place", "holder", "words"]
