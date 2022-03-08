from . import gpt_2 as gpt2
from . import gpt2_utilities as util

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
def generate_with_targets(sess, prompt, targets):
    story = prompt
    words_used = 0
    skipped_words = []

    # Keep adding words until three words are added, or all words have been used up (skipped)
    while words_used < 3 and len(targets) > 0:
        word = targets.pop(0)

        # Insert the word into the story
        print("before searching for " + word + ": " + story)
        story_with_word = util.generate_sanitised(sess, prefix=story, length=20, target=word, model_name=model_name)

        # If the word has been inserted, continue the story a bit
        if story_with_word is not None:
            print("after searching for " + word + ": " + story_with_word)
            story_with_word = util.generate_sanitised(sess, prefix=story_with_word, length=20, model_name=model_name)

        # If the story is still valid, mark this word as added
        if story_with_word is not None:
            story = story_with_word
            words_used += 1

            # Add all skipped words back as they may work now
            targets = skipped_words + targets
            skipped_words = []
        else:
            # Otherwise, skip this word and move to the next one
            print("Skipped word: " + word)
            # Store skipped words to be reused later
            skipped_words.append(word)

    # Finish off the story with a full stop
    # generate_end never returns None so this will always successfully return a story
    return util.generate_end(sess, prefix=story, length=20, model_name=model_name)

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

    # Generate the story
    story = generate_with_targets(sess, prompt, targets)

    # Remove the prefix from the generated story
    if prefix is not None:
        story = story[len(prefix):]
    
    return story

sess = load_model(model_name="124M")
"""""
story = generate_story(sess, prompt="Once upon a time,", targets=["post office", "William Gates Building", "cinema", "jewellery", "computer", "groceries", "park", "school", "academia"], prefix="Here is a short story for young children:\n\n")
print(story)
"""""