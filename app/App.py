
from flask import Flask, session, render_template, jsonify, request, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
from db import db
from controllers.auth import auth
from controllers.notifications import notifications
#load_dotenv() # Loads environment variables from .env file

import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask_login import LoginManager
from models.user import User


# from flask import Flask
# import os
# from models import *
# from db import db
# from controllers.users import users
# from controllers.endorsements import endorsements
# from controllers.jobs import jobs
# from dotenv import load_dotenv


load_dotenv()

# Create a Flask application with db configuration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


CORS(app)


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(notifications, url_prefix='/notifications')
#db.init_app(app)





# app.register_blueprint(users, url_prefix='/users')
# app.register_blueprint(endorsements, url_prefix='/endorsements')
# app.register_blueprint(jobs, url_prefix='/jobs')
db.init_app(app)


# def welcome():
#     return "Welcome to the API!"

# Run the Flask application
if __name__ == '__main__':
    # Create the database tables that don't exist
    with app.app_context():
        db.create_all()

    # Run the app on localhost (127.0.0.1) and port 3000
    app.run(host='127.0.0.1', port=3000, debug=True)
