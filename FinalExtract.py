import tweepy
import pandas as pd
from tabulate import tabulate

# Variables that contains the credentials to access Twitter API
ACCESS_TOKEN = '192754590-Ypri2v6C576aKdRnTLrSXAUev4f7Ue1RY9bs7GWH'
ACCESS_SECRET = 'aeJzdAd1CoN0WYKNxH3x8xmCgfVRXIXXYS2LWzN3Zk0Sd'
CONSUMER_KEY = 'dxcK2lyxZeT0b1YGRAj6KesG3'
CONSUMER_SECRET = 'WIOc3N07WSjnd6QVYlAclYmYXBl1YQiOez8adevWUDcbSBlnM7'


# Setup access to API
def connect_to_twitter_OAuth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth)
    return api


# Create API object
api = connect_to_twitter_OAuth()

# tweets from my stream
##public_tweets = api.home_timeline()
##for tweet in public_tweets:
##    print(tweet.text)

# tweets from a specific user
indiana_tweets = api.user_timeline(791598918)
#for tweet in indiana_tweets:
 #   print(tweet.text)

# Get the user object for Twitter
    ##user = api.get_user('apfledd')
    ##print(user.screen_name)
    ##print(user.followers_count)
    ##for friend in user.friends():
    ##    print(friend.screen_name)
    ##    
### fuction to extract data from tweet object
def extract_tweet_attributes(tweet_object):
    # create empty list
    tweet_list =[]
    # loop through tweet objects
    for tweet in tweet_object:
        tweet_id = tweet.id # unique integer identifier for tweet
        text = tweet.text # utf-8 text of tweet
        favorite_count = tweet.favorite_count
        retweet_count = tweet.retweet_count
        created_at = tweet.created_at # utc time tweet created
        source = tweet.source # utility used to post tweet
        reply_to_status = tweet.in_reply_to_status_id # if reply int of orginal tweet id
        reply_to_user = tweet.in_reply_to_screen_name # if reply original tweetes screenname
        retweets = tweet.retweet_count # number of times this tweet retweeted
        favorites = tweet.favorite_count # number of time this tweet liked
        # append attributes to list
        tweet_list.append({'tweet_id':tweet_id, 
                          'favorite_count':favorite_count,
                          'retweet_count':retweet_count,
                          'created_at':created_at, 
                         'source':source, 
                          'retweets':retweets,
                         'favorites':favorites})
    # create dataframe   
    df = pd.DataFrame(tweet_list, columns=['tweet_id',
                                           'created_at',
                                           'source',
                                           'retweets',
                                           'favorites'])
    #with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        #print(tabulate(df, headers='keys', tablefmt='psql'))
    writer = pd.ExcelWriter('TwitterData.xlsx')
    df.to_excel(writer,'MBB')
    writer.save()
    print('DataFrame is written successfully to Excel File.')
    
extract_tweet_attributes(indiana_tweets)

#Find tweets based on certain word
##query = "deals"
##language = "en"
##results = api.search(q=query,lang=language)
##for tweet in results:
##    print(tweet.user.screen_name,"Tweeted:",tweet.text)
