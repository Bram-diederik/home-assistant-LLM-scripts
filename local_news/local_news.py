#!/usr/bin/python3
import feedparser
import json
from datetime import datetime, timedelta
import shlex
import pytz
import sys
import argparse
import re
import requests

# Function to convert a string to Camel Case
def to_camel_case(s):
    words = s.split()
    result = []

    for i, word in enumerate(words):
        if i == 0:  # Keep the first word in proper case
            result.append(word.capitalize())
        else:  # For subsequent words, capitalize only the first letter
            result.append(word.capitalize())
    
    return ' '.join(result)

def get_postal_code(town, country_code):
    print(town)
    # Prepare the URL for the API request
    url = f"https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-postal-code@public/records"
    params = {
        "select": "postal_code",
        "where": f"country_code='{country_code}' AND place_name='{town}'",
        "order_by": "postal_code",
        "limit": 1
    }

    # Make the GET request to the API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Print the full response for debugging
        print(data)

        # Adjust based on the actual response structure
        try:
            if 'results' in data and len(data['results']) > 0:
                postal_code = data['results'][0]['postal_code']
                return postal_code
            else:
                print("No postal code found for " + town + " " + country_code)
                return f"No postal code found for {{town}}, {{country_code}}."
        except KeyError as e:
            return f"Error accessing key {e} in the response."
    else:
        return f"Error: {response.status_code}"


def get_local_news_rss_nl(postcode):
    try:
        postcode = int(str(postcode)[:4])  # Pak de eerste 4 cijfers van de postcode
    except ValueError:
        return None  # Ongeldige postcode
    
    match postcode:

        # Noord-Holland
        case _ if 1000 <= postcode <= 1299:
            return "https://rss.at5.nl/rss", "%a, %d %b %Y %H:%M:%S %Z"
        case _ if 1380 <= postcode <= 1384 or 1394 <= postcode <= 1394 or 1398 <= postcode <= 1425 or 1430 <= postcode <= 2158 or postcode == 2165:
            return "https://rss.nhnieuws.nl/rss", "%a, %d %b %Y %H:%M:%S %Z"
        # Flevoland
        case _ if 1300 <= postcode <= 1379 or 3890 <= postcode <= 3899 or 8200 <= postcode <= 8259 or 8300 <= postcode <= 8322:
            return "https://www.omroepflevoland.nl/RSS/rss.aspx", "%a, %d %b %Y %H:%M:%S GMT%z"
        # Utrecht
        case _ if 1390 <= postcode <= 1393 or postcode == 1396 or 1426 <= postcode <= 1427 or 3382 <= postcode <= 3464 or 3467 <= postcode <= 3769 or 3795 <= postcode <= 3836 or 3900 <= postcode <= 3924 or 3926 <= postcode <= 3999 or 4120 <= postcode <= 4125 or 4130 <= postcode <= 4146 or 4163 <= postcode <= 4169 or 4230 <= postcode <= 4239 or 4242 <= postcode <= 4249:
            return "https://www.rtvutrecht.nl/rss/nieuws.xml", "%a, %d %b %Y %H:%M:%S %Z"
        # Zuid-Holland
        case _ if 1428 <= postcode <= 1429 or 2159 <= postcode <= 2164 or postcode == 2166 or 2170 <= postcode <= 3381 or 3465 <= postcode <= 3466 or 4200 <= postcode <= 4209 or postcode == 4213 or 4220 <= postcode <= 4229 or 4240 <= postcode <= 4241:
            return "https://www.omroepwest.nl/rss/index.xml", "%a, %d %b %Y %H:%M:%S %Z"
        # Gelderland
        case _ if 3770 <= postcode <= 3794 or 3837 <= postcode <= 3888 or postcode == 3925 or 4000 <= postcode <= 4119 or 4147 <= postcode <= 4162 or 4170 <= postcode <= 4199 or 4211 <= postcode <= 4212 or 4214 <= postcode <= 4219 or 5300 <= postcode <= 5335 or 6500 <= postcode <= 6583 or 6600 <= postcode <= 7399 or postcode == 7439 or 8050 <= postcode <= 8054 or 8070 <= postcode <= 8099 or 8160 <= postcode <= 8195:
            return "https://www.omroepgelderland.nl/rss", "%a, %d %b %Y %H:%M:%S %z"
        # Zeeland
        case _ if 4300 <= postcode <= 4599 or 4672 <= postcode <= 4679 or 4682 <= postcode <= 4699:
            return "http://www.hvzeeland.nl/RSS/Nieuws", "%a, %d %b %Y %H:%M:%S +0100"
        # Noord-Brabant
        case _ if 4250 <= postcode <= 4299 or 4600 <= postcode <= 4671 or postcode == 4680 or 4700 <= postcode <= 5299 or 5340 <= postcode <= 5765 or 5820 <= postcode <= 5846 or 6020 <= postcode <= 6029:
            return "https://www.omroepbrabant.nl/rss", "%a, %d %b %Y %H:%M:%S +0100"
        # Limburg
        case _ if 5766 <= postcode <= 5817 or 5850 <= postcode <= 6019 or 6030 <= postcode <= 6499 or 6584 <= postcode <= 6599:
            return "https://www.l1nieuws.nl/rss/index.xml", "%a, %d %b %Y %H:%M:%S %Z"
        # Overijssel
        case _ if 7400 <= postcode <= 7438 or 7440 <= postcode <= 7739 or 7767 <= postcode <= 7799 or 7950 <= postcode <= 7955 or 8000 <= postcode <= 8049 or 8055 <= postcode <= 8069 or 8100 <= postcode <= 8159 or 8196 <= postcode <= 8199 or 8260 <= postcode <= 8299 or 8323 <= postcode <= 8349 or 8355 <= postcode <= 8379:
            return "https://www.rtvoost.nl/rss", "%a, %d %b %Y %H:%M:%S %Z"
        # Drenthe
        case _ if 7740 <= postcode <= 7766 or 7800 <= postcode <= 7949 or 7956 <= postcode <= 7999 or 8350 <= postcode <= 8354 or 8380 <= postcode <= 8387 or 9400 <= postcode <= 9478 or 9480 <= postcode <= 9499 or 9510 <= postcode <= 9539 or postcode == 9564 or 9570 <= postcode <= 9579:
            return "https://www.rtvdrenthe.nl/rss", "%a, %d %b %Y %H:%M:%S %Z"
        # Friesland
        case _ if 8388 <= postcode <= 9299 or 9850 <= postcode <= 9859 or 9870 <= postcode <= 9879:
            return "https://www.omropfryslan.nl/rss/nieuws.xml", "%a, %d %b %Y %H:%M:%S %Z"
        # Groningen
        case _ if 9300 <= postcode <= 9349 or 9350 <= postcode <= 9399 or postcode == 9479 or postcode == 9500 or 9540 <= postcode <= 9563 or 9565 <= postcode <= 9569 or 9580 <= postcode <= 9653 or 9660 <= postcode <= 9748 or 9750 <= postcode <= 9759 or 9770 <= postcode <= 9849 or 9860 <= postcode <= 9869 or 9880 <= postcode <= 9999:
            return "https://www.rtvnoord.nl/rss/index.xml", "%a, %d %b %Y %H:%M:%S %Z"
        # Default case for unknown region
        case _:
            return None, None

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process zone and hours.")
    parser.add_argument('-z', '--zone', required=False, help="Specify the zone as a string")
    parser.add_argument('-t', '--hours', default=3, help="Specify the number of hours (default: 3)")
    parser.add_argument('-c', '--code', default=3, help="Specify the country code")
    parser.add_argument('--stdin', action='store_true', help="Read arguments from stdin")
    
    args, unknown = parser.parse_known_args()
    
    # If --stdin is passed, read input from stdin
    if args.stdin:
        input_line = sys.stdin.read().strip()  # Read stdin
        stdin_args = shlex.split(input_line)   # Safely split input into arguments
        return parser.parse_args(stdin_args)  # Re-parse the args
    
    return args

# Parse arguments
args = parse_arguments()

# Access the parsed arguments
zone = args.zone
hours = args.hours
code = args.code


if code.upper() == 'NL':
     tz = pytz.timezone('Europe/Amsterdam')
     if (zone == "s-Gravenhage" or zone.lower() == "den haag"):
         postal_code = 2502
     
     # Check if the zone matches the Dutch postal code format (4 digits and optional 2 letters)
     elif re.match(r"^\d{4}[A-Za-z]{0,2}$", zone):
         # If valid, just keep the first 4 digits (if there are extra letters)
         postal_code = zone[:4]
     else:
         postal_code = get_postal_code(to_camel_case(zone), code)
     rss_url, timestamp_format = get_local_news_rss_nl(postal_code)


else:
    print("Country not implemented");
    exit(1)


# Parse the RSS feed
feed = feedparser.parse(rss_url)

# Get the current time and the time based on the provided hours ago
now = datetime.now(tz)
hours = int(float(hours)) 
time_ago = now - timedelta(hours=hours)

# Initialize an empty list to store items published within the last 'hours' period
recent_items = []

for entry in feed.entries:
    # Convert pubDate to datetime object
    pub_date = datetime.strptime(entry.published, timestamp_format)
    pub_date = pub_date.replace(tzinfo=pytz.utc).astimezone(tz)
    
    # Check if the item was published within the specified hours period
    if pub_date > time_ago:
        item_info = {
            "title": entry.title,
            "link": entry.link,
            "description": entry.description if 'description' in entry else "",
            "pubDate": pub_date.isoformat()
        }
        recent_items.append(item_info)


# Return the result as JSON
result = json.dumps({"items": recent_items}, indent=4)
print(result)
