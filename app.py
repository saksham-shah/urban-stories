from flask import Flask, request
import locations_to_words
import words_to_stories
import os

app = Flask(__name__)


@app.route('/')
def handle_request():
    body = request.args
    lat = body.get("lat")
    lon = body.get("lon")
    id = body.get("id")
    try:
        lat = float(lat)
        lon = float(lon)
    except:
        raise Exception("lat="+str(lat)+" "+"lon="+str(lon)+" failed to parse lat and lon to floats")
    if id == None:
        threewords = locations_to_words.similar_word_convert(lat, lon) + locations_to_words.w3w_convert(lat, lon)
        #sentence = words_to_stories.convert(threewords)
        return "The words to convert are "+str(threewords)+"."
    else:
        fileloc = "saved_stories/"+str(id)+".txt"
        if os.path.exists(fileloc):
            with open(fileloc, "r") as file:
                prompt = file.read()
        else:
            prompt = "Once upon a time,"
        threewords = locations_to_words.similar_word_convert(lat, lon) + locations_to_words.w3w_convert(lat, lon)
        sentence = words_to_stories.convert(threewords, prompt)
        with open(fileloc, "w") as file:
            prompt = file.write(sentence)
        return sentence
    return sentence


if __name__ == '__main__':
    app.run()