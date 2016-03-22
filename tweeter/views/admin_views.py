"""The admin interface to look up the db"""
from tweeter import application, models
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


admin = Admin(application, name='Tweeeter', template_mode="bootstrap3")

admin.add_view(ModelView(models.Tweets, models.db.session))
admin.add_view(ModelView(models.KeyWords, models.db.session))