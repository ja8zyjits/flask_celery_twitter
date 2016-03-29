"""The db interaction and request processing module"""

from flask import request, url_for, render_template, redirect, abort

from tweeter import application
from tweeter.models import KeyWords, db, Tweets
from tweeter.views.forms import AddKeyWordForm, EditKeyWordForm, StatisticsForm
from tweeter.views.celery_tasks import stream_tweets
from celery import group
from dateutil.parser import parse as date_parser

@application.route("/")
def index():
    """landing page"""
    return "Success"

@application.route('/add', methods=['GET', 'POST'])
def add():
    """ verifies and adds new keywords to the KeyWords table by calling new_keyword() method """
    keyword_form = AddKeyWordForm()
    key_words = get_active_keywords()
    if request.method == 'POST':
        if keyword_form.validate_on_submit():
            new_keyword()
            TweeterTask.reset_celery()
            return redirect(url_for('add'))
    return render_template("add_keyword.html", form=keyword_form, key_words=key_words)

def get_active_keywords():
    """ queries the keywords that are not deleted/deactivated """
    return KeyWords.query.filter(KeyWords.active == True)

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
        TweeterTask.stop_tasks()
        TweeterTask.start_tasks()

    @staticmethod
    def stop_tasks():
        """ stops the group tasks """
        if TweeterTask.job:
            for tasks in TweeterTask.job.children:
                tasks.revoke(terminate=True)

    @staticmethod
    def start_tasks():
        """ Starts the celery group tasks """
        tasks = group(stream_tweets.s(keyword.streams) for keyword in get_active_keywords())
        TweeterTask.job = tasks.apply_async()

@application.route('/stop_celery')
def stop_celery():
    TweeterTask.stop_tasks()
    return redirect(url_for('add'))

@application.route('/edit/<int:keyword_id>', methods=['GET', 'POST'])
def edit(keyword_id):
    """edit handler for the app"""
    try:
        keyword_obj = get_obj(KeyWords, keyword_id)
        if request.method == 'POST':
            keyword_form = EditKeyWordForm()
            if keyword_form.validate_on_submit():
                keyword_form.populate_obj(keyword_obj)
                status = save_obj(keyword_obj)
                if status:
                    return redirect(url_for('add'))
                else:
                    raise ValueError
        else:
            keyword_form = EditKeyWordForm(obj=keyword_obj)
    except ValueError:
        abort(404)
    else:
        return render_template('edit_keyword.html', form=keyword_form)


def get_obj(obj_class, obj_id):
    """gets the keyword_obj of a particular id from the db"""
    obj = obj_class.query.get(obj_id)
    if obj:
        return obj
    else:
        raise ValueError

def save_obj(obj):
    """saves an object"""
    try:
        db.session.add(obj)
        db.session.commit()
    except Exception, e:
        return False
    else:
        return True

@application.route('/delete', methods=['POST', 'GET'])
def delete():
    """ initiates the delete flag set on a keyword"""
    try:
        if request.method == 'POST':
            keyword_form = EditKeyWordForm()
            if keyword_form.validate_on_submit():
                keyword_obj = get_obj(KeyWords, keyword_form.id.data)
                status = delete_obj(keyword_obj)

                if not status:
                    raise ValueError
    except ValueError:
        abort(404)
    else:
        return redirect(url_for('add'))

def delete_obj(obj):
    """ sets the delete flag of a object """
    try:
        obj.active = False
        db.session.add(obj)
        db.session.commit()
    except Exception:
        return False
    else:
        return True

@application.route('/show_stats/<int:keyword_id>')
def show_stats(keyword_id):
    try:
        if request.method == 'POST':
            form = StatisticsForm()
        keyword_obj = get_obj(KeyWords, keyword_id)
        form = StatisticsForm(obj=keyword_obj)
        return render_template('statistics.html', form=form)

    except Exception, e:
        abort(404)

def update_tweets(session_obj, key_word, tweet, user, generated_time):
    """
    updates the tweets streamed into the database
    :param session_obj: A new scoped session object used to support mutliple
     transactions with sqlalchemy and multiprocess
    """
    key_word_id = get_key_word_id(session_obj, key_word)
    insert_tweets(session_obj, key_word_id, tweet, user, generated_time)

def get_key_word_id(session_obj, keyword):
    """
     gets the id of the keyword 
     :param session_obj: A new scoped session object used to support mutliple
     transactions with sqlalchemy and multiprocess
     """
    key_word = session_obj.query(KeyWords).filter(KeyWords.streams == keyword).first()
    return key_word.id

def insert_tweets(session_obj, key_word_id, tweet, user, generated_time):
    """ 
    Inserts a new tweet into the db mapping a foreign key to the
     keywords table with key_woord_id
     :param session_obj: A new scoped session object used to support mutliple
     transactions with sqlalchemy and multiprocess
     """
    try:
        tweets = Tweets()
        tweets.keywords_id = key_word_id
        tweets.tweet = tweet
        tweets.twitter_user = user
        tweets.tweet_generated_time = date_parser(generated_time)
        session_obj.add(tweets)
        session_obj.commit()
    except Exception, e:
        return False

