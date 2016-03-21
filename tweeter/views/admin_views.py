from tweeter import application
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from tweeter import models


admin = Admin(application, name='Tweeeter', template_mode="bootstrap3")

admin.add_view(ModelView(models.Tweets, models.db.session))
admin.add_view(ModelView(models.KeyWords, models.db.session))