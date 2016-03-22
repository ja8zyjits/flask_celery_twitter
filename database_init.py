"""THe module to be run before the first execution of the application"""
from tweeter.models import db

db.create_all()
