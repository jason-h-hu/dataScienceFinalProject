import urllib

def main():
	url = "http://maps.googleapis.com/maps/api/directions/json?"
	origin = "origin=Toronto"
	destination = "destination=Montreal"
	assembledURL = url + origin + "&" + destination
	print urllib.urlopen(assembledURL).read()


""" Returns the list of (time, coordinates), if applicable

pathObject - ???
"""
def findMealLocation(pathObject, departureTime, breakfast=9, lunch=12, dinner=18):
	pass

""" Returns a list of new pathObjects
"""
def splitRouteIntoDays(pathObject, maxHours=12):
	pass

if __name__ == '__main__':
	main()