from flask import request, url_for, render_template, redirect

from tweeter import application
from tweeter.models import KeyWords, db
from tweeter.views.forms import AddKeyWordForm

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

