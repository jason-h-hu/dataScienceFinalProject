"""
Data Cleaning 
This file takes in a file of various reviews from Yelp to turn into a corpus of cleaned restaurant reviews.
To do this, it also takes a fules of Yelp businesses and checks that reviews
correspond to a business in the restaurant category.

Input: 
	yelp_academic_dataset_reviews.json 
	yelp_academic_dataset_business.json
Output:
	cleaned reviews, that should then be redirected to another file

Use: 
	python data_cleaning.py yelp_academic_dataset_reviews.json yelp_academic_dataset_business.json > just_reviews.txt
"""

import sys
import json
from collections import defaultdict
from porter_stemmer import PorterStemmer
import re
import string as str

bus_dict = defaultdict(lambda :False)
stop_list = ['all', 'whys', 'being', 'over', 'isnt', 'through', 'yourselves', 'its', 'before', 'wed', 'with', 'had', 'should', 'to', 'lets', 'under', 'ours', 'has', 'ought', 'do', 'them', 'his', 'very', 'cannot', 'they', 'werent', 'not', 'during', 'yourself', 'him', 'nor', 'wont', 'did', 'theyre', 'this', 'she', 'each', 'havent', 'where', 'shed', 'because', 'doing', 'theirs', 'some', 'whens', 'up', 'are', 'further', 'ourselves', 'out', 'what', 'for', 'heres', 'while', 'does', 'above', 'between', 'youll', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'both', 'about', 'would', 'wouldnt', 'didnt', 'ill', 'against', 'arent', 'youve', 'theres', 'or', 'thats', 'weve', 'own', 'whats', 'dont', 'into', 'youd', 'whom', 'down', 'doesnt', 'theyd', 'couldnt', 'your', 'from', 'her', 'hes', 'there', 'only', 'been', 'whos', 'hed', 'few', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'on', 'but', 'you', 'hadnt', 'shant', 'mustnt', 'herself', 'than', 'those', 'he', 'me', 'myself', 'theyve', 'these', 'cant', 'below', 'of', 'my', 'could', 'shes', 'and', 'ive', 'then', 'wasnt', 'is', 'am', 'it', 'an', 'as', 'itself', 'im', 'at', 'have', 'in', 'id', 'if', 'again', 'hasnt', 'theyll', 'no', 'that', 'when', 'same', 'any', 'how', 'other', 'which', 'shell', 'shouldnt', 'our', 'after', 'most', 'such', 'why', 'wheres', 'a', 'hows', 'off', 'i', 'youre', 'well', 'yours', 'their', 'so', 'the', 'having', 'once']


def pre_clean(review_file):
	for line in review_file:
		obj = json.loads(line)
		review = obj["text"] 
		bus_id = obj["business_id"] 
		if bus_id in bus_dict:
			clean(review)
"""
clean
input: string to clean
output: string of cleaned
"""

def clean(review):
	review.replace("-", " ")
	review = review.lower().strip().encode('utf-8').split()
	out_review = []

	for word in review:
		if not word[0].isalpha(): #skip words that start with numbers
			continue
		
		elif "www" in word or"http" in word: #replace URLs
			word = "*URL*"
		elif word[0] == "@": #replace at mentions
			word = "AT_USER"
		elif word[0]=="#":
			word = word[1:]
		word = re.sub(r'(.)\1+', r'\1\1', word)
		word = word.translate(str.maketrans("",""), str.punctuation)
		if word in stop_list:
			continue

		else: #stems all other words
			word = PorterStemmer().stem(word, 0,len(word)-1)

		out_review.append(word)

	print " ".join(out_review)


def build_businesses(business_file):
	for line in business_file:
		obj = json.loads(line)
		bus_id = obj["business_id"] 
		categories = obj["categories"]
		if "Restaurants" in categories:
			bus_dict[bus_id] = True
"""

"""


def main():
	if len(sys.argv) != 3:
		print 'usage: python data_cleaning.py [reviews] [businesses]'
		sys.exit()
	else:
		reviews = open(sys.argv[1])
		businesses = open(sys.argv[2])
		build_businesses(businesses)
		clean(reviews)

if __name__ == "__main__":
    main(sys.argv)
