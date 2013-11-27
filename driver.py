# coding= latin-1
# Eva Xiao
# driver.py
# 11/25/2013

# This file runs the POS tagging of chilango slang program. It takes the tags from a tagged Spanish Wikicorpus and an observation
# sequence stored in a file and calculates the most probable emission and transition probabilities using Expectation Maximization.
# Then, it tags the sequence with POS tags using the Viterbi or Beam algorithm. 

from sys import argv
from EM import *
from Viterbi_Beam import *

# *NOTE*: the commented out command line prompt does not work with latin encoding...accent marks and spanish punctuation
# causes errors. 
'''
if __name__ == '__main__':
    if len(argv) < 2: raise Exception('Command syntax: python driver.py observation_seq k = 1') 
    else:
        print("Calculating forward and backward probabilities...")
        fwd_matrix, bwd_matrix = prepare_emit_trans_files(argv[1])
        
        print("Calculating emission and transition probabilities using Expectation Maximization...")
        expectation_maximization(fwd_matrix, bwd_matrix)
        
        print("Tagging observation sequence with Viterbi or Beam...")
        obs_seq = process_user_input(argv[1])
        tag_dict = tag_dictionary("tag_dictionary.txt", 1)
        classes = POS_classes(tag_dict)
        
        # Beam 
        if len(argv) > 2:
            final_tagging = Viterbi_Beam_Algorithm(obs_seq, classes, "final_emissions.txt", "final_transitions.txt", int(argv[2])) 
        # Viterbi
        else:
            final_tagging = Viterbi_Beam_Algorithm(obs_seq, classes, "final_emissions.txt", "final_transitions.txt") 
            
        print(final_tagging)

'''
def main(observation_seq, k = 1):
    print("Calculating forward and backward probabilities...")
    fwd_matrix, bwd_matrix = prepare_emit_trans_files(observation_seq)
    
    print("Calculating emission and transition probabilities using Expectation Maximization...")
    expectation_maximization(fwd_matrix, bwd_matrix)
    
    print("Tagging observation sequence with Viterbi or Beam...")
    obs_seq = process_user_input(observation_seq)
    tag_dict = tag_dictionary("tag_dictionary.txt", 1)
    classes = POS_classes(tag_dict)

    final_tagging = Viterbi_Beam_Algorithm(obs_seq, classes, "final_emissions.txt", "final_transitions.txt", k) 
        
    print(final_tagging)
    
main("observation_files/obs5", 3)