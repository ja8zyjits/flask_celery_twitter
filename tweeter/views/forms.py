""" The module used to define various forms """
from datetime import datetime
from flask_wtf import CsrfProtect, Form
from wtforms import StringField, validators, HiddenField
from tweeter import application
from flask import flash

CsrfProtect(application)

class AddKeyWordForm(Form):
    """Add new keyword"""
    streams = StringField('KeyWord', validators=[validators.Required()])

class EditKeyWordForm(AddKeyWordForm):
    """Edits the keywords"""
    id = HiddenField("keyword_id", validators=[validators.Optional()])


class StatisticsForm(EditKeyWordForm):
    """To get the statistics of a keyword"""
    from_time = StringField('From Time', validators=[validators.Required()])
    to_time = StringField('To Time', validators=[validators.Required()])

    def validate(self):
        try:
            f_time = datetime.strptime(self.from_time.data, "%H:%M")
            t_time = datetime.strptime(self.to_time.data, "%H:%M")
            if not f_time < t_time:
                flash("Error: The From time and To time is in wrong order")
                return False
        except ValueError:
            flash("Error: The time format is not proper")
            return False
        return True

