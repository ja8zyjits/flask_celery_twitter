from tweeter import application
from tweeter.settings import debug, session_type, secret_key, backend_db,\
testing, server_name, login_disabled, image_destination

application.config['SECRET_KEY'] = secret_key
application.config['SESSION_TYPE'] = session_type
application.config['DEBUG'] = debug
application.config['SQLALCHEMY_DATABASE_URI'] = backend_db
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['TESTING'] = testing
application.config["UPLOADED_PHOTOS_DEST"] = image_destination
if server_name:
    application.config['SERVER_NAME'] = server_name
application.config['LOGIN_DISABLED'] = login_disabled
