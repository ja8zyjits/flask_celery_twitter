
testing = False

debug = True

secret_key = 'Super secret key'

session_type = 'filesystem'

image_destination = '/tmp/photolog'

if testing:
    backend_db = 'sqlite:////home/ja8zyjits/project/turbo_labs/test_db.db'
    server_name = 'localhost:5000'
    login_disabled = True
else:
    server_name = ''
    login_disabled = False
    backend_db = 'sqlite:////home/ja8zyjits/project/turbo_labs/production.db'



