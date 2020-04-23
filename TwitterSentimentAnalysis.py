import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    def __init__(self):
        ACCESS_TOKEN = '192754590-Ypri2v6C576aKdRnTLrSXAUev4f7Ue1RY9bs7GWH'
        ACCESS_SECRET = 'aeJzdAd1CoN0WYKNxH3x8xmCgfVRXIXXYS2LWzN3Zk0Sd'
        CONSUMER_KEY = 'dxcK2lyxZeT0b1YGRAj6KesG3'
        CONSUMER_SECRET = 'WIOc3N07WSjnd6QVYlAclYmYXBl1YQiOez8adevWUDcbSBlnM7'

        try:
                self.auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
                self.auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
                self.api = tweepy.API(self.auth)
        except:
                print("Error: Auth Failed")
                      
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):

        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
                return 'negative'
    def get_tweets(self, query, count = 10):
        tweets = []
        try:
                fetched_tweets = self.api.search(q = query, count = count)

                for tweet in fetched_tweets:
                    parsed_tweet = {}
                    parsed_tweet['text'] = tweet.text
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                    if tweet.retweet_count > 0:
                        if parsed_tweet not in tweets:
                            tweets.append(parsed_tweet)
                    else:
                            tweets.append(parsed_tweet)
                return tweets
        except tweepy.TweepError as e:
                print("Error: " + str(e))

def main ():
    api = TwitterClient()
    tweets = api.get_tweets(query = 'stimulus check', count = 500)
    
    ptweets = [tweet for tweet in tweets if tweet ['sentiment'] == 'positive']
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))

    ntweets = [tweet for tweet in tweets if tweet ['sentiment'] == 'negative']
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))

    print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))

    print("\n\nPositive tweets:")
    for tweet in ptweets[:40]:
          print("Tweet: " + tweet['text'])

    print("\n\nNegative tweets:")
    for tweet in ntweets[:40]:
        print("Tweet: " + tweet['text'])
        
if __name__ == "__main__":
    main()
    
        
