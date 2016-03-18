from celery import Celery
from tweeter import application
import time


celery_init = Celery('tweeter')
celery_init.config_from_object(application.config)

@celery_init.task
def find_sum():
    with application.test_request_context() as request:
        print 'hello', request
        time.sleep(4)
        return 1+2
