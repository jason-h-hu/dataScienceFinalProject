"""
Unique Word Builder
Input: dictionary of restaurants for one location

restaurant = {coord:{lat:<float>,lng:<float>}, img_url:<str>, name:<string>, phone_num:<str>,
        address:<list<str>>, rest_url:<str>, num_yelp_reviews:<int>, dist_from_ll:<float>, yelp_review:<str>, 
        google_review_list:[{review_author:<str>,review_star:<float>,review_text:<str>},{},..], 
        google_star:<float>, yelp_star:<float>,google_place_id:<str>,yelp_id:<str>}


output: dictionary of restaurants for one location with an added "unique_words" field
"""

from collections import defaultdict
import data_cleaning
import shelve
import operator
import json

prob_dict_file = 'data/prob_dict'


def build_text_field(restaurant):
	text_string = []
	for line in restaurant:
		text_string += (data_cleaning.clean(line).split())
	
	return text_string if len(text_string)>1 else []



def determine_unique_words(rest_text, prob_dict):
	interesting_words_dict = defaultdict(lambda: 0.0)
	for word in rest_text:
		if word in prob_dict:
			interesting_words_dict[word] += 500 + (.01/prob_dict[word])

	sorted_words = sorted(interesting_words_dict.items(), key=operator.itemgetter(1), reverse = True)
	unique_words =  sorted_words[:10]
	for i in range(len(unique_words)):
		unique_words[i] = unique_words[i][0]
	return unique_words


def build_words_entry(rest_text):

	with open(prob_dict_file) as f:
		prob_dict = json.load(f)
		rest_text = build_text_field(rest_text)
		unique_words = determine_unique_words(rest_text, prob_dict)
		print unique_words



build_words_entry(open("louis.txt"))



