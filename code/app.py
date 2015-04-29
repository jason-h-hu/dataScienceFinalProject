import argparse
import maps
from datetime import date

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
		print 'At '+str(m[0])+', eat at '+str(m[1]['lat'])+', '+str(m[1]['lng'])

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