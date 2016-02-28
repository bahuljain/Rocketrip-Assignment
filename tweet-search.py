import tweepy
import time
import sys
import random as r

# Decorator function for rate limiting function calls.
def RateLimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate

class Twitter:

    def __init__(self, consumer_key=None, consumer_secret=None):
        # Variables that contains the application-only credentials to access Twitter API
        if consumer_key is None:
            consumer_key = "Tq20eDbLhvBBGgK2jXcp8Faif"
        if consumer_secret is None:
            consumer_secret = "flSsRrcAJQCwgfbpnHbcPBy5bN9YexArVB5pYdHtdC25dbipO6"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(auth)

    '''
     In application-only auth, the application can make 450 queries/requests
     per 15 minutes or equivalently 1 query per 2 seconds.
    '''
    @RateLimited(0.5) # 1 query per 2 seconds
    def keyword_search(self, keyword=None):
        if keyword:
            print "Keyword: ", keyword
            try:
                result = self.api.search(q = keyword, rpp = 1)
                tweet = result[r.randint(0, len(result) - 1)]

                pretty_print_tweet(tweet)

                return tweet
            except tweepy.TweepError, err:
                err = err.message[0]
                print "Tweepy Error: " + `err['code']` + " - " +  err['message']
        else:
            print "'keyword' field required. Cannot be empty or null."

    def pretty_print_tweet(self, tweet=None):
        if tweet:
            try:
                text = tweet.text.encode('ascii', 'ignore')
                user_handle = "@" + tweet.author.screen_name

                print "User: ", user_handle
                print "Tweet: ", text
            except Exception as e:
                print e
            print ""
        else:
            print "'tweet' field required. Cannot be empty or null."


if __name__=="__main__":

    # Capture all the keywords passed as arguments in the prompt.
    keywords = sys.argv[1:]

    twitter = Twitter()

    for keyword in keywords:
        twitter.keyword_search(keyword)
