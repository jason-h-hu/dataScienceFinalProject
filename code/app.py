import argparse
import maps
from datetime import date
import get_restaurants
import unique_word_builder

"""
Runs the full application, printing to the console a list of the top restaurants and reviews
Inputs: d (str: a date formatted as mm/dd/yyyy),
		start (str: place name or latlong)
		end (str: place name or latlong)
Prints: top x restaurants and relevant information about them
"""
def run_app(d, start, end):
	print 'Finding places to eat for a road trip starting '+str(d)+' at '+start+' and ending at '+end
	meals = maps.getMeals(start, end, d)
	for m in meals:
		coords = m[1]
		rests = get_restaurants.get_restaurants(coords['lat'], coords['lng'])
		rests = unique_word_builder.build_words_entry(rests)
		print m[0],rests[:10]


"""
Simply takes command line arguments and runs the app - see run_app for more details
"""
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Find places to eat for your next big roadtrip!', prog="roadtrip")
	parser.add_argument('-d', '--date', type=str, nargs=1, metavar='date', default=date.today(),
		help='The date to start the roadtrip, as a string')
	parser.add_argument('-s', '--start', type=str, nargs=1, metavar='start', required=True,
		help='The starting location of the trip, as a string')
	parser.add_argument('-e', '--end', type=str, nargs=1, metavar='end', required=True,
		help='The ending location of the trip, as a string')
	args = parser.parse_args()

	# Run the app itself!
	run_app(args.date, args.start[0], args.end[0])