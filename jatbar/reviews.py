"""from jatbar
https://github.com/mrorii/findjatbar/blob/master/findjatbar/reviews.py
"""
#!/usr/bin/env python

from collections import namedtuple

Review = namedtuple('Review', 'restaurant_id, author, entry')