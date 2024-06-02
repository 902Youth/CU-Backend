from flask import Flask
import os
from models import *
from db import db
from controllers.users import users
from controllers.endorsements import endorsements
from controllers.jobs import jobs
from dotenv import load_dotenv

load_dotenv()

# Create a Flask application with db configuration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(endorsements, url_prefix='/endorsements')
app.register_blueprint(jobs, url_prefix='/jobs')
db.init_app(app)

# Define a route for the root URL
@app.route('/')
def welcome():
    return "Welcome to the API!"

# Run the Flask application
if __name__ == '__main__':
    # Create the database tables that don't exist
    with app.app_context():
        db.create_all()

    # Run the app on localhost (127.0.0.1) and port 3000
    app.run(host='127.0.0.1', port=3000, debug=True)
