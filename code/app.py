import argparse
import maps
from datetime import datetime, date
import get_restaurants
import unique_word_builder
import json
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

DEBUG = True
SECRET_KEY = 'DATASCIENCEISSOCOOL'
USERNAME = 'admin'
PASSWORD = 'default'

"""
Runs the full application, printing to the console a list of the top restaurants and reviews
Inputs: d (str: a date formatted as mm/dd/yyyy),
		start (str: place name or latlong)
		end (str: place name or latlong)
Prints: top x restaurants and relevant information about them
"""
def test_run(d, start, end):
	print 'Finding places to eat for a road trip starting '+str(d)+' at '+start+' and ending at '+end
	meals = maps.getMeals(start, end, d)
	for m in meals:
		coords = m[1]
		rests = get_restaurants.get_restaurants(coords['lat'], coords['lng'])
		if rests==None:
			#TODO! obviously this is NOT only what we want to do, this is a placeholder
			continue
		rests = unique_word_builder.build_words_entry(rests)
		#print m[0],rests[:10]

def run_app():
	app = Flask(__name__)
	app.config.from_object(__name__)

	"""
	To test using curl, try this command:
	curl -H "Content-Type: application/json" -X POST -d '{"start": "Providence, RI", "end": "San Francisco, CA"}' http://127.0.0.1:5000/journey
	"""
	@app.route('/journey', methods=["GET", "POST"])
	def journey():
		# request.json
		start = request.json["start"]
		end = request.json["end"]
		# http://stackoverflow.com/questions/10805589/converting-json-date-string-to-python-datetime
		d = datetime.today()
		meals = maps.getMeals(start, end, d)
		return json.dumps(meals, default=lambda x: x.isoformat() if hasattr(x, 'isoformat') else x)

	"""
	To test using curl, try this command:
	curl -H "Content-Type: application/json" -X POST -d '{"lat": 41.8236, "lng": -71.4222}' http://127.0.0.1:5000/restaurants
	"""
	@app.route('/restaurants', methods=["GET", "POST"])
	def restaurants():
		print request.json

		coords = request.json
		rests = get_restaurants.get_restaurants(coords['lat'], coords['lng'])
		if rests==None:
			#TODO! obviously this is NOT only what we want to do, this is a placeholder
			return json.dumps([])
		rests = unique_word_builder.build_words_entry(rests)

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
			test_run(args.date, args.start[0], args.end[0])