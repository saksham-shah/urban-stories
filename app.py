from flask import Flask, request
import locations_to_words
import words_to_stories

app = Flask(__name__)


@app.route('/')
def handle_request():
    body = request.args
    lat = body.get("lat")
    lon = body.get("lon")
    try:
        lat = float(lat)
        lon = float(lon)
    except:
        raise Exception("lat="+str(lat)+" "+"lon="+str(lon)+" failed to parse lat and lon to floats")
    threewords = locations_to_words.w3w_convert(lat, lon)
    sentence = words_to_stories.convert(threewords)
    return sentence


if __name__ == '__main__':
    app.run()