import create_stories
from os import path

def load_model():
    if not path.exists("models"):
        print("GPT2 model not yet downloaded. Downloading into 'models' folder.")
        create_stories.download_model()
    
    print("Loading GPT2 model")
    return create_stories.load_model()

def convert(wordtriple):
    sess = load_model()
    sentence = create_stories.generateWithKeywords(sess, "Once upon a time, ", wordtriple)
    print(str(sentence))

    return sentence