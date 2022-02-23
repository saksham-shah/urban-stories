import pprint
import pickle

with open('Cambridge_words.pkl', 'rb') as f:
    loaded_dict = pickle.load(f)
pprint.pprint(loaded_dict)
