# Eva Xiao
# noisychannelmatrix.py
# 11/24/2013

# This class defines the basic instance variables for both forward and backward probability matrices:
# * emission probabilities
# * transition probabilities
# * classes (in this case, POS tags will be used)
# * the observation sequence
# * a matrix to store probabilties calculated for the observation sequence 

import math

PWRS_TEN = 1000.0

class noisyChannelMatrix:
    # init_trans is a dictionary of initial transition probabilities. Likewise for init_emit
    def __init__(self, init_trans, init_emit, classes, observation_seq):
        self.trans_prob = init_trans
        self.emit_prob = init_emit
        self.classes = classes # POS in our case
        self.obs_seq = observation_seq # a list of words
        self.matrix = self.build_empty_matrix()
        self.total_probability = None
    
    # Matrix has classes as rows, observation sequence words as columns
    def build_empty_matrix(self):
        num_col = len(self.obs_seq)
        num_row = len(self.classes)
        matrix = []
        
        # Give each row in matrix a list (for columns)
        for clss in self.classes:
            class_row = [] 
            matrix.append(class_row)
            
        return matrix

    def __str__(self):
        return str(self.obs_seq)
        
    
