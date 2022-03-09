from . import create_stories
from os import path

# Load model and start TensorFlow session
def load_model():
    if not path.exists("models"):
        print("GPT2 model not yet downloaded. Downloading into 'models' folder.")
        create_stories.download_model()
    
    print("Loading GPT2 model")
    return create_stories.load_model()


def convert(targets, prompt = "Once upon a time,"):
    # Load the model to be used
    sess = load_model()

    # Prompt GPT2 into creating a story
    prefix = "Here is a short story:\n\n"

    # Generate and return the story created from the target words
    sentence = create_stories.generate_story(sess, prompt=prompt, targets=targets, prefix=prefix)
    print(str(sentence))

    return sentence
