from flask import request, url_for, render_template, redirect

from tweeter import application
from tweeter.models import KeyWords, db
from tweeter.views.forms import AddKeyWordForm
from celery import group
from tweeter.views.celery_tasks import stream_tweets, save_tweets

@application.route("/")
def index():
    return "Success"

@application.route('/add_keyword', methods=['GET', 'POST'])
def add_keyword():
    keyword_form = AddKeyWordForm()
    key_words = KeyWords.query.all()
    if request.method == 'POST':
        if keyword_form.validate_on_submit():
            new_keyword()
            return redirect(url_for('add_keyword'))
    return render_template("add_keyword.html", form=keyword_form, key_words=key_words)

def new_keyword():
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
    job = None
    
    @staticmethod
    def reset_celery():
        if TweeterTask.job:
            TweeterTask.stop_tasks()
        TweeterTask.start_tasks()

    @staticmethod
    def stop_tasks():
        TweeterTask.job.revoke(terminate=True)

    @staticmethod
    def start_tasks():
        tasks = group(stream_tweets.s(keyword) for keyword in get_active_keywords())
        TweeterTask.job = tasks.apply_async()

def get_active_keywords():
    return KeyWords.query.filter(KeyWords.active == True)

def update_tweets(key_word, tweet, user, generated_time):
    key_word_id = get_key_word_id(key_word)
    

def get_key_word_id(keyword):
    key_word = KeyWords.query.filter(KeyWords.stream == keyword).first()
    return key_word.id