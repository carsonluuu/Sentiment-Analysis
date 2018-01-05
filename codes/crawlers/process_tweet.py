# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json
import urllib.request as urllib2
from time import strptime
import calendar
import numpy as np
import csv
# We use the file saved from last step as example
tweets_filename = 'stream_output.json'
tweets_file = open(tweets_filename, "r")
no_loc_file = open("no_location_records.json", "w")
ofile = open("result.csv", "a")
weather = dict()
fieldnames = ['DayOfWeek', 'Location', 'Temperature', '#retweets', '#followers', 'label']
writer = csv.DictWriter(ofile, fieldnames=fieldnames)
count = 0
def get_date(time):
    l = time.split()
    month = str(strptime(l[1], '%b').tm_mon)
    day = l[2]
    year = l[5]
    dow_abbr = list(calendar.day_abbr)
    dow = 0
    for i in range(7):
        if l[0] == dow_abbr[i]:
            dow = i
            break
    return [year, month, day, dow]

def get_woeid(name):
    base_url = "https://www.metaweather.com/api/location/search/?"
    sub = name.split()
    queries = ["query="+s for s in sub]
    query = "&".join(queries)
    url = base_url + query
    response = urllib2.urlopen(url)
    string = response.read().decode('utf-8')
    json_obj = json.loads(string)
    if len(json_obj) == 0:
        return None
    else:
        return(json_obj[0]['woeid'])
    
def get_temp(woeid, date):
    d = str(date[0]) + str(date[1]) + str(date[2])
    if weather.get((woeid, d)) is not None:
        return weather[(woeid, d)]
    base_url = "https://www.metaweather.com/api/location"
    url = '/'.join([base_url, str(woeid), date[0], date[1], date[2]])
    response = urllib2.urlopen(url)
    string = response.read().decode('utf-8')
    json_obj = json.loads(string)
    weather[(woeid, d)] = json_obj[0]['the_temp']
    return json_obj[0]['the_temp']

def one_hot(num, target):
    targets = np.array([target]).reshape(-1)
    one_hot_targets = np.eye(num)[targets]
    return one_hot_targets[0]

for line in tweets_file:
    try:
        # Read in one line of the file, convert it into a json object 
        tweet = json.loads(line.strip())
        if 'text' in tweet: # only messages contains 'text' field is a tweet
            time = tweet['created_at']
            location = tweet['place']['name']

            woeid = get_woeid(location)
            if woeid is None:
                no_loc_file.write(tweet)
                no_loc_file.write("\n")
                continue

            date = get_date(time)

            temp = get_temp(woeid, date)

            dow = one_hot(7, date[3])

            if location == "San Francisco":
                l = 0
            elif location == "Los Angeles":
                l = 1
            else:
                l = 2
            loc = one_hot(3, l)
            output = dict()
            output['DayOfWeek'] = dow
            output['Location'] = loc
            output['Temperature'] = temp
            output['#retweets'] = tweet['retweet_count']
            output['#followers'] = tweet['user']['followers_count']
            output['label'] = tweet['text'].replace('\n', ' ')
            print("..." + str(count) + " records...")
            writer.writerow(output)
            count += 1
    except:
        # read in a line is not in JSON format (sometimes error occured)
        continue
tweets_file.close()
no_loc_file.close()
ofile.close()
