from . import gpt_2 as gpt2

# Set model to use: 124M, 335M or 774M
model_name = "124M"
# Download the model - should only need to run this once
# Saves the model in a 'models' folder
# gpt2.download_gpt2(model_name=model_name)

# Load the model to be used
sess = gpt2.start_tf_sess()

gpt2.load_gpt2(sess, model_name=model_name)


# Use GPT2 to generate text with a prefix
# Temperature, top_p etc has been set according to a tutorial that recommended those values


#target = the word we want to insert into the sentence

def generate_from_prob(sess,prompt,targets):
    for word in targets:
        print("before searching for " +word+ ":"+prompt)
        story = gpt2.generate(sess, prefix=prompt, length=20, model_name=model_name, return_as_list=True,
                      target=word, temperature=0.7, top_p=0.9, )
        prompt = story[0] + " " + word
        print("after searching for " +word+ ":"+prompt)
        story = gpt2.generate(sess, prefix=prompt, length=20, model_name=model_name, return_as_list=True,
                             temperature=0.7, top_p=0.9, )
        prompt = story[0]
    print(prompt)

generate_from_prob(sess, "Once upon a time, ", ["key", "shoe", "jewellery"])

#TODO
#We still need to create a endStory function that will take the prompt and continue generating until we get a fullstop
#We still need to create a function/adapt generate_from_prob to only return the newly generated text so we don't get to
#the point where we are constantly sending the whole story back and forth
