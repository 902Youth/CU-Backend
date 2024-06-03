from flask import Flask, session, render_template, jsonify, request, make_response, redirect, url_for, flash, Blueprint, Response
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
import datetime
import jwt
from functools import wraps
from App import SECRET_KEY



from methods.pwstrength import get_password_strength

import db

# used for the structured json reponses that are returned on successful or unsuccessful login, logout, or signup
from methods.jsonmessages import create_sucess_response, create_error_reponse

#used to establish the current state of login
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


#create a jwt token function for login and sign up
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') or request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithm='HS256')
            current_user = User.query.get(data['user_id'])
        except Exception as e:
            return jsonify({'message': 'Token is invalid'}), 403
        
        return f(current_user, *args, **kwargs)
    return decorated


# redirect login to home page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        user = None
        if(email):
            user = User.query.filter_by(email=email).first()
        elif(username):
            user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            token = generate_token(user.id)
            login_user(user, remember=True)
            response = Response.objects.create({
                'status_code': 200,
                'status': 'success',
                'data' : user,
            })
            return response
        response = Response.objects.create({
            'status_code': 401,
            'status': 'unathorized',
            'message': 'Invalid login credentials, Try again.'
        })
        
        

        
    # return a json object, either error or success

    #return redirect(url_for('home.html'), user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    print('Logout Successful')
    return 


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        confirm_email = request.form.get('confirmemail')
        username = request.form.get('username')
        fullname = request.form.get('fullname')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmpassword')

        # check if user is currently in the database using a query search on the email
        # insert block here
        user = User.query.filter_by(email=email).first()
        if user is not None:
            user = User.query.filter_by(username=user.username).first()
        
        found_in_common = False
        # check to see if all secure conditions
        if (get_password_strength(password) == str):
            found_in_common = True
        else:
            upper_case, lower_case, special, digits = get_password_strength(password)


        # check to see if user is already in the database
        if user:
            print('Email already exists.')

        # check if emails match
        elif email != confirm_email:
            print('Emails do not match')

        # check conditions for password
        elif len(email) < 4:
            print('Email must be atleast 4 characters.')
        
        # check the name conditions, 2 letters for first name, one for space,
        elif (fullname < 5):
            print('Full name must be atleast 5 characters.')
        
        elif found_in_common:
            print('Your password is prone to security vulnerabilities, as it was found in a common passwords database.')

        # check password match
        elif password != confirm_password:
            print('Password must match.')

        elif password.isalpha() == True:
            print('Password must have atleast one number in password')
        
        elif password.isdigit():
            print('Password must have atleast one number in the password')

        elif len(password) < 8:
            print('Password must be atleast 8 characters.')

        #all conditions must be met for password validation
        elif upper_case == 0:
            print('Password must include at least one upper case character.')
        elif lower_case == 0:
            print('Password must include at least one lower case character.')
        elif special == 0:
            print('Password must contain at least one special character.')
        elif digits == 0:
            print('Password must include at least one digit.')
    

        else:
            #create new user
            new_user = User(email=email, username=username, fullname=fullname, password=generate_password_hash(password, 'sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            print('User created successfully.')
            return jsonify(create_sucess_response)

    return render_template('sign_up.html', user=current_user)


