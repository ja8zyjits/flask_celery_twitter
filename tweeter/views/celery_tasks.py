"""celery task class, need to  run this seperately to make the app update tweets propely"""

from celery import Celery
from tweeter import application
from tweeter.views.tweepy_task import create_streamer


celery_init = Celery('tweeter')
celery_init.config_from_object(application.config)

@celery_init.task
def stream_tweets(keyword):
    """streams tweets with the twitter api leveraging multiple cores"""
    with application.test_request_context() as request:
        keywords = keyword.split(' ')
        stream = create_streamer(keyword)
        stream.filter(track=keywords, async=True)

