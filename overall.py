import yelp
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
        restaurant_list = yelp.query_api(input_values.ll)
        for restaurant in restaurant_list:
            if 'coord' in restaurant:
                lat = restaurant['coord']['latitude']
                lng = restaurant['coord']['longitude']
            if 'name' in restaurant:
                name = restaurant['name']
            google_dict = queryGoogle(lat, lng, name)
            restaurant['google_place_id'] = google_dict['google_place_id']
            restaurant['google_rating'] = google_dict['googe_rating']
            restaurant['google_review_list'] = google_dict['reviews']
        #how tdo we return?
    except urllib2.HTTPError as error:
        sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))


if __name__ == '__main__':
    main()