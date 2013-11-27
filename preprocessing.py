# coding= latin-1
# Eva Xiao
# preprocessing.py
# 11/25/2013

# This file contains helper functions to pre-process both test and training corpora. Preprocessing may include lowercasing
# words, removing numbers and punctuation, dealing with Spanish punctuation, checking if a word is a number or puncutation, etc.

# Converts a string to all lowercase letters and checks for Spanish punctuation
def lowercase(string):
    lc_string = ""
    DIFFERENCE = 32
    
    for char in string:
        if (ord(char) > 64 and ord(char) < 91):
            lc_string += chr(ord(char) + DIFFERENCE)
        elif (char == u"\u00BF") or (char == u"\u00A1"): # if inverted question or exclamation mark
            lc_string = lc_string
        else:
            lc_string += char
    
    return lc_string

# Returns True if the word is punctuation (Parole or normal); False if not
def is_punctuation(word, punct_list):
    Parole_punct = ["-Fpa-", "-Fpt-"] # refers to tag set in tagged corpus
    
    for punct in punct_list:
        if word == punct:
            return True
    
    for punct in Parole_punct:
        if word == punct:
            return True
    
    return False

# Returns True if the word is a number; False if not
def is_word_number(word):
    counter = 0
    
    for char in word:
        if (ord(char) >= 33 and ord(char) <= 64) or (ord(char) >= 91 and ord(char) <= 96) or (ord(char) >= 123 and ord(char) <= 126):
            counter += 1
    if counter == len(word):
        return True
    else:
        return False

# Returns True if letter is a number, false if not
def is_letter_number(letter):
    val = ord(letter)
    
    if val >= 48 and val <= 57:
        return True
    
    return False

# Removes punctuation from a word 
def strip_punct_and_numbers(word, punctuation):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for punct in punctuation:
        word = word.replace(punct, "")
    
    for number in numbers:
        word = word.replace(number, "")
        
    return word

# Opens the file that the user wants to use as the observation sequence and processes it into a list of words.
# All words in the list are lowercase and without punctuation or numbers.
def process_user_input(filepath):
    f = open(filepath, 'r')
    observation_words = []
    punctuation = [',', '.', '?', '-', '*', '!', ':', ';', '"', '%', '$', u'\u00bf', u'\u00a1']
    
    for line in f:
        if len(line) > 1:
            temp = line.split()
            for word in temp:
                if not is_word_number(word) and not is_punctuation(word, punctuation):
                    # Process
                    word = strip_punct_and_numbers(word, punctuation)
                    word = lowercase(word)
                    word = convert_strange_symbols(word)
                    if len(word) > 0:
                            observation_words.append(word)
    
    return observation_words

# Reads a file of probabilities (emission, transition, or tag)) and returns a dictionary.
# Flag 0 means it's an emission or transition probability  dictionary; 1 means it is the tag dictionary
def parse_prob_to_dict(filename, flag):
    f = open(filename, 'r')
    prob_dict = {}
    
    for line in f:
        temp = line.split() 
        # Parsing emission/transition probabilities
        if flag == 0:
            key = (temp[1], temp[0]) # key uses format: X|Y = (X, Y)
            val = temp[2] # val returns P(X| Y) 
        else:
            key = temp[0]
            val = temp[1]
        
        prob_dict[key] = val
    
    return prob_dict

# If UTF-8 encoding doesn't decode properly, convert the symbols into actual latin-1 symbols
def convert_strange_symbols(word):
    translation = {'Ã¡':'á', 'Ã©':'é','Ã­':'í','Ã³':'ó','Ãº':'ú', 'Ã±':'ñ'}
    formatted = ""
    i = 0
    
    while i < len(word):
        if i == len(word) - 1:
            formatted += word[i]
            i += 1
        elif word[i:i + 2] in translation:
            formatted += translation.get(word[i:i + 2])
            i += 2
        else:
            formatted += word[i]
            i += 1
    
    return formatted

    