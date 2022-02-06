# https://stackabuse.com/text-generation-with-python-and-tensorflow-keras/

# Keras is an easier to use API for TensorFlow

# Use 'pip3 install' to install any modules that aren't found to run this

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

# Loop through inputs, start at the beginning and go until we hit
# the final character we can create a sequence out of
for i in range(0, input_len - seq_length, 1):
    # Define input and output sequences
    # Input is the sequence of characters starting from the current one
    in_seq = processed_inputs[i:i + seq_length]

    # Output is the character right aftter the input
    out_seq = processed_inputs[i + seq_length]

    # Convert list of characters to integers
    # Add the values to our lists
    x_data.append([char_to_num[char] for char in in_seq])
    y_data.append(char_to_num[out_seq])

n_patterns = len(x_data)
print("Total patterns:", n_patterns)

X = numpy.reshape(x_data, (n_patterns, seq_length, 1))
X = X/float(vocab_len)

y = np_utils.to_categorical(y_data)

model = Sequential()
model.add(LSTM(256, input_shape = (X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(128))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')

# # Set checkpoint to save model to
# filepath = "model_weights_saved.hdf5"
# checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
# desired_callbacks = [checkpoint]

# # Train model
# print("Training model")
# model.fit(X, y, epochs=4, batch_size=256, callbacks=desired_callbacks)

# Load model
filename = "model_weights_saved.hdf5"
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')

num_to_char = dict((i, c) for i, c in enumerate(chars))

start = numpy.random.randint(0, len(x_data) - 1)
pattern = x_data[start]
print("Random Seed:")
print("\"", ''.join([num_to_char[value] for value in pattern]), "\"")

output = []

for i in range(1000):
    x = numpy.reshape(pattern, (1, len(pattern), 1))
    x = x / float(vocab_len)
    prediction = model.predict(x, verbose=0)
    index = numpy.argmax(prediction)
    result = num_to_char[index]

    # sys.stdout.write(result)
    output.append(result)
    print(result)

    pattern.append(index)
    pattern = pattern[1:len(pattern)]