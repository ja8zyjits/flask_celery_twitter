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

- [x] [flask-sqlalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)  creates only a single scope per request and they cannot be shared properly accross multiple processes, this leads to partial db update i.e only one process of celery updates the db and others dont.

- [x] Stopping an executing tasks in celery is not working, tried 

		resultset.revoke(terminate=True)

	This dint fire any error but failed to stop the tasks. Later I tried

		revoke(resultset.children[0].id, terminate=True)

	This fired an error Socket Error[111] connection refused

	```python
		Traceback (most recent call last):
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/flask/app.py", line 1836, in __call__
		    return self.wsgi_app(environ, start_response)
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/flask/app.py", line 1820, in wsgi_app
		    response = self.make_response(self.handle_exception(e))
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/flask/app.py", line 1403, in handle_exception
		    reraise(exc_type, exc_value, tb)
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/flask/app.py", line 1817, in wsgi_app
		    response = self.full_dispatch_request()
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/flask/app.py", line 1477, in full_dispatch_request
		    rv = self.handle_user_exception(e)
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/flask/app.py", line 1381, in handle_user_exception
		    reraise(exc_type, exc_value, tb)
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/flask/app.py", line 1475, in full_dispatch_request
		    rv = self.dispatch_request()
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/flask/app.py", line 1461, in dispatch_request
		    return self.view_functions[rule.endpoint](**req.view_args)
		  File "/home/ja8zyjits/project/turbo_labs/twitter_app/tweeter/views/views.py", line 45, in stop_celery
		    TweeterTask.stop_tasks()
		  File "/home/ja8zyjits/project/turbo_labs/twitter_app/tweeter/views/views.py", line 63, in stop_tasks
		    revoke(tasks.id, terminate=True)
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/celery/local.py", line 188, in __call__
		    return self._get_current_object()(*a, **kw)
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/celery/app/control.py", line 172, in revoke
		    'signal': signal}, **kwargs)
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/celery/app/control.py", line 316, in broadcast
		    limit, callback, channel=channel,
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/kombu/pidbox.py", line 283, in _broadcast
		    chan = channel or self.connection.default_channel
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/kombu/connection.py", line 757, in default_channel
		    self.connection
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/kombu/connection.py", line 742, in connection
		    self._connection = self._establish_connection()
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/kombu/connection.py", line 697, in _establish_connection
		    conn = self.transport.establish_connection()
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/kombu/transport/pyamqp.py", line 116, in establish_connection
		    conn = self.Connection(**opts)
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/amqp/connection.py", line 165, in __init__
		    self.transport = self.Transport(host, connect_timeout, ssl)
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/amqp/connection.py", line 186, in Transport
		    return create_transport(host, connect_timeout, ssl)
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/amqp/transport.py", line 299, in create_transport
		    return TCPTransport(host, connect_timeout)
		  File "/home/ja8zyjits/project/turbo_labs/lib/python2.7/site-packages/amqp/transport.py", line 95, in __init__
		    raise socket.error(last_err)
		error: [Errno 111] Connection refused
	```

- [ ] The celery control cannot revoke a task with sqlalchemy as broker. Need to find another way to revoke tasks.

#### [Future](#markdown-header-future)
----

- [ ] Need to add views for capturing statistics about the tweets of each keyword
- [ ] Need to use tornado broadcast to post everytime a new tweet arrives from the stream to the front-end

#### [Contributors](#markdown-header-contributors)
----
- Jitesh Nair [mail](mailto:nairjitesh8@gmail.com)
