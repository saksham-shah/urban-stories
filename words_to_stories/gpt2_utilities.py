import gpt_2 as gpt2

# Use GPT2 to generate text with a prefix
# Temperature, top_p etc has been set according to a tutorial that recommended those values
def generate(sess, prefix, length=20, target=None, model_name="124M"):
    generated = gpt2.generate(sess,
                model_name=model_name,
                prefix=prefix,
                length=length,
                temperature=0.7,
                top_p=0.9,
                return_as_list=True,
                target=target
                )[0]

    # If there is a target word, add it to the generated text
    if target is not None:
        generated += ' ' + target

    # Don't include the prefix when returning    
    return generated[len(prefix):]

# Removes new lines and double spaces
# Returns None if the sentence has any invalid characters
def sanitise(sentence):
    # Returns True if the character is valid
    # TODO: Should we allow speech marks or not?
    #       They mess with ending a sentence on a full stop so I haven't for now.
    validChars = ".,!-':;"
    def charIsValid(char):
        return (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z') or char in validChars

    output = ""

    for char in sentence:
        if charIsValid(char):
            output += char

        # Replace new lines with a space
        elif char == '\n' and (len(output) == 0 or output[-1] != ' '):
            if (len(output) > 0 and output[-1] not in validChars):
                # If the last character is a letter, add a full stop
                output += '.'
            output += ' '

        # Remove multiple spaces in a row
        elif char == ' ' and (len(output) == 0 or output[-1] != ' '):
            output += ' '
        else:
            return None
    
    return output

# Generates sanitised text
def generateSanitised(sess, prefix, length=20, target=None, include_prefix=True, model_name="124M"):
    attempts = 0
    # Repeatedly generate text until you get one that is valid (or you keep failing)
    while (attempts < 5):
        output = generate(sess, prefix, length=length, target=target, model_name=model_name)
        output = sanitise(output)
        if output is not None:
            # Add the prefix to the generated output if needed
            if include_prefix:
                output = prefix + output
            return output
        attempts += 1
        print("Failed attempt " + str(attempts))
    
    return None

# Generates text up to the first full stop
def generateEnd(sess, prefix, length=20, model_name="124M"):
    # Truncates a sentence up to the first full stop (if there is one)
    def truncateByFullStop(sentence):
        index = sentence.find('.')
        if index == -1:
            return None
        return sentence[:index + 1]

    # Repeatedly generate text until you get one with a full stop
    attempts = 0
    while (attempts < 5):
        # Don't include prefix as we don't want to truncate the prefix, just the newly generated text
        output = generateSanitised(sess, prefix, length=length + 10*attempts, include_prefix=False, model_name=model_name)
        
        # If the output is None, GPT2 is stuck in a loop of using invalid characters
        # Return None to abandon this generation
        if output is None:
            return None

        output = truncateByFullStop(output)
        if output is not None:
            # Add the prefix back
            return prefix + output
        attempts += 1
    
    return None