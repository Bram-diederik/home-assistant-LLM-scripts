#!/usr/bin/python3
import feedparser
import json
from datetime import datetime, timedelta
import pytz
import argparse
import sys
import shlex

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process hours.")
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
hours = args.hours


tz = pytz.timezone('Europe/Amsterdam')

rss_url = "https://www.nu.nl/rss/Buitenland";

# Parse the RSS feed
feed = feedparser.parse(rss_url)

# Get the current time and the time one hour ago
now = datetime.now(tz)
hours = int(float(hours)) 
time_ago = now - timedelta(hours=hours)

# Initialize an empty list to store items published within the last hour
recent_items = []

# Iterate over the feed entries and filter by publication time
for entry in feed.entries:
    # Convert pubDate to datetime object
    pub_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S +0100")
    pub_date = pub_date.replace(tzinfo=pytz.utc).astimezone(tz)
    
    # Check if the item was published within the last hour
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
