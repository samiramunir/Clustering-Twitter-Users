import json
from twitter import *
import time
import pandas as pd
import numpy as np
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




import time
import numpy as np

#Since the api calls for getting retweeters list takes a huge amount of time
#I wrote this script to collect each user info simultaneouly. So that by the time get_retweeter.py
#Completes the we will also have individual retweeter information.

### MAKE EMPTY DF To POPULATE WITH DATA ###########
total_tweets = pd.read_csv('data/nytimesposts.csv').shape[0]
file_path = 'data/retweeterinfo.csv'

df1 = pd.DataFrame(columns = ['tweet_id', 'retweeter_list', 'r_objects'])
df1.to_csv(file_path)

count = 0

while True:
    r = pd.read_csv('data/retweeterlist.csv')
    r2 = pd.read_csv(file_path)
    print('r shape:', r.shape, 'r2 shape:', r2.shape)

    i = r.shape[0]-r2.shape[0]
    print(f'r shape:{r.shape}',  f'r2 shape:{r2.shape},', f'i:{i}')

    if i == 0:
        #checking if retweeterlist for all NYT tweet has been collected or not. The loop breaks if true.
        if r.shape[0] == total_tweets:
            break

        print('wating 30 minutes for more data to populated into r')
        time.sleep(60*30)

        #re-reading the retweeterlist.csv file to get the latest rows
        r = pd.read_csv('data/retweeterlist.csv')
        i = r.shape[0]-r2.shape[0]
        print(f'r shape:{r.shape}',  f'r2 shape:{r2.shape},', f'i:{i}')

    # Separating the new rows in r that have not been looped over yet
    r3 = r.iloc[-i:, :]
    r3.reset_index(inplace=True)
    print(f'r3 shape:{r3.shape}')
    count = 0

    for i in range(r3.shape[0]):

        if count == 899:

            pp_json(twitter.application.rate_limit_status()["resources"]["users"]["/users/lookup"])
            print ("sleeping...")
            time.sleep(60*15)

            count = 0

        try:

            listy = eval(r3['retweeter_list'][i])
            count +=1
            # a list of retweeter objects
            retweeters = twitter.users.lookup(user_id=listy)
            mini_df = pd.DataFrame()
            mini_df['tweet_id'] = [r3.iloc[i, 1]]
            mini_df['retweeter_list'] = [r3.iloc[i, 2]]
            mini_df['r_objects'] = [json.dumps(retweeters)]
            mini_df.to_csv(file_path, mode='a', header=False)
            print('index:', i, 'no. of retweeter"s grabbed:', len(retweeters), 'out of', len(listy))

        except Exception as e:
            print(e)

            if type('TwitterHTTPError') == TwitterHTTPError:
                pp_json(twitter.application.rate_limit_status()["resources"]["users"]["/users/lookup"])
                print ("sleeping...")
                time.sleep(60*15)

            mini_df = pd.DataFrame()
            mini_df['tweet_id'] = [r3.iloc[i, 1]]
            mini_df['retweeterid'] = [r3.iloc[i, 2]]
            mini_df['r_objects'] = np.NaN
            mini_df.to_csv(file_path, mode='a', header=False)
            print('index:', i, 'none grabbed out of', len(listy))

    # Threw in another sleep just in case
    print('sleeping....')
    time.sleep(60*10)
