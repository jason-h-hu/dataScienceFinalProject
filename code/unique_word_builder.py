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

shelfFile = 'data/prob_dict_shelf'


def build_text_field(restaurant):
	text_string = restaurant["yelp_review"]

	for review in restaurant["google_review_list"]:
		text_string = text_string+" "+review["review_text"]

	text_string = data_cleaning.clean(text_string)
	
	return text_string.split() if len(text_string)>1 else []



def determine_unique_words(rest_text, prob_dict):
	interesting_words_dict = defaultdict(lambda: 0.0)
	for word in rest_text:
		if word in prob_dict and prob_dict[word] != 0:
			interesting_words_dict[word] += (1/prob_dict[word])

	sorted_words = sorted(interesting_words_dict.items(), key=operator.itemgetter(1))
	unique_words =  sorted_words[:10]
	for i in range(len(unique_words)):
		unique_words[i] = unique_words[i][0]
	return unique_words


def build_words_entry(location_list):

	for restaurant in location_list:
		prob_dict = shelve.open(shelfFile)
		rest_text = build_text_field(restaurant)
		unique_words = determine_unique_words(rest_text, prob_dict)
		print "unique_words", unique_words
		restaurant["unique_words"] = unique_words

		prob_dict.close()

	return location_list



