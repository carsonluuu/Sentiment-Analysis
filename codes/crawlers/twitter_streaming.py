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

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.filter(locations="-122.75,36.8,-121.75,37.8", language="en")

out_file = open("stream_output.json", "w")
# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 1000 tweets. 
# You don't have to set it to stop, but can continue running 
# the Twitter API to collect data for days or even longer. 
tweet_count = 10
for tweet in iterator:
    tweet_count -= 1
    # Twitter Python Tool wraps the data returned by Twitter 
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
    print("{} tweets to crawl".format(tweet_count))
    out_file.write(json.dumps(tweet))  
    out_file.write("\n")
    # The command below will do pretty printing for JSON data, try it out
    # print json.dumps(tweet, indent=4)
       
    if tweet_count <= 0:
        break 
