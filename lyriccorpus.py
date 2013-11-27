# coding= latin-1
from taggedcorpus import is_number
from sys import argv

def clean_lyric_file(filepath, file):
    f = open(filepath, 'r')
    new_f = open(str(file) + ".txt", 'w')
    
    for line in f:
        if len(line) > 1:
            temp = line.split()
            for word in temp:
                if not is_number(word):
                    word = remove_punct(word)
                    new_f.write(word + " ")
    
    f.close()
    new_f.close()

# Check if the word is punctuation OR a word with punctuation attached to it
def remove_punct(word):
    clean_word = ""
    special_chars = [u'\u00a1', u'\u00bf']
    
    for i in range(len(word)):
        c = word[i]
        if (ord(c) >= 33 and ord(c) <= 47) or (ord(c) >= 91 and ord(c) <= 94) or (ord(c) >= 123 and ord(c) <= 126) or (ord(c) >= 58 and ord(c) <= 64):
            clean_word += ""
        elif (c in special_chars) and (i == 0):
            clean_word += ""
        else:
            clean_word += c
    
    return clean_word
