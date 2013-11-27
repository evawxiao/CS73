# coding= latin-1

# Eva Xiao
# calculate_probabilities.py
# 11/24/2013

# The purpose of this file is to determine initial transition and emission probabilities. 

from knn import read_knn_dict_file
from preprocessing import *
from taggedcorpus import tag_dictionary
import copy

# Finds the counts of different POS tag transitions using the tag dictionary and the "cess.txt" corpus cleaned of tags and numbers
def transition_counts(tag_dict, clean_corpus):
    transition_counts = {} #(tag, tag): probability
    f = open(clean_corpus, 'r')
    EOF = ['.', '!', '?']
    
    # Count POS tag transitions
    for line in f:
        if len(line) > 1:
            temp = line.split()
            for i in range(0, len(temp) - 1):
                if (tag_dict.get(temp[i]) != None) and  (tag_dict.get(temp[i + 1]) != None):	
                    #P(N|ADJ) -> (N, ADJ)
                    key = (tag_dict.get(temp[i + 1]), tag_dict.get(temp[i])) # tuple ('tag', 'tag')
                    if key not in transition_counts:
                        transition_counts[key] = 1
                    else:
                        transition_counts[key] = transition_counts.get(key) + 1
                if i == 0:
                    key = (tag_dict.get(temp[i]), '#')
                    if key not in transition_counts:
                        transition_counts[key] = 1
                    else:
                        transition_counts[key] = transition_counts.get(key) + 1
    
    f.close()
    transition_counts = unknown_transition_counts(transition_counts, tag_dict)
    
    return transition_counts

# Gives us the different classes we need to consider in fwd and bwd matrix using POS tags from the tagged corpus
def POS_classes(tag_dict):
    classes = []
    
    for key in tag_dict:
        tag = tag_dict.get(key)
        if tag not in classes:
            classes.append(tag)
    
    return classes

# Gives POS transition probabilities a low probability if they are not present in our tagged corpus
def unknown_transition_counts(counts_dict, tag_dict):
    classes = POS_classes(tag_dict)
    full_counts_dict = copy.deepcopy(counts_dict)

    for i in range(len(classes)):
        start_key = (classes[i], '#')
        if (start_key not in counts_dict) and (start_key not in full_counts_dict):
            full_counts_dict[start_key] = 0.0001
        for j in range(len(classes)):
            key = (classes[j], classes[i]) 
            if (key not in counts_dict) and (key not in full_counts_dict):
                full_counts_dict[key] = 0.0001

    return full_counts_dict

# Go through a dictionary of counts and calculate the total
def sum_counts(count_dict):
    total = 0
    
    for key in count_dict:
        total += count_dict.get(key)
        
    return total

# Use the total count to normalize count dictionary into a probability dictionary
def transition_probabilities(tag_dict, clean_corpus): # need to change 
    count_dict = transition_counts(tag_dict, clean_corpus)
    total = sum_counts(count_dict)
    transition_prob = {}
    
    for key in count_dict:
        prob = float(count_dict.get(key))/float(total)
        transition_prob[key] = prob
    
    return transition_prob

# Write probability dictionary to file
def save_probabilities(prob_dict, filepath):
    f = open(filepath, 'w')
    
    for key in prob_dict:
        line = str(key[0]) + " " + str(key[1]) + " " +  str(prob_dict.get(key)) + '\n'
        f.write(line)
    
    f.close()

# Calculate initial emission probabilities for observation sequence (without KNN) 
def initialize_emission_prob(tag_dict, obs_seq_file):
    classes = POS_classes(tag_dict)
    obs_dict = process_user_input(obs_seq_file)
    f = open("initial_emissions.txt", 'w')
    vocab = {}
    
    for word in obs_dict:
        if word in vocab:
            vocab[word] += 1
        else:
            vocab[word] = 1
    for pos in classes:
        total = len(vocab)
        for word in vocab:
            prob = 1.0/float(total)
            temp = str(str(pos) + " " + str(word) + " " + str(prob) + '\n') #P(word|tag)
            f.write(temp)
    
    f.close()

# Calculate initial emission probabilities for observation sequence using KNN estimations
def knn_initialize_emission(tag_dict, obs_seq_file):
    classes = POS_classes(tag_dict)
    obs_dict = process_user_input(obs_seq_file)
    knn_tag_dict = read_knn_dict_file("knn_tag_dictionary.txt")
    prob_dict = {}
    unknown = []
    
    for tag in classes:
        for word in obs_dict:
            key = (word, tag)
            if word in tag_dict and key not in prob_dict:
                correct_tag = tag_dict.get(word)
                if key[1] == correct_tag:
                    prob_dict[key] = 1.0
                else:
                    prob_dict[key] = 0.0001
            elif word in knn_tag_dict and key not in prob_dict:
                total = len(knn_tag_dict.get(word))
                if key[1] in knn_tag_dict.get(word):
                    prob_dict[key] = 1.0/float(total)
                else:
                    prob_dict[key] = 0.0001
            else:
                if key not in prob_dict:
                    unknown.append(word)

        for tag in classes:
            total = len(unknown)
            for word in unknown:
                key = (word, tag)
                prob = 1.0/float(total)
                prob_dict[key] = prob

    return prob_dict
