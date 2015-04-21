import urllib
import json
import math

def printAsTime(totalSeconds):
	hours = int(math.floor(totalSeconds/(60*60)))
	mins = totalSeconds/60 - hours*60
	return str(hours) + ":" + str(mins)


def main():
	fullJourney = makeRequest("Providence,RI", "San Francisco,CA")
	dayJourneys = splitRouteIntoDays(fullJourney)

	for day in dayJourneys:
		# print sum([step["duration"]["value"] for step in day["steps"]])/(60*60)
		elapsed = 9*60*60
		for step in day["steps"]:
			elapsed += step["duration"]["value"]
			print printAsTime(elapsed), "\t->\t",step["distance"]["value"]
		meals = findMealLocation(day)
		for time, coordinate in meals:
			print "We'll be eating at", coordinate["lat"], ",", coordinate["lng"], "at", printAsTime(time)
		print "next day"


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
# where you'll be after traveling desiredSeconds
def findTimeHelper(steps, desiredSeconds):

	secsTraveledToday = 0
	for i, step in enumerate(steps):
		secsTraveledToday += step["duration"]["value"]
		if secsTraveledToday > desiredSeconds:
			return i+1

	return len(steps)

""" Returns a list of new pathObjects
"""
def splitRouteIntoDays(pathObject, minHours=6, maxHours=12):

	days = []

	idealSeconds = ((minHours + maxHours) / 2)*60*60

	steps = pathObject["steps"]
	while len(steps) > 0:
		i = findTimeHelper(steps, idealSeconds)
		currentSteps = steps[:i]
		day = {	"distance": {"value": sum([step["distance"]["value"] for step in currentSteps])}, 
				"duration": {"value": sum([step["duration"]["value"] for step in currentSteps])}, 
				"start_location": currentSteps[0]["start_location"], 
				"end_location": currentSteps[-1]["end_location"], 
				"steps": currentSteps}
		days.append(day)
		steps = steps[i:]

	return days

""" Returns the list of (time, coordinates), if applicable

pathObject - ???
"""
def findMealLocation(pathObject, departureTime=9, lunch=12, dinner=18):

	meals = []
	steps = pathObject["steps"]
	l = findTimeHelper(steps, (lunch-departureTime)*60*60)
	lunchtime = departureTime*60*60 + sum([step["duration"]["value"] for step in steps[:l]])
	lunchlocation = steps[l-1]["end_location"]

	d = findTimeHelper(steps, (dinner-departureTime)*60*60)
	dinnertime = departureTime*60*60 + sum([step["duration"]["value"] for step in steps[:d]])
	dinnerlocation = steps[d-1]["end_location"]

	return [(lunchtime, lunchlocation), (dinnertime, dinnerlocation)]



	pass
if __name__ == '__main__':
	main()