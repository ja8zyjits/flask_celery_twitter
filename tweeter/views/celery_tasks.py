from celery import Celery
from tweeter import application
from tweeter.views.tweepy_task import create_streamer
import time


celery_init = Celery('tweeter')
celery_init.config_from_object(application.config)

@celery_init.task
def stream_tweets(keyword):
    with application.test_request_context() as request:
        keywords = keyword.split(' ')
        stream = create_streamer(keyword)
        stream.filter(track=keywords, async=True)

