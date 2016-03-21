from celery import Celery
from tweeter import application
from application.views.tweepy_task import MyStreamer, auth, Stream
import time


celery_init = Celery('tweeter')
celery_init.config_from_object(application.config)

@celery_init.task
def find_sum():
    with application.test_request_context() as request:
        print 'hello', request
        time.sleep(4)
        return 1+2

@celery_init.task
def stream_tweets(keyword):
    with application.test_request_context() as request:
        keywords = keyword.split(' ')
        listner = MyStreamer()
        listner.key_word = keyword
        stream = Stream(auth, listner)
        stream.filter(track=keywords, async=True)

@celery_init.task
def save_tweets(key_word, tweet, user, generated_date):
    pass