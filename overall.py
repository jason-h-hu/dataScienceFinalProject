import yelpPlay
import argparse
import urllib
import urllib2

SARAH_HOUSE = "41.826998,-71.403599"

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