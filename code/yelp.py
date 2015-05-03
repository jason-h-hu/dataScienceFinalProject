
"""USAGE: python yelpPlay.py -ll "<lat>,<lon>"
(note: south and west are negatives)
prints info.... we can play around this later
"""

import argparse
import json
import pprint
import sys
import urllib
import urllib2

import oauth2


# consumer key: SF7TtjFhkf3sDWq38r5UpQ
CONSUMER_KEY = "SF7TtjFhkf3sDWq38r5UpQ"
CONSUMER_SECRET= "FFDWCFtr89ZfuFsr6niTrSchah4"
TOKEN= "oik-47zq8TldfTqVweDICCAkDhTCHTOy"
TOKEN_SECRET=  "8Br7itbZZ3Irt7wrZtdp74OqXPk"

API_HOST = 'api.yelp.com'
# DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA' #this will change
SEARCH_LIMIT = "20" #what is this
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'
SORT = "1" #sort by distance
#SARAH AND EMILY - radius_filter
#temp global for testing
SARAH_HOUSE = "41.826998,-71.403599"
OFFSET = "20"


def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'http://{0}{1}?'.format(host, urllib.quote(path.encode('utf-8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)
    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()
    try:
        conn = urllib2.urlopen(signed_url, None)
        response = json.loads(conn.read())
        conn.close()
        return response
    except:
        return None


def search(location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """
    
    url_params = {
        # 'term': term.replace(' ', '+'),
        'll': location.replace(' ', '+'), #need to check in an pass eventually
        # 'limit': SEARCH_LIMIT.replace(' ', '+'),
        # 'offset': OFFSET.replace(' ', '+'),
        'limit': SEARCH_LIMIT.replace(' ', '+'),
        'sort': SORT.replace(' ', '+'),
        'category_filter': "restaurants"
    }
    # print 'url_params'
    # print url_params
    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def get_business(business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)

def query_api(location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    #print "in query api, location", location
    response = search(location)
    if response==None:
        return None

    businesses = response.get('businesses')
    num_restaurants_found = len(businesses)

    if num_restaurants_found==0: #TODO play around with this?
        return None
    else:
        restaurant_list = []
        # restaurant = {coord:{lat:<float>,lng:<float>}, img_url:<str>, name:<string>, phone_num:<str>,
        # address:<list<str>>, rest_url:<str>, num_yelp_reviews:<int>, dist_from_ll:<float>, yelp_review:<str>, 
        # google_review_list:[{review_author:<str>,review_star:<float>,review_text:<str>},{},..], 
        # google_star:<float>, yelp_star:<float>,google_place_id:<str>,yelp_id:<str>}
        for bus in businesses:

            restaurant = {}

            if 'name' in bus:
                name = bus['name']
                restaurant['name'] = name.encode('utf-8')

            if 'rating' in bus:
                yelp_star = bus['rating']
                restaurant['yelp_star'] = yelp_star

            if 'url' in bus:
                rest_url = bus['url']
                restaurant['rest_url'] = rest_url

            if 'phone' in bus:
                phone_num = bus['phone']
                restaurant['phone_num'] = phone_num

            if 'snippet_text' in bus:
                yelp_review = bus['snippet_text']
                restaurant['yelp_review'] = yelp_review

            if 'image_url' in bus:
                img_url = bus['image_url']
                restaurant['img_url'] = img_url

            if 'location' in bus:
                if 'display_address' in bus['location']:      
                    address = bus['location']['display_address']
                    restaurant['address'] = address
                if 'coordinate' in bus['location']:
                    coord = bus['location']['coordinate']
                    restaurant['coord'] = coord

            if 'id' in bus:
                yelp_id = bus['id']
                restaurant['yelp_id'] = yelp_id

            if 'review_count' in bus:
                num_yelp_reviews = bus['review_count']
                restaurant['num_yelp_reviews'] = float(num_yelp_reviews)

            if 'distance' in bus:
                dist_from_ll = bus['distance']
                restaurant['dist_from_ll'] = dist_from_ll

            restaurant_list.append(restaurant)

        #print restaurant_list
        return restaurant_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ll', '--ll', dest='ll', default=SARAH_HOUSE, type=str, help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.ll)
       
    except urllib2.HTTPError as error:
        sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))


if __name__ == '__main__':
    main()