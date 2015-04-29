import urllib
import json
import math
import datetime

"""

NOTES: 

Right now, the whole journey is being partitioned into days using a greedy algorithm.

To decide where we'll be for a meal, we find the segment we'll be traveling on when it's mealtime, and we use the "destination" field of that segment

These have a few weird edge cases. 

Day partitioning could be much smarter.

Also, if we're on a long segment during lunchtime, that schedules lunch for around 3 or 4. 

We should interpolate on those segments, so we can find a better coordinate for lunch


"""

""" This is the only function you all will care about. 
Takes in a start and end location, as words
date is a datetime.datetime() object

Returns a list of (timestamp, coordinate) of all the meals we want
this is a datetime.datetime() object and a (int, int) respectively
"""
def getMeals(start, end, date):
	fullJourney = makeRequest(start, end)
	dayJourneys = splitRouteIntoDays(fullJourney)
	meals = []
	daytime = datetime.timedelta(1)
	currentDay = datetime.datetime(date.year, date.month, date.day, 9)
	for day in dayJourneys:
		currentMeals = findMealLocation(day)
		for secondsEllpased, location in currentMeals:
			timedelta = datetime.timedelta(0, secondsEllpased)
			meals.append((currentDay + timedelta, location))
		currentDay = currentDay + daytime
	return meals


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# DANGER DANGER! This is all helper functions. You shouldn't need to call any of these functions! 
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


""" Makes the API request, parses it, and returns a pathObject
"""
def makeRequest(startLocation, endLocation):

	# Assembling the API request. Maybe we should do some
	# input checking?																<-------------------------------------???
	url = "http://maps.googleapis.com/maps/api/directions/json?"
	origin = "origin=" + startLocation
	destination = "destination=" + endLocation
	assembledURL = url + origin + "&" + destination
	response = json.loads(urllib.urlopen(assembledURL).read())
	if response["status"] != "OK":
		print "Warning! Status is not okay" # should throw error? 					<-------------------------------------???
		return None
	# See https://developers.google.com/maps/documentation/directions/#DirectionsResponses
	# for details about the fields returned by the API request.
	return parseLegHelper(response["routes"][0]["legs"][0])

""" Helps parse the API request, specifically the "leg" field returned by Google
Takes in the really verbose description, and filters it down to just the
distance, duration, start_location, and end_location field
"""
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

	# Right now, I take the average of min and max
	# and say that's how long we travel
	idealSeconds = ((minHours + maxHours) / 2)*60*60


	# Okay, so this is a bad alogirthm. It greedily goes
	# through the steps, to carve out segments of the journey.
	# Paul Valiant would cry. 
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
	lunchtime = sum([step["duration"]["value"] for step in steps[:l]])
	lunchlocation = steps[l-1]["end_location"]

	d = findTimeHelper(steps, (dinner-departureTime)*60*60)
	dinnertime = lunchtime + sum([step["duration"]["value"] for step in steps[l:d]])
	dinnerlocation = steps[d-1]["end_location"]

	return [(lunchtime, lunchlocation), (dinnertime, dinnerlocation)]


def printAsTime(totalSeconds):
	hours = int(math.floor(totalSeconds/(60*60)))
	mins = totalSeconds/60 - hours*60
	return str(hours) + ":" + str(mins)



def main():
	getMeals("Providence,RI", "San Francisco,CA", datetime.datetime(2015, 5, 27))


if __name__ == '__main__':
	main()