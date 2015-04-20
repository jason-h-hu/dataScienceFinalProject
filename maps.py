import urllib
import json


def main():
	fullJourney = makeRequest("Providence,RI", "Miami,FL")
	dayJourneys = splitRouteIntoDays(fullJourney)
	for day in dayJourneys:
		print day["start_location"], "->", day["end_location"]
	meals = [findMealLocation]
	for time, coordinate in meals:
		print "We'll be eating at", coordinate, "at", time


""" Makes the API request, parses it, and returns a pathObject
"""
def makeRequest(startLocation, endLocation):

	# Assembling the API request. Maybe we should do some
	# input checking?
	url = "http://maps.googleapis.com/maps/api/directions/json?"
	origin = "origin=" + startLocation
	destination = "destination=" + endLocation
	assembledURL = url + origin + "&" + destination
	response = json.loads(urllib.urlopen(assembledURL).read())
	if response["status"] != "OK":
		print "Warning! Status is not okay" # should throw error?
		return None

	# See https://developers.google.com/maps/documentation/directions/#DirectionsResponses
	# for details about the fields returned by the API request.
	return parseLegHelper(response["routes"][0]["legs"][0])

def parseLegHelper(leg):
	# A leg as defined by Google is a poriton of the path, 
	# if we use waypoints. Otherwise, it's the whole path
	pathObjectFields = ["distance", "duration", "start_location", "end_location"]

	# A step is the smallest fragement of the journey.
	steps = [{key: step[key] for key in pathObjectFields} for step in leg["steps"]]
	steps = [step for step in steps]

	pathObject = {key: leg[key] for key in pathObjectFields}
	pathObject["steps"] = steps

	return pathObject

# Returns the index of the step in pathObject["steps"]
# where you'll be after traveling desiredMins
def findTimeHelper(steps, desiredMins):

	steps = pathObject["steps"]
	minsTraveledToday = 0
	for i, step in enumerate(steps):
		minsTraveledToday += step["duration"]["value"]
		if minsTraveledToday > desiredMins:
			return i

	return len(steps)

""" Returns a list of new pathObjects
"""
def splitRouteIntoDays(pathObject, minHours=6, maxHours=12):

	days = []

	idealMinutes = ((minHours + maxHours) / 2) * 60

	steps = pathObject["steps"]
	while len(steps) > 0:
		i = findTimeHelper(steps, idealMinutes)
		currentSteps = steps[:i]
		day = {	"distance": {"value": sum([step["distance"]["value"] for step in currentSteps])}, 
				"duration": {"value": sum([step["duration"]["value"] for step in currentSteps])}, 
				"start_location": steps[0]["start_location"], 
				"end_location": currentSteps[-1]["end_location"], 
				"steps": currentSteps}
		steps = steps[i+1:]

	return days

""" Returns the list of (time, coordinates), if applicable

pathObject - ???
"""
def findMealLocation(pathObject, departureTime=9, lunch=12, dinner=18):
	pass



	pass
if __name__ == '__main__':
	main()