import yelp
import argparse
import urllib
import google_places
import urllib2
from time import sleep
# input: latitude (float) and longitude (float)
# output: list of restaurants around that lat and lng
# restaurant = {coord:{lat:<float>,lng:<float>}, img_url:<str>, name:<string>, phone_num:<str>,address:<list<str>>, rest_url:<str>, num_yelp_reviews:<int>, dist_from_ll:<float>, review_list:[{review_author:<str>,review_star:<float>,review_text:<str>},{},..], google_star:<float>, yelp_star:<float>,google_place_id:<str>,yelp_id:<str>}
#if restaurant doesn't have google review, then it won't have review_list, google star, or goolge place id in its dictionary
# google place {reviews,google_place_id, google_star}

SARAH_HOUSE_LAT = 41.826998
SARAH_HOUSE_LNG = -71.403599

def get_restaurants(lat=SARAH_HOUSE_LAT,lng=SARAH_HOUSE_LNG):
    sleep(1)
    ll = str(lat) + "," + str(lng)
    restaurant_list = yelp.query_api(ll)
    if restaurant_list==None:
        return None
    counter = 1
    for restaurant in restaurant_list:
        if counter == 10:
            sleep(1)
        lat = None
        lng = None
        name = None
        if 'coord' in restaurant:
            lat = restaurant['coord']['latitude']
            lng = restaurant['coord']['longitude']
        if 'name' in restaurant:
            name = restaurant['name']
        if lat and lng and name:
            #print "calling google places"
            google_dict = google_places.queryGoogle(lat, lng, name)
            if (google_dict!=None):
                #print "google dict was not none"
                restaurant['google_place_id'] = google_dict['google_place_id']
                restaurant['google_rating'] = google_dict['googe_rating']
                restaurant['google_review_list'] = google_dict['reviews']
            else:
                #print "google dict was none"
                restaurant['google_place_id'] = ""
                restaurant['google_rating'] = None
                restaurant['google_review_list'] = []
        counter += 1

    return restaurant_list



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-lat', '--lat', dest='lat', default=SARAH_HOUSE_LAT, type=float, help='Search location latitude (default: %(default)s)')
    parser.add_argument('-lng', '--lng', dest='lng', default=SARAH_HOUSE_LNG, type=float, help='Search location longitude (default: %(default)s)')
    
    input_values = parser.parse_args()
    get_restaurants(input_values.lat,input_values.lng)

if __name__ == '__main__':
    main()
