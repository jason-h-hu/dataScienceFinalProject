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
    url = 'http://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

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
    
    print u'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response

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
        'offset': OFFSET.replace(' ', '+'),
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
    response = search(location)

    businesses = response.get('businesses')

    if not businesses:
        print u'No businesses in {0} found.'.format(location)
        return
    # print "\n\n\n businesses"
    print "length"
    print len(businesses)
    # print businesses
    business_id = businesses[0]['id']

    print u'{0} businesses found, querying business info for the top result "{1}" ...'.format(
        len(businesses),
        business_id
    )

    response = get_business(business_id)

    print u'Result for business "{0}" found:'.format(business_id)
    pprint.pprint(response, indent=2)


def main():
    parser = argparse.ArgumentParser()

    # parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM, type=str, help='Search term (default: %(default)s)')
    # parser.add_argument('-l', '--location', dest='location', default=DEFAULT_LOCATION, type=str, help='Search location (default: %(default)s)')
    parser.add_argument('-ll', '--ll', dest='ll', default=SARAH_HOUSE, type=str, help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        # query_api(input_values.term, input_values.location)
        query_api(input_values.ll)
        # query_api(LL)
    except urllib2.HTTPError as error:
        sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))


if __name__ == '__main__':
    main()