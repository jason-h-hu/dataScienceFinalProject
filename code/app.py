import argparse
from datetime import date

"""
Runs the full application, printing to the console a list of the top restaurants and reviews
Inputs: start_date (str: formatted as mm/dd/yyyy),
		start_location (str: place name or latlong)
		end_location (str: place name or latlong)
Prints: top x restaurants and relevant information about them
"""
def run_app(start_date, start_location, end_location):
	print start_date, start_location, end_location

"""
Simply takes command line arguments and runs the app - see run_app for more details
"""
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Find places to eat for your next big roadtrip!', prog="roadtrip")
	parser.add_argument('-d', '--date', type=str, nargs=1, metavar='date', default=date.today(),
		help='The date to start the roadtrip, as a string')
	parser.add_argument('-s', '--start', type=str, nargs=1, metavar='start_location', required=True,
		help='The starting location of the trip, as a string')
	parser.add_argument('-e', '--end', type=str, nargs=1, metavar='end_location', required=True,
		help='The ending location of the trip, as a string')
	args = parser.parse_args()

	# Run the app itself!
	run_app(args.date, args.start, args.end)