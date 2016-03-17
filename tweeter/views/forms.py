from flask_wtf import CsrfProtect
from tweeter import application

CsrfProtect(application)