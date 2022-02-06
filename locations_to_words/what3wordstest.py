import what3words

geocoder = what3words.Geocoder("L5311VV5")

res = geocoder.convert_to_3wa(what3words.Coordinates(51.484463, -0.195405))
print(res)