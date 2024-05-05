from flask import Blueprint, request
from ..models.users import User

# Create a Blueprint for the users routes
users = Blueprint('users', __name__)

@users.get('/')
def get_users():
    return "Get all users"

@users.post('/')
def get_user():
    return "User created"

@users.get('/<int:id>')
def get_user(id):
    return f"Get user with id {id}"

@users.put('/<int:id>')
def update_user(id):
    return f"Update user with id {id}"

@users.delete('/<int:id>')
def delete_user(id):
    return f"Delete user with id {id}"




