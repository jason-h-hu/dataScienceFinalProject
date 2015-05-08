import argparse
import maps
from datetime import datetime, date
import get_restaurants
import unique_word_builder
import sentiment_builder
import json
import ranking
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


"""
This is the general helper method to get a list of restaurants from a coordinate.
Inputs: {'lat': , 'lng'}
Output: List of restaurants
"""
def get_restaurants_from_coordinate(coords):
	rests = get_restaurants.get_restaurants(coords['lat'], coords['lng'],pmin=1,pmax=5)
	if rests==None:
		return []
	rests = unique_word_builder.build_words_entry(rests)
	rests = sentiment_builder.build_sent_entry(rests)
	rests = ranking.rank(rests)
	return rests

"""
Allows Cross-Origin so localhost:8888 can call us
"""
def add_cors_header(response):
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
	response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, PATCH, DELETE, OPTIONS'
	return response

"""
Runs the full application, printing to the console a list of the top restaurants and reviews
Inputs: d (str: a date formatted as mm/dd/yyyy),
		start (str: place name or latlong)
		end (str: place name or latlong)
Prints: top x restaurants and relevant information about them
"""
def test_run(d, start, end, pmin, pmax):
	print 'Finding places to eat for a road trip starting '+str(d)+' at '+start+' and ending at '+end
	meals = maps.getMeals(start, end, d)
	for m in meals:
		coords = m[1]
		rests = x(coords)
		rests = [(r["name"],r["weighted_score"],"Info is",r['weighted_stars'],r['sentiment'],r['num_yelp_reviews']) for r in rests]
		print m[0],rests[:10]

def run_app():
	app = Flask(__name__)
	app.config.from_object(__name__)
	app.after_request(add_cors_header)
	
	"""
	Clears current requests somehow (TODO!!)
	"""
	@app.route('/clear', methods=["POST"])
	def clear():
		return json.dumps({})

	"""
	To test using curl, try this command:
	curl -H "Content-Type: application/json" -X POST -d '{"start": "Providence, RI", "end": "San Francisco, CA", "date":"2011-12-01T12:00:00.00Z"}' http://127.0.0.1:5000/journey
	"""
	@app.route('/journey', methods=["GET", "POST"])
	def journey():
		start = request.json["start"]
		end = request.json["end"]
		d = datetime.strptime(request.json["date"], '%Y-%m-%dT%H:%M:%S.%fZ') if request.json["date"] != None else datetime.datetime.today()
		meals = maps.getMeals(start, end, d)
		return json.dumps(meals, default=lambda x: x.isoformat() if hasattr(x, 'isoformat') else x)

	"""
	To test using curl, try this command:
	curl -H "Content-Type: application/json" -X POST -d '{"lat": 41.8236, "lng": -71.4222}' http://127.0.0.1:5000/restaurants
	"""
	@app.route('/restaurants', methods=["GET", "POST"])
	def restaurants():
		coords = request.json
		rests = get_restaurants_from_coordinate(coords)
		return json.dumps(rests, default=lambda x: x.isoformat() if hasattr(x, 'isoformat') else x)

	app.run()


"""
Simply takes command line arguments and runs the app - see test_run for more details
"""
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Find places to eat for your next big roadtrip!', prog="roadtrip")
	parser.add_argument('-d', '--date', type=str, nargs=1, metavar='date', default=date.today(),
		help='The date to start the roadtrip, as a string')
	parser.add_argument('-s', '--start', type=str, nargs=1, metavar='start',
		help='The starting location of the trip, as a string')
	parser.add_argument('-e', '--end', type=str, nargs=1, metavar='end',
		help='The ending location of the trip, as a string')
	parser.add_argument('-pmin', '--pmin', type=str, nargs=1, metavar = 'pmin', default='1',
		help='The minimum price for the restaurant, between 1 and 5, as a string')
	parser.add_argument('-pmax','--pmax', type=str, nargs=1, metavar = 'pmax', default='5',
		help="The maximum price for the restaurant, between 1 and 5, as a string")
	parser.add_argument('-g', '--gui', action='store_true', default=False,
		help='Whether to also run this with a Flask server')
	args = parser.parse_args()
	if args.gui:
		run_app()
	else:
		# Run the app itself!
		if args.start == None or args.end == None:
			print "NO! YOU NEED TO PROVIDE AN START AND END"
		else:
			test_run(args.date, args.start[0], args.end[0], int(args.pmin[0]), int(args.pmax[0]))
