from flask import Flask, session, render_template, jsonify, request, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
from db import db
from controllers.auth import auth
load_dotenv() # Loads environment variables from .env file

import jwt
from datetime import datetime, timedelta
from functools import wraps


# Create a Flask application
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config['SECRET_KEY'] = '89f210f05f874915ad4e347ice71ce7f6454'
CORS(app)

app.register_blueprint(auth)


db.init_app(app)
jwt.init_app(app)


def welcome():
    return "Welcome to the API!"

# Run the Flask application
if __name__ == '__main__':
    # Run the app on localhost (127.0.0.1) and port 3000
    app.run(host='127.0.0.1', port=3000)
