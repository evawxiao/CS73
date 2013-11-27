Documentation for Chilango Slang POS Tagger - by Eva Xiao

There are several directories in this repository:
* vector_ready_corpora
* vector_files
* observation_files
* corpora

vector_ready_corpora: simply includes processed text files from "corpora" that can be converted into word2vec fies

vector_files: word feature vectors, returned by word2vec from text files in vector_ready_corpora

observation_files: some test observation files that are Spanish text with chilango slang embedded in them (good for testing...especially people who don't speak Spanish/know any chilango slang). The sentences in the observation files are excerpts from rap lyrics from Mexico City artists MC Luka and Bocafloja, as well as facebook statuses from my friends in Mexico City. 

corpora: all the text files used for KNN training. Also includes the tagged corpus, which is called "cess.txt". Included in this folder are the subtitle files for two films: Y Tu Mama Tambien and Amores Perros, and rap lyrics from Mexico City music group Sociedad Cafe.

---------------------------------------------------------------------

PYTHON PROGRAM FILES:
The python files for this program can be organized into the following categories:
* preprocessing
* k-nearest-neighbors
* expectation-maximization
* viterbi/beam search
* program drivery

Preprocessing Python Files:
* lyriccorpus.py - A python file that reads in text files with lyrics in them and cleans them of punctuation and numbers.

* moviecorpus.py - A python file that reads in .srt files of Amores Perros and Y Tu Mama Tambien and cleans them of punctuation and numbers. 

* preprocessing.py - A python file that includes all helper functions for processing text: checking if a word or letter is a number, checking if a word or letter is punctuation, stripping words of punctuation and numbers, lowercasing words, parsing text files with probabilities saved to them into dictionaries

* taggedcorpus.py - A python file that reads in the tagged Spanish Wikicorpus (corpora/cess.txt) and creates a dictionary of words:tags. In addition, this file contains methods to clean the tagged Spanish Wikicorpus file by removing the Parole tags, punctuation, and numbers. Also includes methods to save the tag dictionary to a text file or to read in a text file where the tag dictionary is saved. 

---------------------------------------------------------------------

K-Nearest Neighbors Python Files:
* knn.py - A python file that implements the KNN algorithm. Includes helper functions that calculate k neighbors for a given word vector, and the class label that its neighbors vote on. In addition, the file includes methods to convert word2vec files into vectors, and methods that calculate what words lack tags in our entire corpus (or what words require KNN tag estimations)

---------------------------------------------------------------------

Expectation-Maximization Python Files:
* noisychannelmatrix.py - A python file that defines the noisyChannelMatrix class, which holds important instance variables for both forward and backward matrices: a matrix, emission and transition probabilities, and total probability. 

* bwdmatrix.py - A python file that defines the bwdMatrix object, which inherits the noisyChannelMatrix class. It defines a specific class method called "calculate_bwd_prob()" which calculates the backward probability of an observation sequence given transition and emission files. 

* EM.py - A python file that implements the Expectation-Maximization for an observation sequence. It includes functions that implement the Forward-Backward algorithm, normalize transition and emission counts, and save EM-calculated transition and emission probabilities to a text file.

* fwdmatrix.py - A python file that defines the fwdMatrix object, which inherits the noisyChannelMatrix class. It definse a specific class method called "calculate_fwd_prob()" which calculates the forward probability of an observation sequence given transition and emission files. 

---------------------------------------------------------------------
Viterbi/Beam Search Python Files

* Viterbi_Beam.py - A python files that implements both the Viterbi and Beam Search algorithm. It includes functions that create a matrix for Viterbi to store probabilities and a backtrack function that chooses the highest probability calculated during the Viterbi algorithm. 

---------------------------------------------------------------------

Main program

* driver.py

To use the program, you only have to specify the filepath of your observation sequence (a text file) and, if you're using Beam Search, what your k value is, or how many tags you want returned per word. 

In driver.py, there is a main() program. To operate the program, change the parameters for main. At the moment, it is automatically set to "main("observation_files/obs0"), which means that it is using the text file "obs0" in the observation_files directory as the 
observation sequence. 

---------------------------------------------------------------------

Tag Glossary:
ADJ- adjective
ADV- adverb
DET- determinant/article
N- noun
V- verb
PRO- pronoun
C- conjunction
I- interjection
P- preposition
Fe- " "
Fs- ...
W- word describing time/date
Zm- word describing a monetary amount

Zp- word describing a percentage



---------------------------------------------------------------------

Text files in the repository:

* cleaned_cess.txt - a version of the tagged Spanish Wikicorpus that is cleaned of tags, numbers, and punctuation

* tag_dictionary.txt - a dictionary of word type: POS tag written to file so that it doesn't have to be computer over and over again

* knn_tag_dictionary.txt - a dictionary of word type: POS tag(s) written to file from the KNN algorithm to be used during Expectation-Maximization