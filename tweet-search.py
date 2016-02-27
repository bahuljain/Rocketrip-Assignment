import tweepy
import time

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
        #Variables that contains the application-only credentials to access Twitter API
        if consumer_key is None:
            consumer_key = "Tq20eDbLhvBBGgK2jXcp8Faif"
        if consumer_secret is None:
            consumer_secret = "flSsRrcAJQCwgfbpnHbcPBy5bN9YexArVB5pYdHtdC25dbipO6"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(auth)

    # In application-only auth, the application can make 450 queries/requests
    # per 15 minutes or equivalently 30 queries per minute.
    @RateLimited(0.5) # 1 query per 2 seconds
    def keyword_search(self, keyword):
        print keyword


if __name__=="__main__":
    twitter = Twitter()

    for i in range(1,11):
        twitter.keyword_search("Nigga")
