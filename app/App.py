from flask import Flask, session, render_template, jsonify, request, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
from db import db
load_dotenv() # Loads environment variables from .env file

import jwt
from datetime import datetime, timedelta
from functools import wraps


# Create a Flask application
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config['SECRET_KEY'] = '89f210f05f874915ad4e347ice71ce7f6454'
CORS(app)


db.init_app(app)


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request/args.get('token')
        if not token:
            return jsonify({'Alert': 'Token is missing!'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'Alert': 'Invalid Token!'})
    return decorated

# Define a route for the root URL
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in currently'
    
@app.route('/public')
def public():
    return 'For Public'

@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified'

@app.route('/login', methods=['POST'])
def login():
    print(request.POST.get('/login'))
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True
        token = jwt.encode({
            'user' : request.form['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=120))
        
        },
        app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8')})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed!'})


def welcome():
    return "Welcome to the API!"

# Run the Flask application
if __name__ == '__main__':
    # Run the app on localhost (127.0.0.1) and port 3000
    app.run(host='127.0.0.1', port=3000)
