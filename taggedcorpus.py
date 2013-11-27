# coding= latin-1

# Eva Xiao
# tagged_corpus.py
# Reads in the Spanish Wikicorpus and creates a type:type dictionary.

from sys import argv
from preprocessing import *

# Flag 0 means that you want to build it from scratch by reading the tagged corpus. Flag 1 means that it is saved
# in a text file. 
def tag_dictionary(corpus_filename, flag = 0):
    f = open(corpus_filename, 'r')
    tag_dict = {}
    
    if flag == 1:
        for line in f:
            temp = line.split() 
            tag_dict[temp[0]] = temp[1]
        return tag_dict
    
    else:
        punctuation = [',', '.', '?', '-', '*', '!', ':', ';', '"', '%', '$', u'\u00bf', u'\u00a1']
        word_start = 1
        word_buffer = None
        i = 0
        
        for line in f:
            temp = line.split()
            for j in range(len(temp)):
                if (i % 2) == 0:
                    if not is_punctuation(temp[j], punctuation) and not is_word_number(temp[j]):
                        word_buffer = lowercase(temp[j])
                    else:
                        word_buffer = None
                elif (i % 2) != 0:
                    tag = standardize_tag(temp[j])
                    if (word_buffer not in tag_dict) and (word_buffer != None):
                        tag_dict[word_buffer] = tag
                i += 1
            i = 0
        
        return tag_dict  

# Write the tag dictionary to file. 
def save_tagged_dictionary(tag_dict, filepath):
    f = open(filepath, 'w')
    
    for key in tag_dict:
        line = str(key) + " " +  str(tag_dict.get(key)) + '\n'
        f.write(line)
    
    f.close()

# Removes tags, numbers, and unwanted punctuation from the tagged corpus. Flag 0 means you want it cleaned for word2vec to
# process; flag 1 means you want to keep end-of-sentence punctuation for transition probability processing.
def clean_tagged_corpus(corpus_filepath, cleaned_corpus_filepath, flag):
    f = open(corpus_filepath, 'r')
    new_f = open(cleaned_corpus_filepath, 'w')
    punctuation0 = [',', '-', '*', ':', ';', '"', '%', '$', u'\u00a1', u'\u00bf', '.', '?', '!']
    punctuation1 = [',', '-', '*', ':', ';', '"', '%', '$', u'\u00a1', u'\u00bf']
    EOS = ['.', '?', '!']
    i = 0
    
    for line in f:
        temp = line.split()
        for j in range(len(temp)):
            if (i % 2) == 0:
                word = temp[j]
                if flag == 1:
                    if word in EOS:
                        new_f.write(word + '\n')
                    else:
                        if not is_punctuation(word, punctuation1) and not is_word_number(word):
                            word = lowercase(word)
                            new_f.write(word + " ")
                elif flag == 0:
                    if not is_punctuation(temp[j], punctuation0) and not is_word_number(temp[j]):
                        word = lowercase(temp[j])
                        new_f.write(word + " ")
            i += 1
        i = 0
    
    f.close()
    new_f.close()
        
# Reads in a Parole tag and returns a "standard" (as defined below) tag
def standardize_tag(raw_tag):
    tag_codes = {"a":"ADJ", "r":"ADV", "d":"DET", "n":"N", "v":"V", "p":"PRO", "c":"C", "i":"I", "sp":"P"} 
    
    if str(raw_tag[0]) in tag_codes:
        tag = tag_codes.get(str(raw_tag[0]))
        return tag
    elif str(raw_tag[0:2]) == "sp":
        tag = tag_codes.get("sp")
        return tag
    else:
        return raw_tag

