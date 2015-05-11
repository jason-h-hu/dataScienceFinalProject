import urllib
import json
import math
import datetime

def getMeals(start, end, date, DEPARTURE=9, LUNCHTIME=12, DINNERTIME=18, HOURSPERDAY=12):
	""" 
	Takes in a start and end location, as words
	date is a datetime.datetime() object

	Returns a list of (timestamp, coordinate) of all the meals we want
	this is a datetime.datetime() object and a (int, int) respectively
	"""
	fullJourney = makeRequest(start, end)
	return getMealsHelper(fullJourney, date, DEPARTURE, LUNCHTIME, DINNERTIME, HOURSPERDAY)

def getMealsAndPath(start, end, date, DEPARTURE=9, LUNCHTIME=12, DINNERTIME=18, HOURSPERDAY=12):
	""" 
	Takes in a start and end location, as words
	date is a datetime.datetime() object

	Returns the results from the Google Directions API, and the list 
	of (timestamp, coordinate) of all the meals we want.
		{
			"path": A polyline, defined as [{latitude: int, longitude: int} ... ],
			"locations": [(timestamp, coordinate) ...]
		}
	"""
	fullJourney = makeRequest(start, end)
	print fullJourney
	path = fullJourney["steps"]
	path = map(lambda x: {"latitude": x["start_location"]["lat"] , "longitude": x["start_location"]["lng"]}, path)
	# lastPoint = fullJourney["steps"][-1]["end_location"]
	# path += {"latitude": lastPoint["lat"], "longitude": lastPoint["lng"]}
	# print path
	return  {
		"path":  path,
		"locations": getMealsHelper(fullJourney, date, DEPARTURE, LUNCHTIME, DINNERTIME, HOURSPERDAY)
	}  


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# DANGER DANGER! This is all helper functions. You shouldn't need to call any of these functions! 
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def getMealsHelper(fullJourney, date, DEPARTURE=9, LUNCHTIME=12, DINNERTIME=18, HOURSPERDAY=12):

	steps = fullJourney["steps"]

	meals = []
	today = datetime.datetime(date.year, date.month, date.day, DEPARTURE)

	totalSecondsSinceLastStop = 0
	important_times = [(LUNCHTIME - DEPARTURE)*60*60, (DINNERTIME - LUNCHTIME)*60*60, (HOURSPERDAY+DEPARTURE-DINNERTIME)*60*60]
	i = 0
	next_mealtime = important_times[i]
	totalTotal = 0

	for step in steps:

		# You've traveled a bit further
		remaining_time = next_mealtime - totalSecondsSinceLastStop
		totalSecondsSinceLastStop += step["duration"]["value"]
		totalTotal += step["duration"]["value"]

		# You should stop for a meal!
		# why the while? Well, on really long stretches (i.e. > 3 hours) maybe there'll
		# be two meals along that route
		while totalSecondsSinceLastStop >= next_mealtime:

			# If it's the last "event" then you know it's just finding a place to rest
			# Reset the counter
			if i == len(important_times) - 1:
				today = datetime.datetime(today.year, today.month, today.day+1, DEPARTURE)
				interpolateSegment(step, remaining_time)

			else:
				meals.append((today + datetime.timedelta(0, sum(important_times[:i+1])), interpolateSegment(step, remaining_time)))

			totalSecondsSinceLastStop -= next_mealtime
			i += 1
			i %= len(important_times)
			next_mealtime = important_times[i]
			remaining_time += next_mealtime

		# if step["duration"]["value"] + totalSecondsSinceLastStop >= next_mealtime:

		# 	# If it's the last one, then we know it's the end of the day. Just reset the day counter
		# 	if i == len(important_times) - 1:
		# 		today = datetime.datetime(today.year, today.month, today.day+1, DEPARTURE)
		# 		totalSecondsSinceLastStop += step["duration"]["value"]
		# 		totalSecondsSinceLastStop %= next_mealtime

		# 	# Otherwise it's an actual meal. Figure out the coordinates we'll be at during the mealtime
		# 	else:
		# 		remaining_time = next_mealtime - totalSecondsSinceLastStop
		# 		meals.append((today + datetime.timedelta(0, sum(important_times[:i+1])), interpolateSegment(step, remaining_time)))
		# 		totalSecondsSinceLastStop += step["duration"]["value"]
		# 	i += 1
		# 	i %= len(important_times)
	return meals

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

# def getCoordinateAtTime(pathObject, travel_time):
# 	time_traveled = 0
# 	steps = pathObject["steps"]
# 	for step in steps:
# 		if step["duration"]["value"] + time_traveled >= travel_time:
# 			remaining_time = travel_time - time_traveled
# 			return interpolateSegment(step, remaining_time), True
# 		time_traveled += step["duration"]["value"]
# 	return None, False

def interpolateSegment(step, travel_time):
	p = float(travel_time)/step["duration"]["value"]
	lat = interpolate(step["start_location"]["lat"], step["end_location"]["lat"], p)
	lng = interpolate(step["start_location"]["lng"], step["end_location"]["lng"], p)
	return {"lat":lat, "lng": lng}

def interpolate(x1, x2, p):
	return x1 + (x2 - x1)*p

def secondsToTimestamp(start, secondsEllapsed):
	return start + datetime.timedelta(0, secondsEllapsed)

def secondsToHours(seconds):
	return float(seconds)/60/60

def main():
	getMeals("Providence,RI", "Miami,FL", datetime.datetime(2015, 5, 27))


if __name__ == '__main__':
	main()