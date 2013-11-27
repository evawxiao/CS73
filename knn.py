# coding= latin-1

# Eva Xiao
# knn.py
# 11/25/2013

# This file implements the K-Nearest-Neighbors algorithm to estimate x probable tags for a word using k neighbors. 

from taggedcorpus import *
from wordvector import wordVector
from preprocessing import convert_strange_symbols
import copy

# Searches through test corpora for unknown words - words not in the tagged corpus
def unknown_words(test_vectors, tag_dict):
    unknowns = []
    seen = {}
    
    for vector in test_vectors:
        if vector.word not in tag_dict and vector.word not in seen:
            if not is_word_number(vector.word):
                unknowns.append(vector.word)
                seen[vector.word] = 1
    
    return unknowns

# Saves vectors that represent unknown words in the test corpora
def unknown_word_vectors(untagged_vectors, unknown_words):
    unknown_vectors = [] # may have to change this to a dictionary
    seen = {}
    
    for vector in untagged_vectors:
        for word in unknown_words:
            if vector.word == word and vector.word not in seen:
                unknown_vectors.append(vector)
                seen[vector.word] = 1
    
    return unknown_vectors
            
# Creates a wordVector object using the information from a word2vec file
def create_word_vectors(vector_file, tag_dict):
    f = open(vector_file, 'r')
    f.readline(); f.readline() # skip </s> and word2vec file header
    line = f.readline()
    vectors = []
    
    # Read the file until EOF
    while len(line) > 0:
        temp = line.split()
        word = convert_strange_symbols(str(temp[0]))
        new_vector = wordVector(word, temp[1:])
        # If its POS tag is defined in our tag ictionary
        if (tag_dict.get(word)) != None:
            tag = []
            tag.append(tag_dict.get(word))
            new_vector.tags = tag
        vectors.append(new_vector)
        line = f.readline()
        
    f.close()
    return vectors

# Merge two lists of vectors into one
def merge_vector_files(vectors1, vectors2):
    merged = copy.deepcopy(vectors1)
    
    for vector in vectors2:
        merged.append(vector)
    
    return merged
        
# Finds the k most similar, or nearest, vectors using Euclidean distance
def neighbors(unknown_vector, known_vectors, k):
    distances = [] # tuples: (distance, vector)
    neighbors = []
    
    for vector in known_vectors:
        if vector.tags != None: # Don't want to use other unknown words to vote on POS tag
            d = unknown_vector.distance(vector)
            distances.append((d, vector))
    
    distances.sort(cmp=None, key=None, reverse=False) 
    
    # Make sure that the number of neighbors doesn't exceed the number of vectors
    if k > len(distances):
        for i in range(len(distances)):
                neighbors.append(distances[i][1])
    else:
        for i in range(k):
                neighbors.append(distances[i][1])
        
    return neighbors

# Using the vector's k neighbors, estimate l probable POS tags
def knn_vote(vector, k_neighbors, l):
    possible_tags = [] # tuples: (# of votes, POS tag)
    tags = []
    index = {} # keeps track of where POS tags that are in possible_tags list
    
    for neighbor in k_neighbors:
        # if the neighbor's POS tag has not been added to the vector's list of plausible tags
        if neighbor.tags[0] not in index:
            possible_tags.append((1, neighbor.tags[0]))
            index[neighbor.tags[0]] = len(possible_tags) - 1
        else:
            votes = (possible_tags[index.get(neighbor.tags[0])])[0] + 1 # add votes
            possible_tags[index.get(neighbor.tags[0])] = (votes, neighbor.tags[0])
    
    possible_tags.sort(cmp=None, key=None, reverse=True)
    
    # Pick the l most probable POS tags
    if l <= len(possible_tags):
        for i in range(0, l):
            tags.append(possible_tags[i][1])
    else:
        for i in range(0, len(possible_tags)):
            tags.append(possible_tags[i][1])
    
    return tags

# K-Nearest-Neighbor algorithm: ties together neighbors() and knn_vote() and estimates
# l probable POS tags for all test vectors using k neighbors
def knn(tag_dict, test_vectors, merged, k, l):
    calculated_tags = {} # word:[k tags]
    print("We need to estimate tags for " + str(len(test_vectors)) + " words")
    i = 0
    
    for vector in test_vectors:
        print(str(i) + "/" + str(len(test_vectors)))
        k_neighbors = neighbors(vector, merged, k) # calculate neighbors
        k_tags = knn_vote(vector, k_neighbors, l) # calculate tags
        calculated_tags[vector] = k_tags
        vector.tags = k_tags
        i += 1
    
    return calculated_tags

# write tag dictionary to a file -> use for EM/Viterbi
def save_tag_dict(full_tag_dict, filepath):
    f = open(filepath, 'w')
    
    for key in full_tag_dict:
        line = str(key) + ":" + str(full_tag_dict.get(key)) + '\n'
        f.write(line)
    
    f.close()

# Read text file with KNN estimated tags for words (file format described in save_tag_dict())
def read_knn_dict_file(knn_tag_filepath):
    f = open(knn_tag_filepath, 'r')
    knn_dict = {}
    
    for line in f:
        temp = line.split(':')
        knn_dict[temp[0]] = temp[1]
    
    return knn_dict

# Takes in a list of word2vec files and return s a list of wordVector objects. 
def create_all_vectors(tag_dict, vector_filepaths):
    all_vectors = []
    temp = []
    
    for i in range(len(vector_filepaths)): 
        vectors = create_word_vectors(vector_filepaths[i], tag_dict)
        temp.append(vectors)
        if i == 0:
            all_vectors = merge_vector_files(vectors, temp[0]) # merge first and second vectors
        elif i > 0:
            all_vectors = merge_vector_files(all_vectors, vectors) # merge all vectors with new vectors
    
    return all_vectors

# The driver that puts together wordVector creation and KNN. This function reads in word2vec files
# before converting them into wordVector objects. These wordVector objects are then used in KNN. 
# *Note: test_filepaths and all_vector_filepaths are lists of filepaths were word2vec files are contained
def main(k, l, tagged_corpus_filepath, test_filepaths, all_vector_filepaths):
    tag_dict = tag_dictionary(tagged_corpus_filepath)
    all_vectors = create_all_vectors(tag_dict, all_vector_filepaths)
    test_vectors = create_all_vectors(tag_dict, test_filepaths)
    
    print("All word vectors created! Now finding the untagged words...")
    mystery_words = unknown_words(test_vectors, tag_dict)
    untagged = unknown_word_vectors(all_vectors, mystery_words)
    
    print("Unknown words found! Using KNN to find k tag possibilities for unknown words...")
    new_tag_dict = knn(tag_dict, untagged, all_vectors, k, l)
    print(new_tag_dict)
    save_tag_dict(new_tag_dict, "knn_tag_dictionary.txt")
