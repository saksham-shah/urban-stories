from tokenize import TokenInfo
from nltk.tokenize import RegexpTokenizer
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

def tokenise(text):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text.lower())
    return tokens

def get_word_freqs(text):
    tokens = tokenise(text)
    token_counts = {}
    for token in tokens:
        if token not in token_counts.keys():
            token_counts[token] = 0
        token_counts[token] += 1
    return token_counts    

if __name__ == "__main__":
    f = open("nesbit.txt", "r")
    text = f.read()
    tokens = tokenise(text)[:2000000]

    token_counts = {}
    for token in tokens:
        if token not in token_counts.keys():
            token_counts[token] = 0
        token_counts[token] += 1


    ordered_tokens = sorted(token_counts, key=lambda x: token_counts[x], reverse=True)

    for token in ordered_tokens[:100]:
        print(f"{token}\t{token_counts[token]}")

    n = 500
    type_freqs = [token_counts[token] for token in ordered_tokens[:n]]
    plt.bar(np.arange(n), type_freqs)
    plt.show()
