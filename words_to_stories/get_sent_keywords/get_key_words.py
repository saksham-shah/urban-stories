from lib2to3.pgen2.tokenize import tokenize
import rank_words
from nltk.tokenize import sent_tokenize
import re

def get_global_token_freqs():
    f = open("nesbit.txt", "r")
    text = f.read().lower()
    freqs = rank_words.get_word_freqs(text)
    return freqs

def get_key_words(sentence, n):
    global_freqs = get_global_token_freqs() 
    tokens = rank_words.tokenise(sentence)
    sentence_freqs = {token: global_freqs[token] for token in tokens}
    ordered_tokens = sorted(sentence_freqs, key=lambda x: sentence_freqs[x])
    sentence_freqs = {token: sentence_freqs[token] for token in ordered_tokens}
    return list(sentence_freqs.keys())[:min(len(tokens), n)]

def get_test_sentences():
    f = open("nesbit.txt", "r")
    text = f.read()
    text = re.sub("\s+", " ", text)
    # tokeniser = RegexpTokenizer("[^\.]+[\!\?\.]")
    sentences = sent_tokenize(text[:10000])
    sentences = list(map(lambda x: x.strip(), sentences))
    return sentences

sentence = "The quick brown fox jumped over the lazy dog"

# key_words = get_key_words(sentence, 7)
# print(key_words)

test_sentences = get_test_sentences()
for s in test_sentences:
    print("------------")
    print(f"sentence:\n{s}")
    key_words = get_key_words(s, 3)
    print(f"keywords: {key_words}\n")
