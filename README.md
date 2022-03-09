# urban-stories
An app that generates stories based on your location
## Running the backend
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