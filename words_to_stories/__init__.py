from . import create_stories
from os import path


def load_model():
    if not path.exists("models"):
        print("GPT2 model not yet downloaded. Downloading into 'models' folder.")
        create_stories.download_model()
    
    print("Loading GPT2 model")
    return create_stories.load_model()


def convert(targets, prompt = "Once upon a time,"):
    # TODO: @Tom load_model takes a while to run but only needs to be run once when the server starts
    #       Can you move this code to wherever the server boots up, and store sess (the TenserFlow session) somewhere
    #       Then we can change this function to also take sess as a parameter which is passed to generate_story
    sess = load_model()

    # TODO: Figure out a better way to force GPT2 to create stories
    #       Maybe have a list of story openers and pick one at random
    #       Could maybe get a database of short stories from somewhere
    #       and use the opening few words from them
    prefix = "Here is a short story:\n\n"

    sentence = create_stories.generate_story(sess, prompt=prompt, targets=targets, prefix=prefix)
    print(str(sentence))

    return sentence
