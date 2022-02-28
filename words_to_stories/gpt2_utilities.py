# Use GPT2 to generate text with a prefix
# Temperature, top_p etc has been set according to a tutorial that recommended those values
def generate(sess, prefix, length=20, target=None):
    generated = gpt2.generate(sess,
                model_name=model_name,
                prefix=prefix,
                length=length,
                temperature=0.7,
                top_p=0.9,
                return_as_list=True,
                target=target
                )[0]

    if (target is not None):
        generated += ' ' + word
    
    return generated

# Removes new lines and double spaces
# Returns None if the sentences has any invalid characters
def sanitise(sentence):
    def charIsValid(char):
        return (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z') or char in ".,!-'"

    output = ""

    for char in sentence:
        if charIsValid(char):
            output += char
        elif char == '\n' and output[-1] != ' ':
            output += ' '
        elif char == ' ' and output[-1] != ' ':
            output += ' '
    
    return output

# Generates sanitised text
def generateSanitised(sess, prefix, length=20, target=None):
    attempts = 0
    # Repeatedly generate text until you get one that is valid
    while (attempts < 5):
        output = generate(sess, prefix, length=length, target=target)
        output = sanitise(output)
        if output is not None:
            return output
        attempts += 1
    
    return None

# Generates text up to the first full stop
def generateEnd(sess, prefix, length=20):
    # Truncates a sentence up to the first full stop (if there is one)
    def truncateByFullStop(sentence):
        index = sentence.find('.')
        if index == -1:
            return None
        return sentence[:index + 1]

    # Repeatedly generate text until you get one with a full stop
    attempts = 0
    while (attempts < 5):
        output = generateValidated(sess, prefix, length=length + 10*attempts, target=target)
        output = truncateByFullStop(output)
        if output is not None
            return output
        attempts += 1
    
    return None