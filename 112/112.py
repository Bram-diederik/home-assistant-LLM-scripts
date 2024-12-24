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
        #print(data)

        # Adjust based on the actual response structure
        try:
            if 'results' in data and len(data['results']) > 0:
                postal_code = data['results'][0]['postal_code']
                return postal_code
            else:
                return f"No postal code found for {town}, {country_code}."
        except KeyError as e:
            return f"Error accessing key {e} in the response."
    else:
        return f"Error: {response.status_code}"

def get_rss_url_nl(postcode):
    try:
        postcode = int(str(postcode)[:4])  # Pak de eerste 4 cijfers van de postcode
    except ValueError:
        return None  # Ongeldige postcode
    
    match postcode:
        # Achterhoek
        case _ if 7000 <= postcode <= 7100:
            return "http://alarmeringen.nl/feeds/region/achterhoek.rss"
        
        # Amsterdam-Amstelland
        case _ if 1000 <= postcode <= 1099:
            return "http://alarmeringen.nl/feeds/region/amsterdam-amstelland.rss"
        
        # Bollenstreek
        case _ if 2200 <= postcode <= 2250:
            return "http://alarmeringen.nl/feeds/region/bollenstreek.rss"
        
        # Brabant-Noord
        case _ if 5200 <= postcode <= 5299:
            return "http://alarmeringen.nl/feeds/region/brabant-noord.rss"
        
        # Brabant-Zuidoost
        case _ if 5600 <= postcode <= 5699:
            return "http://alarmeringen.nl/feeds/region/brabant-zuidoost.rss"
        
        # Drenthe
        case _ if 7700 <= postcode <= 7999:
            return "http://alarmeringen.nl/feeds/region/drenthe.rss"
        
        # Flevoland
        case _ if 8200 <= postcode <= 8299:
            return "http://alarmeringen.nl/feeds/region/flevoland.rss"
        
        # Friesland
        case _ if 8400 <= postcode <= 9299:
            return "http://alarmeringen.nl/feeds/region/friesland.rss"
        
        # Gelderland Midden
        case _ if 6800 <= postcode <= 6899:
            return "http://alarmeringen.nl/feeds/region/gelderland-midden.rss"
        
        # Gelderland-Zuid
        case _ if 6500 <= postcode <= 6599:
            return "http://alarmeringen.nl/feeds/region/gelderland-zuid.rss"
        
        # Gooi en Vechtstreek
        case _ if 1200 <= postcode <= 1299:
            return "http://alarmeringen.nl/feeds/region/gooi-en-vechtstreek.rss"
        
        # Groningen
        case _ if 9700 <= postcode <= 9999:
            return "http://alarmeringen.nl/feeds/region/groningen.rss"
        
        # Haaglanden
        case _ if 2500 <= postcode <= 2599:
            return "http://alarmeringen.nl/feeds/region/haaglanden.rss"
        
        # Hoeksche Waard
        case _ if 3200 <= postcode <= 3299:
            return "http://alarmeringen.nl/feeds/region/hoeksche-waard.rss"
        
        # Hollands Midden
        case _ if 2300 <= postcode <= 2399:
            return "http://alarmeringen.nl/feeds/region/hollands-midden.rss"
        
        # IJsselland
        case _ if 8000 <= postcode <= 8299:
            return "http://alarmeringen.nl/feeds/region/ijsselland.rss"
        
        # Kennemerland
        case _ if 2000 <= postcode <= 2199:
            return "http://alarmeringen.nl/feeds/region/kennemerland.rss"
        
        # Limburg Noord
        case _ if 5900 <= postcode <= 5999:
            return "http://alarmeringen.nl/feeds/region/limburg-noord.rss"
        
        # Limburg Zuid
        case _ if 6000 <= postcode <= 6299:
            return "http://alarmeringen.nl/feeds/region/limburg-zuid.rss"
        
        # Midden- en West-Brabant
        case _ if 4800 <= postcode <= 5199:
            return "http://alarmeringen.nl/feeds/region/midden-en-west-brabant.rss"
        
        # Noord en Oost-Gelderland
        case _ if 7200 <= postcode <= 7499:
            return "http://alarmeringen.nl/feeds/region/noord-en-oost-gelderland.rss"
        
        # Noord-Holland Noord
        case _ if 1600 <= postcode <= 1899:
            return "http://alarmeringen.nl/feeds/region/noord-holland-noord.rss"
        
        # Rotterdam-Rijnmond
        case _ if 3000 <= postcode <= 3199:
            return "http://alarmeringen.nl/feeds/region/rotterdam-rijnmond.rss"
        
        # Twente
        case _ if 7500 <= postcode <= 7699:
            return "http://alarmeringen.nl/feeds/region/twente.rss"
        
        # Utrecht
        case _ if 3400 <= postcode <= 3999:
            return "http://alarmeringen.nl/feeds/region/utrecht.rss"
        
        # Zaanstreek-Waterland
        case _ if 1500 <= postcode <= 1599:
            return "http://alarmeringen.nl/feeds/region/zaanstreek-waterland.rss"
        
        # Zeeland
        case _ if 4300 <= postcode <= 4599:
            return "http://alarmeringen.nl/feeds/region/zeeland.rss"
        
        # Zuid-Holland Zuid
        case _ if 3300 <= postcode <= 3399:
            return "http://alarmeringen.nl/feeds/region/zuid-holland-zuid.rss"
        
        # Gouda (added)
        case _ if 2800 <= postcode <= 2899:
            return "http://alarmeringen.nl/feeds/region/zuid-holland-zuid.rss"
        
        # Onbekende regio
        case _:
            return None



def parse_arguments():
    parser = argparse.ArgumentParser(description="Process zone and hours.")
    parser.add_argument('-z', '--zone', help="Specify the postal code or town")
    parser.add_argument('-t', '--hours', default=3, help="Specify the number of hours (default: 3)")
    parser.add_argument('-c', '--code', help="Specify the country code")
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
     # Check if the zone matches the Dutch postal code format (4 digits and optional 2 letters)
     if re.match(r"^\d{4}[A-Za-z]{0,2}$", zone):
         # If valid, just keep the first 4 digits (if there are extra letters)
         postal_code = zone[:4]
     else:
         postal_code = get_postal_code(to_camel_case(zone), code)
     rss_url = get_rss_url_nl(postal_code)
else:
    print("Country not implemented");
    exit(1)


#print(rss_url);
# Parse the RSS feed
feed = feedparser.parse(rss_url)

# Get the current time and the time based on the provided hours ago
now = datetime.now(tz)
hours = int(float(hours)) 
time_ago = now - timedelta(hours=hours)

# Initialize an empty list to store items published within the last 'hours' period
recent_items = []

# Iterate over the feed entries and filter by publication time
for entry in feed.entries:
    # Convert pubDate to datetime object
    pub_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S +0000")
    pub_date = pub_date.replace(tzinfo=pytz.utc).astimezone(tz)
    
    # Check if the item was published within the specified hours period
    if pub_date > time_ago:
        item_info = {
            "title": entry.title,
            "link": entry.link,
            "description": getattr(entry, 'description', ''),
            "pubDate": pub_date.isoformat()
        }
        recent_items.append(item_info)

# Return the result as JSON
result = json.dumps({"items": recent_items}, indent=4)
print(result)
