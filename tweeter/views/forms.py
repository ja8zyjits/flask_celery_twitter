from flask_wtf import CsrfProtect, Form
from wtforms import StringField, validators
from tweeter import application

CsrfProtect(application)

class AddKeyWordForm(Form):
    """Add new keyword"""
    streams = StringField('KeyWord', validators=[validators.Required()])
