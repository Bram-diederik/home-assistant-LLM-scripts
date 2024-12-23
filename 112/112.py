#!/usr/bin/python3
import feedparser
import json
from datetime import datetime, timedelta
import shlex
import pytz
import sys
import argparse

def get_rss_url(zone):
    zone = zone.lower() 
    match zone:
        #ADDD OTHER CASES YOUR SELF
        # Amsterdam-Amstelland RSS feed
        case ("woonkamer"|"huiskamer"|"slaapkamer"|"studeerkamer"|"meterkast","amsterdam west" | "Station sloterdijk" | "vondelpark" | "amsterdam"|
              "amsterdam centrum"):
            return "http://alarmeringen.nl/feeds/region/amsterdam-amstelland.rss"

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process zone and hours.")
    parser.add_argument('-z', '--zone', required=False, help="Specify the zone as a string")
    parser.add_argument('-t', '--hours', default=3, help="Specify the number of hours (default: 3)")
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



# Set the timezone for proper time comparison
tz = pytz.timezone('Europe/Amsterdam')

# Get the RSS URL based on the zone
rss_url = get_rss_url(zone)

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
            "description": entry.description,
            "pubDate": pub_date.isoformat()
        }
        recent_items.append(item_info)

# Return the result as JSON
result = json.dumps({"items": recent_items}, indent=4)
print(result)
