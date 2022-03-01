import gpt_2 as gpt2
import gpt2_utilities as util

# Set model to use: 124M, 335M or 774M
model_name = "124M"

def download_model(model_name="124M"):
    # Download the model - should only need to run this once
    # Saves the model in a 'models' folder
    gpt2.download_gpt2(model_name=model_name)

def load_model(model_name="124M"):
    # Load the model to be used
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, model_name=model_name)
    return sess

# Generate a story based on target words
# If anything goes wrong, it returns None
def generate_with_targets(sess, prompt, targets):
    story = prompt
    for word in targets:
        print("before searching for " + word + ": " + story)
        story = util.generateSanitised(sess, prefix=story, length=20, target=word, model_name=model_name)
        if story is None:
            return None
        
        print("after searching for " + word + ": " + story)
        story = util.generateSanitised(sess, prefix=story, length=20, model_name=model_name)
        if story is None:
            return None

    story = util.generateEnd(sess, prefix=story, length=20, model_name=model_name)
    # print(story)
    return story

# Generate a story based on target words
# Wraps the function above by constantly trying to generate a story
# until one is successfully created
def generate_story(sess, prompt, targets, prefix=None):
    # Prompt is the start of the story
    #       e.g. "Once upon a time,"
    # Prefix is an extra prompt that isn't part of the story
    # But it can be used to push GPT2 to writing a story
    #       e.g. "Here is a short story:\n\n"

    # Join the prefix and prompt
    if prefix is not None:
        prompt = prefix + prompt

    # Keep generating stories until success
    story = None
    while story is None:
        story = generate_with_targets(sess, prompt, targets)

    # Remove the prefix from the generated story
    if prefix is not None:
        story = story[len(prefix):]
    
    return story

sess = load_model(model_name="124M")

story = generate_story(sess, prompt="Once upon a time,", targets=["church", "train", "phone"], prefix="Here is a short story for young children:\n\n")
print(story)