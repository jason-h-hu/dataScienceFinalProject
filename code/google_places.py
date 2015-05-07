# usage example: python googlePlay.py --lat 37.878998 --lng -122.182021 --name "La Piazza"


#*Functions to grab the necessary data from Google.
#BEGIN PROGRAM.
import urllib, urllib2, json
import argparse

AUTH_KEY = "AIzaSyBXuz1jrJbf0aJYAx031Yqop0RGQ5MrxaI"

def query_google(lat, lng, name, radius=10):
  place_info = get_place_info(lat,lng,name)
  if (place_info != None):
    # print place_info
    (place_id,rating) = place_info
    review_list=get_reviews(place_id)
    googleDict = {}
    googleDict['google_place_id']=place_id
    googleDict['google_rating']=rating
    googleDict['reviews'] = review_list
    return googleDict
  else:
    return None

#### DO NOT DIRECTLY CALL ANYTHING BELOW THIS, THESE ARE ALL HELPER FUNCTIONS

#Grabbing and parsing the JSON data
def get_place_info(lat,lng,name,radius=10):
  # print "in get place id", lat,lng,name
  #making the url
  # AUTH_KEY = "AIzaSyAOjjN8YD3ZudTfA1miPPY3Wm1S7Zla8Dk"
  LOCATION = str(lat) + "," + str(lng)
  RADIUS = radius
  TYPES = "restaurant"
  NAME = str(name)
  MyUrl = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json'
           '?location=%s'
           '&radius=%s'
           '&types=%s'
           '&name=%s'
           '&sensor=false&key=%s') % (LOCATION, RADIUS, TYPES, NAME, AUTH_KEY)
  #grabbing the JSON result
  response = urllib.urlopen(MyUrl)
  jsonRaw = response.read()
  jsonData = json.loads(jsonRaw)
  # print jsonData
  if ('results' in jsonData):
    if len(jsonData['results'])==0:
      return None
    elif ('rating' in jsonData['results'][0]):
      return (jsonData['results'][0]['place_id'], jsonData['results'][0]['rating'])
    else:
      return None
  else:
    return None


#This is a helper to grab the Json data that I want in a list
def iter_json(place):
  x = [place['name'], place['reference'], place['geometry']['location']['lat'], 
         place['geometry']['location']['lng'], place['vicinity']]
  return x
#END PROGRAM.

def get_reviews(place_id):
  PLACE_ID = str(place_id)
  # AUTH_KEY = "AIzaSyAOjjN8YD3ZudTfA1miPPY3Wm1S7Zla8Dk"
  MyUrl = ('https://maps.googleapis.com/maps/api/place/details/json'
           '?placeid=%s'
           '&sensor=false&key=%s') % (PLACE_ID, AUTH_KEY)
  #grabbing the JSON result
  response = urllib.urlopen(MyUrl)
  # print response
  jsonRaw = response.read()
  jsonData = json.loads(jsonRaw)
  reviewData = jsonData['result']['reviews']
  review_list = []
  for review in reviewData:
    review_dict = {}
    review_dict['review_star']=review['rating']
    review_dict['review_author']=review['author_name']
    review_dict['review_text'] = review['text']
    review_list.append(review_dict)
  return review_list
  
def main():
   
    east_side_lat  = 41.829554
    east_side_lng  = -71.400978
    east_side_name = "East Side Pockets"

    parser = argparse.ArgumentParser()
    parser.add_argument('-lat', '--lat', dest='lat', default=east_side_lat, type=float, help='Search Latitude (default: %(default)s)')
    parser.add_argument('-lng', '--lng', dest='lng', default=east_side_lng, type=float, help='Search Longitude (default: %(default)s)')
    parser.add_argument('-name', '--name', dest='name', default=east_side_name, type=str, help='Search Name (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        google_results = query_google(input_values.lat, input_values.lng, input_values.name, radius=10)
        # print google_results

    except urllib2.HTTPError as error:
        sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))



if __name__ == '__main__':
    main()