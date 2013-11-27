# Eva Xiao
# Viterbi_Beam.py
# 11/25/2013

# This file implements both the Viterbi algorithm and Beam Search. It iterates through a matrix of emission and transition
# probabilities and calculates the most probable tagging sequence, or in the case of Beam, the k most probable tagging sequences.

import math
from sys import argv
from preprocessing import *

# Calculates Viterbi probabilities in a matrix. 
def Viterbi_Beam_matrix(obs_seq, classes, emission_dict, transition_dict):
    # Convert observation sequence in file to a list of characters
    class_row = []
    
    # Copy list of all classes
    for pclass in classes:
        class_row.append(pclass)
        
    #Create lists to store probability values for each class
    for i in range(0, len(classes)):
        class_row[i] = []

    # Calculate values for all characters in observation sequence
    for i in range(0, len(obs_seq)):
        if i == 0: 
            # Calculate first cell for all classes
            for j in range(0, len(classes)):
                if ((obs_seq[i], classes[j]) in emission_dict) and ((classes[j], '#') in transition_dict):
                    trans_prob = float(transition_dict[(classes[j], '#')])
                    emis_prob = float(emission_dict[(obs_seq[i], classes[j])])
    
                    class_row[j].append(trans_prob * emis_prob)
                else:
                    class_row[j].append(None)
       
        else:
            # Calculate ith cell for all classes
            for j in range(0, len(classes)):
                possible_vals = []
                for k in range(0, len(classes)):
                    if ((obs_seq[i], classes[j]) in emission_dict) and ((classes[j], classes[k]) in transition_dict):
                        trans_prob = float(transition_dict[(classes[j], classes[k])])
                        emis_prob = float(emission_dict[(obs_seq[i], classes[j])])
                        if (class_row[k][i - 1] != None):
                            temp = class_row[k][i - 1] * trans_prob * emis_prob
                            possible_vals.append(temp)
                # Save maximum value in the matrix
                if (len(possible_vals) > 0):
                    cell_value = max(possible_vals)
                    class_row[j].append(cell_value)
                else:
                    class_row[j].append(None)
    
    return class_row

# Backtracks through the probability matrix and uses highest probabilities to determine Viterbi tagging
def Viterbi_backtrack(class_lists, classes, k):
    num_cells = len(class_lists[0]) - 1
    tag_seq_bckwrds= [] # a list of lists
    tag_seq = []
    
    # Find max value 
    for i in range(num_cells, -1, -1):
        k_POS = []
        cell_vals = []
        for j in range(0, len(class_lists)):
            cell_vals.append((class_lists[j][i], j))
        cell_vals.sort(cmp = None, key = None, reverse = True)
        for j in range(0, k):
            k_POS.append(classes[cell_vals[j][1]])
        tag_seq_bckwrds.append(k_POS)
        
    # Flip list
    for j in range(len(tag_seq_bckwrds) - 1, -1, -1):
        tag_seq.append(tag_seq_bckwrds[j])
    
    #print(tag_seq)
    return tag_seq

# Combines Viterbi_matrix() and Viterbi_backtrack() to compute the Viterbi tagging sequence of a given observation.
# If k is larger than 1, it returns k number of tagging sequences for a given observation. 
def Viterbi_Beam_Algorithm(observation, classes, emission_file, transition_file, k = 1):
    
    if k >= len(classes):
        print("K value too large. Aborted.")
        return
    # Parse probability files and save values into a dictionary
    trans_dict = parse_prob_to_dict(transition_file, 0)
    emis_dict = parse_prob_to_dict(emission_file, 0)
    final_tagging = ""
    
    # Create matrix with probability values, then calculate tag sequence by backtracking
    matrix = Viterbi_Beam_matrix(observation, classes, emis_dict, trans_dict)
    tag_seq = Viterbi_backtrack(matrix, classes, k)
    i = 0
    
    for word in observation:
            final_tagging += word + " (" + str(tag_seq[i]) + ") "
            i += 1

    return final_tagging

            
            