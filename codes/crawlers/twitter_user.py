# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '925228398363918336-btpd6lJcKkdBtmd2bjQr51cMYT4aNAG'
ACCESS_SECRET = 'T1QPY6edOPi9GA7sPjyRR6gJsNot65eGCO6HGAuWX2jq2'
CONSUMER_KEY = 'qLK1LPJfsLSeqSqybpXmEVo68'
CONSUMER_SECRET = 'ofjUokR46EkuP5lNMqqgtatjeaofvmixSX5lTgjgPmAbMQ8OSl'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter API
twitter = Twitter(auth=oauth)

file_name = open("screen_name.txt", "r")

for name in file_name:
    time_line = twitter.statuses.user_timeline(screen_name=name)
    for tweet in time_line:
        print(json.dumps(tweet))
