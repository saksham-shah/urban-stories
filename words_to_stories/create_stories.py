import gpt_2 as gpt2
import gpt2_utilities as util

# Set model to use: 124M, 335M or 774M
model_name = "124M"

# Download the model - should only need to run this once
# Saves the model in a 'models' folder
# gpt2.download_gpt2(model_name=model_name)

def load_model(model_name="124M"):
    # Load the model to be used
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, model_name=model_name)
    return sess

def generate_with_targets(sess, prompt, targets):
    for word in targets:
        print("before searching for " + word + ": " + prompt)
        prompt = util.generateSanitised(sess, prefix=prompt, length=20, target=word)
        
        print("after searching for " + word + ": " + prompt)
        prompt = util.generateSanitised(sess, prefix=prompt, length=20)
    print(prompt)

sess = load_model(model_name="124M")

generate_with_targets(sess, "Once upon a time, ", ["key", "shoe", "jewellery"])
