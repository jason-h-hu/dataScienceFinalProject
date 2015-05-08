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

scores = {} # initialize an empty dictionary

def build_text_field(restaurant):
	text_string = restaurant["yelp_review"]

	for review in restaurant["google_review_list"]:
		text_string = text_string+" "+review["review_text"]

	text_string = data_cleaning.clean(text_string)
	
	return text_string.split() if len(text_string)>1 else []


def build_scores(sentiment_file):
	global scores
	for line in sentiment_file:
		term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
		scores[term] = float(score)      # Convert the score to a float.

def determine_sent(rest_text):
	sentiment_score = 0.0
	for word in rest_text:
		if word in score:
			sentiment_score += scores[word]

	return sentiment_score


def build_sent_entry(location_list, sentiment_file):
	sentiment_file = open("data/AFINN-111.txt")
	build_scores(sentiment_file)
	for restaurant in location_list:
		rest_text = build_text_field(restaurant)
 #sarah indented teh next two lines in
		sentiment = determine_sent(rest_text)
		restaurant["sentiment"] = sentiment

	return location_list



