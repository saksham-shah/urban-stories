
# urban-stories
An app that generates stories based on your location
## Running the back-end
### Install required modules
First, you will need to install several Python modules using `pip install`:
* flask
* what3words
* requests
* pickle
* numpy
* tensorflow
* gpt_2_simple

On running the code, there may be more modules missed from this list. Please install any modules indicated to run the server.
### Download the GPT2 model
Before you can run the server, you will need to download the GPT2 model. We have used the 124M parameter by default, although this can easily be changed.

The model can be downloaded by running `words_to_stores/download_model.py` once. This will download the model and put it in a `models` folder in the project directory.

Once downloaded, this file should not need to be run again on this device.
### Run the server
The server can be started by running `app.py`. It will be running on http://127.0.0.1:5000/
The server takes latitude and longitude coordinates and returns the story generates based on that location.
Try it out in your browser by going to http://127.0.0.1:5000/?lat=\[LATITUDE\]&lon=\[LONGITUDE\], e.g. http://127.0.0.1:5000/?lat=1&lon=1

NOTE: GPT2 takes a while to download, load and run. All of the above files take some time to run, and the stories also take about a minute to be generated. You can follow the progress of story generation by looking at the console of the server.
## Running the front-end
The front-end has been designed using Flutter. It uses the above server to request stories for a specific location. We cannot host our server anywhere for free as the GPT2 model is too large to store, so the front-end can't actually be linked to the back-end. This can easily be fixed by hosting the server commercially.
## Files
* `app.py`: main server file
* `locations_to_words/__init__.py`: entry point for code that takes locations and returns keywords
* `locations_to_words/extract_word.py`: takes locations and returns keywords
* `locations_to_words/collect_words.py`: collect set of words from a big area, used to create word frequency dictionary.
* `locations_to_words/London_words.pkl`: one of the word frequency dictionary, sampling words from London.
* `words_to_stories/__init__.py`: entry point for code that takes keywords and generates stories
* `words_to_stories/create_stories.py`: takes keywords and generates stories
* `words_to_stories/download_model.py`: downloads the GPT2 model
* `words_to_stories/gpt_2.py`: adapted from gpt_2_simple
* `words_to_stories/sample.py`: adapted from gpt_2_simple
* `words_to_stories/gpt2_utilities.py`: utility functions to help in generating stories

Other files in this repository were used for testing and debugging.
