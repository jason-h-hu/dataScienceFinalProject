import yelpPlay
import argparse
import urllib
import urllib2

SARAH_HOUSE = "41.826998,-71.403599"

# input: latitude (float) and longitude (float)
# output: list of restaurants around that lat and lng
# restaurant = {coord:{lat:<float>,lng:<float>}, img_url:<str>, name:<string>, phone_num:<str>,address:<list<str>>, rest_url:<str>, num_yelp_reviews:<int>, dist_from_ll:<float>, review_list:[{review_author:<str>,review_star:<float>,review_text:<str>},{},..], google_star:<float>, yelp_star:<float>,google_place_id:<str>,yelp_id:<str>}

# google place {reviews,google_place_id, google_star}

SARAH_HOUSE_LAT = 41.826998
SARAH_HOUSE_LNG = -71.403599

def get_restaurants(lat=SARAH_HOUSE_LAT,lng=SARAH_HOUSE_LNG):
    ll = lat + "," + lng
    restaurants = yelp.query_api(ll) #list of restaurants



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ll', '--ll', dest='ll', default=SARAH_HOUSE, type=str, help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        yelpPlay.query_api(input_values.ll)
        #next we need to write it so that yelp play will make a list of lat, long, and name to pass into googlep lay and we need to have it so that google play will return a list of reviews or however paige wants it
        # TODO start here 
        # query_api(LL)
    except urllib2.HTTPError as error:
        sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))


if __name__ == '__main__':
    main()