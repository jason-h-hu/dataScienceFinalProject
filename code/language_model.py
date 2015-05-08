"""
unique words python
input: corpus file of restaurant reviews
output: dictionary of words and their probabilities

This smooths for unknown words by taking all words that appear less than 4 times 
and changing them to "*UNK*", then finding a probability for "*UNK*"
  
"""

import sys
import math
from collections import defaultdict
import json


prob_dict = defaultdict(lambda:0.0)
word_dict = defaultdict(lambda:0.0)
word_count = 0.0


"""
Input: a file name to count the words of
Output: None.
Populates global word count with words as keys and number of occurences as value
"""

def word_count(input_file):
        global word_dict
        global word_count
        counter = 0
        #Goes through lines of file, adding them to dictionary
        for line in input_file:
            #Goes through lines and adds a start and stop character
            line_arr = line.split()
            line_arr.insert(0, ">>")
            line_arr.append("<<")
            
            for word in line_arr: 
            # Counts words and updates dictionary
                counter += 1
                word_dict[word] += 1
                
        word_count = counter
        # Close file
        input_file.close()



"""
set_prob

Input: Alpha, a parameter for smoothing unigram probabilities
Output: None
Populates global prop_dict with the smoothed probabilities for all single words
"""
def set_prob():
    global word_dict
    global prob_dict
    
    divisor =word_count

    for word in word_dict:
        #sets the probability of each word to the frequency of word 
        # divided by the total word count
        theta_w = word_dict[word]/divisor
        prob_dict[word] = theta_w
"""
clean_prob

Goes through and makes all words that appear less than 3 times *UNK*

"""

def clean_words():
    global word_dict
    for word in word_dict.keys():
        if (word_dict[word] <= 600 or word_dict[word] >= 65000):
            #word_dict["*UNK*"] += word_dict[word]
            del word_dict[word]


def main(argv):
    # Checks 
    if len(argv) != 2:
        print "Please enter input file."
    else:
        training = open(argv[1])

        #necessary set up to populat global variables
        #if data is changed, these functions must be re-run
        word_count(training)
        clean_words()
        set_prob()
        with open('data/prob_dict', 'w') as f:
            json.dump(prob_dict, f)

if __name__ == "__main__":
    main(sys.argv)
