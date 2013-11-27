# coding= latin-1
# Eva Xiao
# moviecorpus.py
# 11/23/2013

# The purpose of this file is to clean the subtitle files of "Amores Perros" and "Y Tu Mama Tambien." The end result are files
# without punctuation or numbers and can be converted into word2vec files. 

import string
import re
import copy
from sys import argv
from preprocessing import *

# Cleans the .srt file of "Y Tu Mama Tambien"
def clean_y_tu_mama_tambien(corpus_filepath, cleaned_corpus_filepath):
    f = open(corpus_filepath, 'r')
    new_f = open(cleaned_corpus_filepath, 'w')
    punct_list = ['-', '"', ',', '.', '?', '!']
    for line in f:
        if len(line) > 1:
            temp = line.split()
            if not is_letter_number(temp[0][0]):
                for word in temp:
                    word = strip_punct_and_numbers(word, punct_list) # can change this if punctuation doesn't matter
                    word = lowercase(word)
                    if len(word) > 0:
                        new_f.write(word + " ")
    
    f.close()
    new_f.close()

# Converts a corpus into a dictionary, word type:token
def corpora_to_dictionary(corpora_filename):
    f = open(corpora_filename, 'r')
    corpora_dict = {}
    
    for line in f:
        temp = line.split()
        for word in temp:
            if word not in corpora_dict:
                corpora_dict[word] = 1
            elif word in corpora_dict:
                corpora_dict[word] = corpora_dict.get(word) + 1
                
    return corpora_dict

# Cleans the .srt file of "Amores Perros"
def clean_amores_perros(corpus_filepath, cleaned_corpus_filepath):
    f = open(corpus_filepath, 'r')
    new_f = open(cleaned_corpus_filepath, 'w')
    punct_list = ['-', '"', ',', '.', '?', '!']
    
    for line in f:
        if len(line) > 1:
            line = clean_ap_line(line)
            temp = re.split(r'[| \n ]', line)
            for word in temp:
                if len(word) > 0 and not is_letter_number(word[0]):
                    word = strip_punct_and_numbers(word, punct_list)
                    word = lowercase(word)
                    if len(word) > 0:
                        new_f.write(word + " ")
    
    f.close()
    new_f.close()
    
# Removes the {numbers}{numbers} at the beginning of the line in Amores Perros' .srt file 
def clean_ap_line(string):
    copied = copy.deepcopy(string)

    if ord(copied[0]) == 123:
        i = 1
        while ord(copied[i]) != 125:
            i += 1
        i += 1
        while ord(copied[i]) != 125:
            i += 1
        copied = copied[i + 1:]
    
    return copied
