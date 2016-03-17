from flask import Flask


application = Flask(__name__)

import tweeter.config
import tweeter.views