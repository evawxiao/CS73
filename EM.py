# coding= latin-1
# Eva Xiao
# EM.py
# 11/24/2013

# The purpose of this file is to execute the Expectation Maximization algorithm to estimate just emission probabilities. 

from fwdmatrix import *
from bwdmatrix import *
from taggedcorpus import *
from calculate_probabilities import *
from preprocessing import *
from Viterbi_Beam import *
import copy
import math

# Uses Expectation Maximization to calculate emission probabilities 
def expectation_emission(fwd_matrix, bwd_matrix):
	emit_counts = {}
	obs_seq = fwd_matrix.obs_seq
	classes = fwd_matrix.classes
	
	for i in range(0, len(obs_seq)):
		for j in range(0, len(classes)):
			fwd_val = fwd_matrix.matrix[j][i]
			bwd_val = bwd_matrix.matrix[j][(len(obs_seq) - i) - 1]
			prob = (fwd_val * bwd_val)/fwd_matrix.total_probability
			if (obs_seq[i], classes[j]) in emit_counts:
				emit_counts[(obs_seq[i], classes[j])] += prob
			else:
				emit_counts[(obs_seq[i], classes[j])] = prob
	
	return normalize_counts(emit_counts, classes, 0)
	
# Uses Expectation Maximization to calculate transition probabilities. 
def expectation_transition(fwd_matrix, bwd_matrix):
	trans_counts = {}
	obs_seq = fwd_matrix.obs_seq
	classes = fwd_matrix.classes
	
	for i in range(0, len(obs_seq) - 1):
		for j in range(0, len(classes)):
			for k in range(0, len(classes)):
				if i == 0:
					if (classes[j], '#') not in trans_counts:
						fwd_val = fwd_matrix.matrix[j][0]
						bwd_val = bwd_matrix.matrix[j][len(obs_seq) - 1]
						prob = (fwd_val * bwd_val)/fwd_matrix.total_probability
						trans_counts[(classes[j], '#')] = prob
				fwd_trans_val = fwd_matrix.matrix[j][i] 
				bwd_trans_val = bwd_matrix.matrix[k][(len(obs_seq) - i) - 2]
				transition = float(fwd_matrix.trans_prob[(classes[k], classes[j])])
				emission = float(fwd_matrix.emit_prob[(obs_seq[i + 1], classes[k])])
				prob = (fwd_trans_val * bwd_trans_val * transition * emission)/float(fwd_matrix.total_probability)
				if (classes[k], classes[j]) in trans_counts:
					trans_counts[(classes[k], classes[j])] += prob
				else:
					trans_counts[(classes[k], classes[j])] = prob
	
	return (normalize_counts(trans_counts, classes, 1))

# flag = 0 means emission; flag = 1 means transition
def normalize_counts(prob_dict, classes, flag):
	totals = {}
	normalized = {}
	start_classes = copy.deepcopy(classes)
	start_classes.append('#')
	
	# Calculate total probability for each class
	for key in prob_dict:
		for i in range(0, len(start_classes)):
			if key[1] == start_classes[i]:
				if start_classes[i] in totals:
					totals[start_classes[i]] += prob_dict.get(key)
				else:
					totals[start_classes[i]] = prob_dict.get(key)
	
	
	# Normalize each probability with total probability 
	for key in prob_dict:
		total = totals.get(key[1])
		if total == 0:
			normalized[key] = 0.0
		else:
			prob = prob_dict.get(key)/float(total)
			normalized[key] = prob
		
	return normalized

# Iterates through expectation_transition() and expectation_maximization() until the log-likelihoods converge. Then, the
# final emission and transition probabilities are saved. 
def expectation_maximization(fwd_matrix, bwd_matrix,threshold = .01):
	old_LL = PWRS_TEN
	LL_buffer = PWRS_TEN
	new_LL = math.log(fwd_matrix.total_probability, 2)
	i = 1
	
	
	while math.fabs(old_LL - new_LL) > threshold and math.fabs(LL_buffer - new_LL) > threshold:
		if i % 3 == 0:
			LL_buffer = old_LL
		i += 1
		old_LL = new_LL

		# Incorporate new emission probabilities into fwd and bwd matrices
		emission_dict = expectation_emission(fwd_matrix, bwd_matrix)
		transition_dict = expectation_transition(fwd_matrix, bwd_matrix)
		
		classes_copy = copy.deepcopy(fwd_matrix.classes)
		obs_seq_copy = copy.deepcopy(fwd_matrix.obs_seq)
		fwd_new_matrix = fwdMatrix(transition_dict, emission_dict, classes_copy, obs_seq_copy)
		bwd_new_matrix = bwdMatrix(transition_dict, emission_dict, classes_copy, obs_seq_copy)	
		fwd_new_matrix.calculate_fwd_prob()
		bwd_new_matrix.calculate_bwd_prob()
		
		fwd_matrix.matrix = copy.deepcopy(fwd_new_matrix.matrix)
		bwd_matrix.matrix = copy.deepcopy(bwd_new_matrix.matrix)
		fwd_matrix.total_probability = copy.deepcopy(fwd_new_matrix.total_probability)
		bwd_matrix.total_probability = copy.deepcopy(bwd_new_matrix.total_probability)
		
		if fwd_matrix.total_probability == 0:
			break
		else:
			new_LL = math.log(fwd_matrix.total_probability, 2)
	write_to_file(emission_dict, "final_emissions.txt")
	write_to_file(transition_dict, "final_transitions.txt")

	return

# Save the new probabilities calculated by writing them to file. 
def write_to_file(prob_dict, emission_filepath):
	f = open(emission_filepath, 'w')
	for key in prob_dict:
			if key[0] != None:
				temp = str(key[1] + " " + key[0] + " " + str(prob_dict.get(key)) + '\n')
			f.write(temp)
			
	f.close()
	return 

# Goes through the process of creating the tag dictionary, initial transition and emission probabilities, finding what POS
# tags will serve as the classes, and splitting the observation sequence into a list of words before creating the forward and
# backward matricies. 
def prepare_emit_trans_files(observation_seq):
	tag_dict = tag_dictionary("tag_dictionary.txt", 1)
	transition_dict = transition_probabilities(tag_dict,"cleaned_cess.txt")
	#initialize_emission_prob(tag_dict, observation_seq) # if we don't want to use KNN to estimate initial emission probabilities
	#emission_dict = parse_prob_to_dict("initial_emissions.txt", 0)
	emission_dict = knn_initialize_emission(tag_dict, observation_seq)

	obs_seq = process_user_input(observation_seq)
	classes = POS_classes(tag_dict)

	fwd_matrix = fwdMatrix(transition_dict, emission_dict, classes, obs_seq)
	bwd_matrix = bwdMatrix(transition_dict, emission_dict, classes, obs_seq)

	fwd_matrix.calculate_fwd_prob()
	bwd_matrix.calculate_bwd_prob()
	
	return fwd_matrix, bwd_matrix
	

