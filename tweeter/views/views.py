"""The db interaction and request processing module"""

from flask import request, url_for, render_template, redirect

from tweeter import application
from tweeter.models import KeyWords, db, Tweets
from tweeter.views.forms import AddKeyWordForm
from celery import group
from tweeter.views.celery_tasks import stream_tweets
from dateutil.parser import parse as date_parser

@application.route("/")
def index():
    """landing page"""
    return "Success"

@application.route('/add_keyword', methods=['GET', 'POST'])
def add_keyword():
    """ verifies and adds new keywords to the KeyWords table by calling new_keyword() method """
    keyword_form = AddKeyWordForm()
    key_words = KeyWords.query.all()
    if request.method == 'POST':
        if keyword_form.validate_on_submit():
            new_keyword()
            TweeterTask.reset_celery()
            return redirect(url_for('add_keyword'))
    return render_template("add_keyword.html", form=keyword_form, key_words=key_words)

def new_keyword():
    """ The function that adds the keyword to the db """
    try:
        keyword_form = AddKeyWordForm()
        key = KeyWords()
        keyword_form.populate_obj(key)
        db.session.add(key)
        db.session.commit()
        return True
    except Exception, e:
        return True

class TweeterTask():
    """Dummy class to keep related functions and variables in an organized manner"""
    job = None #The variable used to track the celery group tasks
    
    @staticmethod
    def reset_celery():
        """ stops and restarts the celery tasks """
        if TweeterTask.job:
            TweeterTask.stop_tasks()
        TweeterTask.start_tasks()

    @staticmethod
    def stop_tasks():
        """ stops the group tasks """
        TweeterTask.job.revoke(terminate=True)

    @staticmethod
    def start_tasks():
        """ Starts the celery group tasks """
        tasks = group(stream_tweets.s(keyword.streams) for keyword in get_active_keywords())
        TweeterTask.job = tasks.apply_async()

def get_active_keywords():
    """ queries the keywords that are not deleted/deactivated """
    return KeyWords.query.filter(KeyWords.active == True)

def update_tweets(key_word, tweet, user, generated_time):
    """updates the tweets streamed into the database"""
    key_word_id = get_key_word_id(key_word)
    insert_tweets(key_word_id, tweet, user, generated_time)

def get_key_word_id(keyword):
    """ gets the id of the keyword """
    key_word = KeyWords.query.filter(KeyWords.streams == keyword).first()
    return key_word.id

def insert_tweets(key_word_id, tweet, user, generated_time):
    """ Inserts a new tweet into the db mapping a foreign key to the
     keywords table with key_woord_id"""
    try:
        tweets = Tweets()
        tweets.keywords_id = key_word_id
        tweets.tweet = str(tweet)
        tweets.twitter_user = user
        tweets.tweet_generated_time = date_parser(generated_time)
        db.session.add(tweets)
        db.session.commit()
    except Exception, e:
        return False
