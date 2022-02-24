import gpt_2 as gpt2


import requests
import random
# Set model to use: 124M, 335M or 774M
model_name = "124M"
# Download the model - should only need to run this once
# Saves the model in a 'models' folder
#gpt2.download_gpt2(model_name=model_name)

# Load the model to be used
sess = gpt2.start_tf_sess()

gpt2.load_gpt2(sess, model_name=model_name)

# Use GPT2 to generate text with a prefix
# Temperature, top_p etc has been set according to a tutorial that recommended those values


def generateWithPrefix(sess, prefix, length=100, include_prefix=True):
    return gpt2.generate(sess,
                         model_name=model_name,
                         prefix=prefix,
                         length=length,
                         temperature=0.7,
                         top_p=0.9,
                         include_prefix=include_prefix,
                         return_as_list=True
                         )[0]


# Get the part of speech of a word using Dictionary API
def getPartOfSpeech(word):
    result = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + word)

    if result.status_code != 200:
        return None

    json = result.json()
    return json[0]["meanings"][0]["partOfSpeech"]


# Find a word with a specific part of speech and replace it with a given word
# I will comment this better later just uploading to github rn
def replacePartOfSpeech(sentence, word, partOfSpeech):
    sentence += " "
    output = ""
    currentWord = ""
    for char in sentence:
        if char >= 'a' and char <= 'z':
            currentWord += char
        else:
            if (len(word) > 0):
                # end of word
                wordPartOfSpeech = getPartOfSpeech(currentWord)
                if (wordPartOfSpeech == partOfSpeech and random.uniform(0, 1) > 0.5):
                    output += word
                    return output
                else:
                    output += currentWord
                currentWord = ""
            output += char

    return None


# Insert a word into the sentence by replacing it with a word with a matching part of speech
def insertWordAndTruncate(sentence, word):
    # Get the part of speech of the word
    partOfSpeech = getPartOfSpeech(word)
    # Replace a word of that part of speech with the word
    return replacePartOfSpeech(sentence, word, partOfSpeech)


# Generate a sentence with a set of keywords
# I will comment this better later just uploading to github rn
def generateWithKeywords(sess, prefix, keywords):
    output = prefix
    for word in keywords:
        attempts = 0
        addition = None
        while (attempts < 5 and addition == None):
            print("Prefix: " + output)
            print("Word: " + word)
            generated = generateWithPrefix(sess, output, 20 + attempts * 10)
            print("Generated: " + generated)
            addition = insertWordAndTruncate(generated[len(output):], word)
            print("Truncated: " + str(addition))

            attempts += 1
        if (addition != None):
            output += addition

    output = generateWithPrefix(sess, output, 200)
    return output

story, index = gpt2.generate(sess, length=100, model_name=model_name, return_as_list=True, target="shoe",top_p=0.9)
print(story[0])
print(index)

story,index = gpt2.generate(sess, length=100, model_name=model_name, return_as_list=True, target="shoe",top_p=0.9)
print(story[0])
print(index)

story, index = gpt2.generate(sess, length=100, model_name=model_name, return_as_list=True, target="shoe",top_p=0.9)
print(story[0])
print(index)

story, index = gpt2.generate(sess, length=100, model_name=model_name, return_as_list=True, target="shoe",top_p=0.9)
print(story[0])
print(index)

story, index = gpt2.generate(sess, length=100, model_name=model_name, return_as_list=True, target="shoe",top_p=0.9)
print(story[0])
print(index)



