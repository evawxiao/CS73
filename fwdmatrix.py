# Eva Xiao
# fwdmatrix.py
# 11/24/2013

# The fwdMatrix class inherits the noisyChannelMatrix class and is able to calculate forward probabilities using the
# observation sequence, emission probability, and transition probability instance variables. 

from noisychannelmatrix import *
from preprocessing import *
from sys import argv
from calculate_probabilities import POS_classes

class fwdMatrix(noisyChannelMatrix):
    def __init__(self, *arg):
        noisyChannelMatrix.__init__(self, *arg)
    
    def calculate_fwd_prob(self):
        for i in range(len(self.obs_seq)):
            curr_obs = self.obs_seq[i]
            if i == 0:
                for j in range(len(self.classes)):
                    class1 = self.classes[j]
               	    #if (POS| #) in transition dictionary and (POS|word) in emission dictionary
                    if ((class1, '#') in self.trans_prob) and ((curr_obs, class1) in self.emit_prob):
                        transition = self.trans_prob.get((class1, '#'))
                        emission = self.emit_prob.get((curr_obs, class1))
                        val = PWRS_TEN * float(transition) * float(emission)
                    else:
                        val = 0.0
                    self.matrix[j].append(val) 

            else:
                for j in range(len(self.classes)):
                    cell_vals = []
                    class1 = self.classes[j]
                    for k in range(len(self.classes)):
                        class2 = self.classes[k]
                        if ((class1, class2) in self.trans_prob) and ((curr_obs, class1) in self.emit_prob):
                            transition = self.trans_prob.get((class1, class2))
                            emission = self.emit_prob.get((curr_obs, class1))
                            prev = self.matrix[k][i - 1]
                            val = float(prev) * float(transition) * float(emission) * PWRS_TEN
                        else:
                            val = 0.0
                        cell_vals.append(val)
                    total = sum(cell_vals)
                    self.matrix[j].append(total)

        # descale the matrix!
        self.descale()
        self.total_prob()

        return self.matrix
    
    # Descales values in the matrix after forward or backward multiplications in the matrix
    def descale(self):
        new_matrix = []

        for i in range(0, len(self.matrix)):
            temp = []
            new_matrix.append(temp)
            for j in range(0, len(self.matrix[i])):
                new_val = (self.matrix[i][j])
                for k in range(0, j + 1): 
                    new_val = new_val * (1.0/PWRS_TEN)
                new_matrix[i].append(new_val)

        self.matrix = new_matrix
        
        return
    
    # Calculate total probability by adding all forward probabilities in the last column
    def total_prob(self):
        total_prob = 0.0
        last_cell = len(self.matrix[0]) - 1 # index of last cell
    
        # Calculate the sum of all class probabilities in the last cell
        for clss in self.matrix:
            total_prob += clss[last_cell]
        
        self.total_probability = total_prob
        return 
