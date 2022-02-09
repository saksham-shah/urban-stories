import gensim.downloader

glove_vectors = gensim.downloader.load("glove-wiki-gigaword-50")

def recursive_generate_similar_words(target_word):
    sims1 = set([p[0] for p in glove_vectors.most_similar(target_word, topn=5)])
    sims2 = set([])
    for w in sims1:
        sims2 = sims2.union(set([p[0] for p in glove_vectors.most_similar(w, topn=10)]))
    sims1 = sims1.union(sims2)
    return sims1


sim = recursive_generate_similar_words("hotel")
for word in sim:
    print(word)
