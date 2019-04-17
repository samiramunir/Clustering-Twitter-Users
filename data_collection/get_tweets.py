import json
from twitter import *
import time
import pandas as pd
import os


#-----------------------------------------------------------------------
# load our API credentials  from the config.py file
#-----------------------------------------------------------------------
config = {}
exec(open('config.py').read(), config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

#function to parse twitter JSON
#json.loads : Parse JSON - Convert from JSON to Python
#json.dumps : Convert from Python to JSON

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None

if not 'data' in os.listdir():
    os.mkdir('data')

#setting the earliest date of tweets to be grabbed. Set it to one day before the date you want.
# So that all posts of that particular day is grabbed. However,  twitter api only allows around 3200 posts to be collected for one particular account. So the loop is designed to break once that number is reached which could happen depending on your settings, before the earliest date is reached.

earliest_date = 'Jan 17'
screen_name = 'nytimes'
file_path = 'data/nytimesposts.csv'

#####################################################################
### MAKE EMPTY DF To POPULATE WITH DATA ###########

df = pd.DataFrame(columns = ['created_at', 'tweet_id', 'text', 'url', 'retweet_count', 'status'])
df.to_csv(file_path)


#-----------------------------------------------------------------------
# loop through each of newsoutlet statuses, and print its content
#-----------------------------------------------------------------------
count = 0
last_id = 0
_continue = True
posts_collected = 0

while True:
 # Make API CALL
    try:

        if last_id == 0:
            count +=1
            print('request', count)
            data = twitter.statuses.user_timeline(screen_name=screen_name, count=200)
        else:
            if _continue == False:
                print (f'DONE! All posts collected till {earliest_date}, 2019')
                break

            count +=1
            print('request', count)
            print('lastid', last_id)
            data = twitter.statuses.user_timeline(screen_name=screen_name, max_id = last_id-1, count=200)

        if len(data) == 0:
            #twitter API only allows around 3200 tweets to be collected for one particular user. After maxing out it returns an empty list.
            print (f'Maximum number of posts for one user reached, total no. of posts collected: {posts_collected}')
            break

        last_id = data[-1]['id']

    except Exception as E:
        print(E)
        pp_json(twitter.application.rate_limit_status()["resources"]["statuses"]["/statuses/user_timeline"])
        print ("sleeping...")
        time.sleep(60*15)

    #check how many posts grabbed
    posts_collected += len(data)
    print('Total posts collected:', posts_collected)

    # Loop through the statuses to get information and populated df
    for status in data:
        if earliest_date in status['created_at']:
            _continue = False
            break

        mini_df = pd.DataFrame()
        mini_df['created_at'] = [status['created_at']]
        mini_df['tweet_id'] = [status['id']]
        mini_df['text'] = [status['text']]
        mini_df['url'] =  [status['user']['entities']['description']['urls'][0]['expanded_url']]
        mini_df['retweet_count'] = [status['retweet_count']]
        mini_df['status'] = [json.dumps(status)]
        mini_df.to_csv(file_path, mode='a', header=False)
