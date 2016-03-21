
testing = False

debug = True

secret_key = 'Super secret key'

session_type = 'filesystem'

image_destination = '/tmp/photolog'

if testing:
    backend_db = 'sqlite:////home/jitesh/testing/tweepy_testing/test_db.db'
    server_name = 'localhost:5000'
    login_disabled = True
else:
    server_name = ''
    login_disabled = False
    backend_db = 'sqlite:////home/jitesh/testing/tweepy_testing/production.db'

celery_broker = 'sqla+sqlite:////home/jitesh/testing/tweepy_testing/celery_broker.db'

