# [TWITTERAPP](#markdown-header-twitterapp)

Twitter App is a multiprocess architectured twitter streaming api user that can read multiple streams and update the details into the db. Primarily based on [flask](http://flask.pocoo.org/) behind a [tornado](http://www.tornadoweb.org/en/stable/) container for asynchronous connection along with [celery](http://docs.celeryproject.org/en/latest/) for job distribution, [tweepy](http://www.tweepy.org/) for twitter api and [flask-sqlalchemy](http://flask-sqlalchemy.pocoo.org/2.1/) for database connection. We use a simple sqllite database for running this app, we can use another database too by changing the url in tweeter/settings.py .

#### [Features](#markdown-header-features)
----
  - Add new keywords to the stream.
  - Update the keywords.
  - Celery based streaming task to fetch the tweets.
  - Multiprocess and distributed.

#### [Setting Up](#markdown-header-setting-up)
----
Just follow these basic steps to start the server in *development mode*.

1. Use the requirements.txt to install all the dependencies.

        pip install -r requirements.txt

2. Run the database intializer

		python database_init.py

3. Run the application script

		python run_application.py

4. Run the celery worker

                python -A tweeter.views.flask_tasks worker

5. Open the browser and go to http://127.0.0.1:5000/add_keyword

#### [Methodology](#markdown-header-methodology)
----

1. The basic request handle is handled by flask

2. To perform twitter streaming we use tweepy library.

3. We use celery to initiate the api using all the cpus/processors and doing parallel api requesting.

4. Sqlalchemy is used to communicate with db.

#### [Problems](#markdown-header-problems)
----

- [x] The timestamp of the system and the local network timestamp should be same or else you may get 401 error form the twitter network, it took me a while to realize that it was the time stamp and not the api keys that resulted in 401 authentication error

- [x] While using multiple processors parallely and trying to stream, the twitter may return 420 rate limiting error, but further it doesn't respond, it happens only initially

- [ ] [flask-sqlalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)  creates only a single scope per request and they cannot be shared properly accross multiple processes, this leads to partial db update i.e only one process of celery updates the db and others dont.

#### [Future](#markdown-header-future)
----

- [ ] Need to add views for capturing statistics about the tweets of each keyword
- [ ] Need to use tornado broadcast to post everytime a new tweet arrives from the stream to the front-end

#### [Contributors](#markdown-header-contributors)
----
- Jitesh Nair [mail](mailto:nairjitesh8@gmail.com)
