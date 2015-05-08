
"""
weighted rating (WR) = (v / (v+m)) * R + (m / (v+m)) * C
Where:
R = average for the movie (mean) = (Rating)
v = number of votes for the movie = (votes)
m = minimum votes required to be listed in the Top 250 (currently 25000)
C = the mean vote across the whole report (currently 7.0)
http://www.quora.com/Recommendation-Systems/How-do-ranking-algorithms-eg-Amazon-Tripadvisor-work

Takes in one restaurant, returns that restuarant with weight as
weighted_stars in the dictionary

Note: ignores google star review, since we only have Yelp # reviews
"""
def create_weighted_stars(rests):
	m = min([r['num_yelp_reviews'] for r in rests])
	C = sum(r['yelp_star']*r['num_yelp_reviews'] for r in rests)/sum(r['num_yelp_reviews'] for r in rests)
	for rest in rests:
		R = rest['yelp_star']
		v = float(rest['num_yelp_reviews'])
		rest['weighted_stars'] = (v/(v+m))*R + (m/(v+m))*C
	return rests

# """
# Creates relative_unique values based on uniqueness
# TODO: Does nothing for now
# """
# def create_relative_uniqueness(rests):
# 	for r in rests:
# 		r['relative_unique'] = 0.0

"""
Linearly combines all metrics
"""
def weight(rest):
	star = rest['weighted_stars']
	dist = rest['dist_from_ll']
	# uniq = rest['relative_unique']
	sent = rest['sentiment']
	numRevs = rest['num_yelp_reviews']

	rest['weighted_score'] = 0.0
	return rest



"""
Ranks a list of restaurants based on their calculated weight
Adds the weighted rank to the restaurant dictionary as 'weighted_score'
Returns a sorted list
"""
def rank(rests):
	create_weighted_stars(rests)
	create_relative_uniqueness(rests)
	rests = [weight(r) for r in rests]
	rests.sort(key = lambda x: x['weighted_score'], reverse=True)
	return rests