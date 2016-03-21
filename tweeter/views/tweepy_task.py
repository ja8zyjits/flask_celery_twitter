from tweepy import StreamListener, OAuthHandler, Stream
import json

ckey = "05e8fDRy7MR90tRRYKvyR03f7"
csecret = "KYqF4j2LkZkjFSnCC1zyjpo4pACIMKryI0XqB64sfGVbqKcFPu"

atoken = "4753351087-TUiLK8DJ3Iettlu4Z1uTxqCKzteRFVhEjLFd7cv"
asecret = "uIZYdyBlOTwPLQPpVFFJSyzwmP7lp0w5LhgWIQMNqmBkN"

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
        print tweet, "####", username, "####", tweet_generated_at, self.key_word, '\n'
        return True
    
    def on_error(self, status):
        print status
        return False

listener = MyStreamer()
listener.key_word = "kohli pakistan"

myst =  Stream(auth=auth, listener=listener)

myst.filter(track=["kohli","pakistan"])
