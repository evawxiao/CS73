# Eva XIao
# wordvector.py
# 11/25/2013

# This file contains the wordVector class, which stores information from word2vec files: the vector's word type,
# the vector values (the vectors in this project are all 25-D), the dimension of the vector, and the word type's POS tag(s).

import math

class wordVector:
    def __init__(self, word, vector_values):
        self.word = word
        self.vector_values = vector_values # a list of vector values
        self.dimension = len(vector_values)
        self.tags = None
    
    # Euclidean distance between this vector and another vector
    def distance(self, other_vector):
        sum = 0
        distance = 0
        
        if self.dimension != other_vector.dimension:
            print("ERROR: vector dimensions do not match.")
            return None 
        else:
            for i in range(len(self.vector_values)):
                temp = (float(self.vector_values[i]) - float(other_vector.vector_values[i])) ** 2.0
                sum += temp
            distance = math.sqrt(sum)
            
            return distance
    
    def __repr__(self):
        return str(self.word)

