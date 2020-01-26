#!/usr/bin/env python

""" Alfred workflow to convert Plus Codes to Lat/Lng. """

from openlocationcode import decode

import os
import sys
import time
import json
import urllib.parse

from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


pluscode = sys.argv[1]

# decode plus code
items = []

try:
    # short code+reference point, we need a geo reverse lookup for the reference point
    if (' ' in pluscode):

        pluscode_url = 'https://plus.codes/%s' % (urllib.parse.quote_plus(pluscode))

        opp = Options()
        opp.add_argument('--headless')

        # We use Chrome as browser an not Safari (which would be installed on any Mac),
        # b/c 1) Safari doesn't support a headless mode as of now (so it would open, we lose 
        # focus on the Alfred window) 2) it was slow (>5s) to startup.
        browser = Chrome(os.environ['CHROMEDRIVER'], options=opp) 
        browser.get(pluscode_url)

        # wait until the URL get's rewritten to contain the logn form plus code (but max. 5s)
        wait = WebDriverWait(browser, 5)
        wait.until(lambda driver: driver.current_url != pluscode_url)

        url = browser.current_url
        browser.quit()

        o = urllib.parse.urlparse(url)
        pluscode = o.path[1:]

    # convert plus code to GPS
    codearea = decode(pluscode)
    latlng = "%s, %s" % (round(codearea.latitudeCenter, 6), round(codearea.longitudeCenter, 6))

    item = {
        'title': latlng,
        'subtitle': 'Latitude, Longitude',
        'arg': latlng,
        'text': {
            'copy': latlng
        },
        'mods': {
            "alt": {
                "arg": "http://maps.google.com/maps?q=%s" % (latlng),
                "subtitle": "Open in Google Maps"
            }
        }
    }
    items.append(item)

    item = {
        'title': pluscode,
        'subtitle': 'Long form Plus Code',
        'arg': pluscode,
        'text': {
            'copy': pluscode
        },
        'mods': {
            'alt': {
                'arg': 'https://plus.codes/%s' % (pluscode),
                'subtitle': "Open in Plus.codes"
            }
        }
    }
    items.append(item)

except Exception as e:
    item = {}
    item['title'] = "Something went wrong: %s" % (type(e).__name__)
    item['subtitle'] = str(e)
    items.append(item)

response = {}
response['items'] = items
print(json.dumps(response)) 
