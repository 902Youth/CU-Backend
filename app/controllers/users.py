from flask import Blueprint, request
from db import db
from models.users import User
import bcrypt

# Create a Blueprint for the users routes
users = Blueprint('users', __name__)

# Utility functions

# Validates the request body for update or post requests
def _validate_user(body):
    return ('firstname' in body and 'lastname' in body  
    and 'username' in body and 'password' in body)

# Routes
@users.get('/')
def get_users():
    users = db.session.query(User).all()
    return [user._asdict() for user in users]
@users.post('/')
def create_user():
    body = request.json

    # Check if user already exists
    if db.session.query(User).filter(User.username == body['username']).first():
        return "User already exists", 400
    
    # Validate request body
    if not _validate_user(body):
        return "Missing required fields", 400

    # Salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(body['password'].encode('utf-8'), salt)
    
    # Add the new user to the database
    new_user = User(username=body['username'], hash=hashed_password, 
                    salt=salt, firstname=body['firstname'], lastname=body['lastname'])
    db.session.add(new_user)
    db.session.commit()
    
    return "User created"

@users.get('/<id>')
def get_user(id):
    user = db.get_or_404(User, id)
    return user

@users.put('/<id>')
def update_user(id):
    user = db.get_or_404(User, id)
    body = request.json

    # Validate request body
    if not _validate_user(body):
        return "Missing required fields", 400

    # Update user fields
    user.firstname = body['firstname']
    user.lastname = body['lastname']
    user.username = body['username']
    salt = bcrypt.gensalt()
    user.hash = bcrypt.hashpw(body['password'].encode('utf-8'), salt)

    db.session.commit()
    return f"Updated user with id {id}"

@users.delete('/<id>')
def delete_user(id):
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()
    return f"Deleted user with id {id}"