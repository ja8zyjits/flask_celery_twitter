from tweeter import application
from tweeter.models import KeyWords

@application.route("/")
def index():
    return "Success"