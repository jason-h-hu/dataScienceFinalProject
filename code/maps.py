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




LUNCHSECS = 12*60*60
DINNERSECS = 18*60*60




""" This is the only function you all will care about. 
Takes in a start and end location, as words
date is a datetime.datetime() object

Returns a list of (timestamp, coordinate) of all the meals we want
this is a datetime.datetime() object and a (int, int) respectively
"""
def getMeals(start, end, date):
	fullJourney = makeRequest(start, end)
	meals = []
	startDate = datetime.datetime(date.year, date.month, date.day, 0)
	currentDay = datetime.datetime(date.year, date.month, date.day, 0)
	while True:
		# def getCoordinateAtTime(pathObject, travel_time):
		lunchtime = currentDay + datetime.timedelta(0, LUNCHSECS)
		coordinate, success = getCoordinateAtTime(fullJourney, (lunchtime - startDate).total_seconds())
		if success:
			meals.append((lunchtime, coordinate))
		else:
			break
		dinnertime = currentDay + datetime.timedelta(0, DINNERSECS)
		coordinate, success = getCoordinateAtTime(fullJourney, (dinnertime - startDate).total_seconds())
		if success:
			meals.append((dinnertime, coordinate))
		else:
			break
		currentDay = currentDay + datetime.timedelta(1)
	return meals


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# DANGER DANGER! This is all helper functions. You shouldn't need to call any of these functions! 
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


""" Makes the API request, parses it, and returns a pathObject
Input - startLocation: A string describing the start, as either words or coordinates
		endLocation: Same, but for the end
Returns - a pathObject dicitonary:
	{
		<------------- summary of the whole path ------------->
		"distance"
		"duration"
		"start_location"
		"end_location"
		"steps": [
			<------------- each individual segment --------->
			{
				"distance"
				"duration"
				"start_location"
				"end_location"			
			},
			...	
		]
	}

	Note, distance and duration have two fields: "value" and "text"
	Start and end locations have two fields: "lat" and "lng"
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
	leg = response["routes"][0]["legs"][0]

	# A leg as defined by Google is a poriton of the path, 
	# if we use waypoints. Otherwise, it's the whole path
	pathObjectFields = ["distance", "duration", "start_location", "end_location"]

	# A step is the smallest fragement of the journey.
	steps = [{key: step[key] for key in pathObjectFields} for step in leg["steps"]]
	steps = [step for step in steps]

	pathObject = {key: leg[key] for key in pathObjectFields}
	pathObject["steps"] = steps

	return pathObject

def getCoordinateAtTime(pathObject, travel_time):
	time_traveled = 0
	steps = pathObject["steps"]
	for step in steps:
		if step["duration"]["value"] + time_traveled >= travel_time:
			remaining_time = travel_time - time_traveled
			return interpolateSegment(step, remaining_time), True
		time_traveled += step["duration"]["value"]
	return None, False

def interpolateSegment(step, travel_time):
	p = (travel_time)/step["duration"]["value"]
	lat = interpolate(step["start_location"]["lat"], step["end_location"]["lat"], p)
	lng = interpolate(step["start_location"]["lng"], step["end_location"]["lng"], p)
	return {"lat":lat, "lng": lng}

def interpolate(x1, x2, p):
	return x1 + (x2 - x1)*p



def main():
	print getMeals("Providence,RI", "San Francisco,CA", datetime.datetime(2015, 5, 27))


if __name__ == '__main__':
	main()