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




df= pd.read_csv('data/nytimesposts.csv')

# #####################################################################
# ### MAKE EMPTY DF To POPULATE WITH DATA ###########
file_path = 'data/retweeterlist.csv'

df1 = pd.DataFrame(columns = ['tweet_id', 'retweeter_list'])
df1.to_csv(file_path)



skipped = [] #for the indexes skipped due to exception
for i in range(df.shape[0]):
    try:
        mini_df = pd.DataFrame()
        r = twitter.statuses.retweeters.ids( _id=df.iloc[i, 2])['ids']
        mini_df['tweet_id'] = [df.iloc[i, 2]]
        mini_df['retweeter_list'] = [r]
        mini_df.to_csv(file_path, mode='a', header=False)
        print(f'index:{i}',  f'retweeter count:{len(r)}', 'original retweeter count:', df.iloc[i, 5])
    except Exception as e:
        skipped.append(i)
        print(e)
        print ("sleeping...")
        pp_json(twitter.application.rate_limit_status()["resources"]["statuses"]["/statuses/retweeters/ids"])
        time.sleep(60*15)
#
time.sleep(60*10)

# skipped = [28, 104, 180, 256, 332, 408, 484, 560, 636, 712, 788, 864, 940, 1016, 1092, 1168, 1244, 1320, 1396, 1472, 1548, 1624, 1700, 1776, 1852, 1928, 2004, 2080, 2156, 2232, 2308, 2384, 2460, 2536, 2612, 2688, 2764, 2840, 2916, 2992, 3068, 3144, 3220]
#RUNNING AGAIN FOR THE INDEXES SKIPPED
for i in skipped:
    try:
        mini_df = pd.DataFrame()
        r = twitter.statuses.retweeters.ids( _id=df.iloc[i, 2])['ids']
        mini_df['tweet_id'] = [df.iloc[i, 2]]
        mini_df['retweeter_list'] = [r]
        mini_df.to_csv(file_path, mode='a', header=False)
        print(f'index:{i}',  f'retweeter count:{len(r)}', 'original retweeter count:', df.iloc[i, 5])
    except Exception as e:
        skipped.append(i)
        print(e)
        print ("sleeping...")
        pp_json(twitter.application.rate_limit_status()["resources"]["statuses"]["/statuses/retweeters/ids"])
        time.sleep(60*15)

df1 = pd.read_csv(file_path)

print('no. of posts in new df:', df1.shape[0])

print('*****DONE******')
print('****YOU ARE AWESOME ****')
