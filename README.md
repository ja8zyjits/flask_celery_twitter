# [TWITTERAPP](#markdown-header-twitterapp)

Twitter App is a multiprocess architectured twitter streaming api user that can read multiple streams and update the details into the db. Primarily based on [flask](http://flask.pocoo.org/) behind a tornado container for asynchronous connection.

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

4. Open the browser and go to http://127.0.0.1:5000/add_keyword

#### [Contributors](#markdown-header-contributors)
----
- Jitesh Nair [mail](mailto:nairjitesh8@gmail.com)