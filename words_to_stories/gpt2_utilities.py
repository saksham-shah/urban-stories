from . import gpt_2 as gpt2

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
        # Capilatise target word if it follows the end of a sentence
        if generated[-1] in ".!":
            target = target.capitalize()

        generated += ' ' + target

    # Don't include the prefix when returning    
    return generated[len(prefix):]

# Removes new lines and double spaces
# Returns None if the sentence has any invalid characters
# If return_none is False, instead of returning None it just removes invalid characters
def sanitise(sentence, return_none=True):
    # Returns True if the character is valid
    valid_chars = ".,!-':;"
    def char_is_valid(char):
        return (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z') or (char >= '0' and char <= '9') or char in valid_chars

    output = ""

    for char in sentence:
        if char_is_valid(char):
            output += char

        # Replace new lines with a space
        elif char == '\n' and (len(output) == 0 or output[-1] != ' '):
            if (len(output) > 0 and output[-1] not in valid_chars):
                # If the last character is a letter, add a full stop
                output += '.'
            output += ' '

        # Remove multiple spaces in a row
        elif char == ' ' and (len(output) == 0 or output[-1] != ' '):
            output += ' '
        elif return_none:
            return None
    
    return output

# Generates sanitised text
def generate_sanitised(sess, prefix, length=20, target=None, include_prefix=True, model_name="124M", return_none=True):
    # Generate text and sanitise it
    output = generate(sess, prefix, length=length, target=target, model_name=model_name)
    output = sanitise(output, return_none=return_none)

    # If output is None, it was invalid so return None to skip this word
    # This never happens if return_none is False
    if output is None:
        return None

    # Add the prefix to the generated output if needed
    if include_prefix:
        output = prefix + output

    return output

# Generates text up to the first full stop
def generate_end(sess, prefix, length=20, model_name="124M"):
    # Truncates a sentence up to the first full stop (if there is one)
    def truncate_by_full_stop(sentence):
        index = sentence.find('.')
        if index == -1:
            return None
        return sentence[:index + 1]

    # Truncates a sentence up to the last full stop (if there is one)
    def truncate_by_last_full_stop(sentence):
        for i in range(len(sentence) - 1, 0, -1):
            if (sentence[i] == '.'):
                return sentence[:i + 1]
        
        return sentence

    # Repeatedly generate text until you get one with a full stop
    attempts = 0
    while (attempts < 5):
        # Don't include prefix as we don't want to truncate the prefix, just the newly generated text
        # return_none is False as we want to make sure we get an output
        output = generate_sanitised(sess, prefix, length=length + 10*attempts, include_prefix=False, model_name=model_name, return_none=False)

        output = truncate_by_full_stop(output)

        # If the output has been truncated correctly, return it
        if output is not None:
            # Add the prefix back
            return prefix + output

        attempts += 1
    
    # If there is still no full stop after 5 attempts, truncate the current text to the last full stop
    return truncate_by_last_full_stop(prefix)