# Eva Xiao
# bwdmatrix.py
# 11/24/2013

# The bwdMatrix class inherits the noisyChannelMatrix class and is able to calculate backward probabilities using the
# observation sequence, emission probability, and transition probability instance variables. 

from noisychannelmatrix import *
from sys import argv
from preprocessing import *
from calculate_probabilities import POS_classes

class bwdMatrix(noisyChannelMatrix):
    def __init__(self, *arg):
        noisyChannelMatrix.__init__(self, *arg)
        # Add one to first cell of every row
        for row in self.matrix:
            row.append(1)
            
    # Fill in matrix using transition and emission probabilities
    def calculate_bwd_prob(self):
        for i in range(len(self.obs_seq) - 1, -1, -1):
            curr_obs = self.obs_seq[i]
            if i == 0:
                cell_vals = []
                for j in range(0, len(self.classes)):
                    class1 = self.classes[j]
                    if ((class1, '#') in self.trans_prob) and ((curr_obs, class1) in self.emit_prob):
                        transition = float(self.trans_prob.get((class1, '#')))
                        emission = float(self.emit_prob.get((curr_obs, class1)))
                        prev = float(self.matrix[j][(len(self.obs_seq) - i) - 1])
                        val = PWRS_TEN * transition * emission * prev
                    else:
                        val = 0.0
                    cell_vals.append(val)
                total = sum(cell_vals)
                self.total_probability = total
            else:
                for j in range(0, len(self.classes)):
                    cell_vals = []
                    class1 = self.classes[j]
                    for k in range(0, len(self.classes)):
                        class2 = self.classes[k]
                        if ((class2, class1) in self.trans_prob) and ((curr_obs, class2) in self.emit_prob): 
                            transition = float(self.trans_prob.get((class2, class1)))
                            emission= float(self.emit_prob.get((curr_obs, class2)))
                            if i == (len(self.obs_seq) - 1):
                                val = PWRS_TEN * transition * emission
                            else:
                                prev = self.matrix[k][(len(self.obs_seq) - i) - 1]
                                val = PWRS_TEN * prev * transition * emission
                        else:
                            val = 0.0
                        cell_vals.append(val)
                    total = sum(cell_vals)
                    self.matrix[j].append(total)

        self.descale() # Return PWRS_TEN'd values to actual values

        return
    
    # Descales values in the matrix after backward multiplications in the matrix
    def descale(self):
        new_matrix = []

        for i in range(0, len(self.matrix)):
            temp = []
            new_matrix.append(temp)
            for j in range(0, len(self.matrix[i])):
                new_val = (self.matrix[i][j])
                # Avoid Overflow problems for large j values
                for k in range(0, j):
                    new_val = new_val * (1.0)/PWRS_TEN
                new_matrix[i].append(new_val)
        
        # Avoid Overflow problems for large (j + 1) values
        for i in range(0, j + 1): 
            self.total_probability = self.total_probability * (1.0)/PWRS_TEN
        self.matrix = new_matrix
        
        return

