# https://stackabuse.com/text-generation-with-python-and-tensorflow-keras/

# Keras is an easier to use API for TensorFlow

# Use 'pip3 install' to install  to run this

# frankenstein.txt has the first three chapters

import numpy
import sys
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint

# nltk.download('stopwords')

file = open("frankenstein.txt").read()

def tokenize_words(input):
    # Lowercase everything to standardise it
    input = input.lower()

    # Instantiate tokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(input)

    # Keep the tokens that are in the stop words
    filtered = filter(lambda token: token not in stopwords.words('english'), tokens)
    return " ".join(filtered)


# Preprocess the input data and make tokens
processed_inputs = tokenize_words(file)

chars = sorted(list(set(processed_inputs)))
char_to_num = dict((c, i) for i, c in enumerate(chars))

input_len = len(processed_inputs)
vocab_len = len(chars)

print("Total number of characters:", input_len)
print("Total vocab:", vocab_len)

seq_length = 100
x_data = []
y_data = []

