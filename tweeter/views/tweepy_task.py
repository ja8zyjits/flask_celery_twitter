import json
from tweepy import StreamListener, OAuthHandler, Stream

ckey = "Z30OWOsTk80mRS17J4w2sGPZl"
csecret = "ljRQphsoO7c030nCss4iPgPFRIFQuumM2PAHLVvAVZrr7SFNuF"

atoken = "4753351087-Ofzx5ikg1CCz0bx7m5CKjT2q7NFdSRkj1X9MpZ0"
asecret = "T5bJXWpv9xHheQ6begRMmOtGfkVB1p2QddM66DJ7GW4jK"

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)


class MyStreamer(StreamListener):

    def __init__(self, key_word=None, *args, **kwargs):
        super(MyStreamer, self).__init__(*args, **kwargs)
        self.key_word = key_word
    
    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data['text']
        username = all_data["user"]["screen_name"]
        tweet_generated_at = all_data["created_at"]
        self.update_db(self.key_word, tweet, username, tweet_generated_at)
        # print tweet, '####', username, '#####', tweet_generated_at, "###3", self.key_word
        print tweet,"tweet"
        return True
    
    def on_error(self, status):
        print status
        return False

    def update_db(self, key_word, tweet, user, generated_time):
        from tweeter.views.views import update_tweets
        update_tweets(key_word, tweet, user, generated_time)



# listener = MyStreamer()
# listener.key_word = "kohli pakistan"

# myst =  Stream(auth=auth, listener=listener)

# myst.filter(track=["kohli","pakistan"])

def create_streamer(key_words):
    listener = MyStreamer()
    listener.key_word = key_words
    myst = Stream(auth=auth, listener=listener)
    return myst
