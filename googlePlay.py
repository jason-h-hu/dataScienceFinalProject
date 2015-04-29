# usage example: python googlePlay.py --lat 37.878998 --lng -122.182021 --name "La Piazza"


#*Functions to grab the necessary data from Google.
#BEGIN PROGRAM.
import urllib, json
import argparse



#Grabbing and parsing the JSON data
def get_place_id(lat,lng,name):
  #making the url
  AUTH_KEY = "AIzaSyAOjjN8YD3ZudTfA1miPPY3Wm1S7Zla8Dk"
  LOCATION = str(lat) + "," + str(lng)
  RADIUS = 10 #radius
  TYPES = "restaurant"
  NAME = name
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
  print jsonData
  print jsonData['results'][0]['place_id']
  return jsonData['results'][0]['place_id']

#This is a helper to grab the Json data that I want in a list
def IterJson(place):
  x = [place['name'], place['reference'], place['geometry']['location']['lat'], 
         place['geometry']['location']['lng'], place['vicinity']]
  return x
#END PROGRAM.

def get_reviews(place_id):
  PLACE_ID = str(place_id)
  AUTH_KEY = "AIzaSyAOjjN8YD3ZudTfA1miPPY3Wm1S7Zla8Dk"
  MyUrl = ('https://maps.googleapis.com/maps/api/place/details/json'
           '?placeid=%s'
           '&sensor=false&key=%s') % (PLACE_ID, AUTH_KEY)
  #grabbing the JSON result
  response = urllib.urlopen(MyUrl)
  jsonRaw = response.read()
  jsonData = json.loads(jsonRaw)
  reviews = jsonData['result']['reviews']
  print reviews
  return reviews



def main():
    #parser = argparse.ArgumentParser()
    #parser.add_argument('-ll', '--ll', dest='ll', default=SARAH_HOUSE, type=str, help='Search location (default: %(default)s)')
    #input_values = parser.parse_args()

    # try:
    #     # query_api(input_values.term, input_values.location)
    #     query_api(input_values.ll)
    #     # query_api(LL)
    # except urllib2.HTTPError as error:
    #     sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))

    east_side_lat  = 41.829554
    east_side_lng  = -71.400978
    east_side_name = "East Side Pockets"
    #name = "east side"
    #name = "pockets"


    parser = argparse.ArgumentParser()

    # parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM, type=str, help='Search term (default: %(default)s)')
    # parser.add_argument('-l', '--location', dest='location', default=DEFAULT_LOCATION, type=str, help='Search location (default: %(default)s)')
    parser.add_argument('-lat', '--lat', dest='lat', default=east_side_lat, type=float, help='Search Latitude (default: %(default)s)')
    parser.add_argument('-lng', '--lng', dest='lng', default=east_side_lng, type=float, help='Search Longitude (default: %(default)s)')
    parser.add_argument('-name', '--name', dest='name', default=east_side_name, type=str, help='Search Name (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        place_id = get_place_id(input_values.lat,input_values.lng,input_values.name)
        get_reviews(place_id)
        # query_api(LL)
    except urllib2.HTTPError as error:
        sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))



if __name__ == '__main__':
    main()