import datetime
import binascii
import uuid
from flask import Flask, session, render_template, jsonify, request, make_response, redirect, url_for, flash, Blueprint, Response
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from dotenv import load_dotenv
import os
import datetime
import jwt
import re
from methods.pwstrength import get_password_strength

# used for the structured json reponses that are returned on successful or unsuccessful login, logout, or signup
from methods.jsonmessages import create_success_response, create_error_reponse
#used to establish the current state of login
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session




load_dotenv()
auth = Blueprint('auth', __name__)

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL, echo=False)
Session = scoped_session(sessionmaker(bind=engine))


db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
}

def get_db_connection():
    return Session()

def generate_token(username):
    #avoid circular import
    from App import app
    SECRET_KEY = app.config['SECRET_KEY']
    payload = {
        'user_id' : username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token




# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.args.get('token') or request.headers.get('Authorization')

#         if not token:
#             return jsonify({'message': 'Token is missing'}), 403
        
#         try:
#             data = jwt.decode(token, auth.config['SECRET_KEY'], algorithm='HS256')
#             current_user = User.query.get(data['user_id'])
#         except Exception as e:
#             return jsonify({'message': 'Token is invalid'}), 403
        
#         return f(current_user, *args, **kwargs)
#     return decorated


# redirect login to home page
@auth.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        session = get_db_connection()


        print(username, password)
        user = None

        if(email):
            user = session.query(User).filter_by(email=email).first()
        elif(username):
            user = session.query(User).filter_by(username=username).first()
        print(user.username, user.fullname, user.email)
        
        
        if user.verify_user(password=password):
            try: 
                token = generate_token(user.id)
                #login_user(user, remember=True)

                auth_token = generate_token(user.id)
                response_data = {
                    'status': 'success',
                    'message': f'{user.username} successfully logged in.',
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'username': user.username,
                        'fullname': user.fullname,
                    },
                    'auth_token': auth_token
                }
                status_code = 200
                response = make_response(jsonify(response_data), status_code)
                response.headers['Content-Type'] = 'application/json'
                # try: 
                #     user.lastLogin = datetime.datetime.now()
                #     session.add(user)
                #     session.commit()

                #     return response, status_code
                # except Exception as e:
                #     return jsonify({'status': 'fail', 'message': e.message}), 400
                return response                                                                       
            except Exception as e:
                return jsonify({'status': 'fail', 'message': e}), 400
        else:
            return jsonify({'status': 'fail', 'message': 'Incorrect password'}), 400


# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     response = Response.objects.create({
#         'status_code' : 200,
#         'status' : 'successful',
#         'message' : 'Logged out successfully',
#     })
#     return response


#function to check email validity
def validate_email(email):
    return bool(re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email))



@auth.route('/sign_up', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        confirm_email = request.form.get('confirmemail')
        username = request.form.get('username')
        fullname = request.form.get('fullname')
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmpassword')



        # establish connection to database
        session = get_db_connection()
        
        # get the cursor for the first search term
        #cursor = session.cursor(dictionary=True)
        try: 
        # target the email address
            existing_email = session.query(User).filter_by(email=email).first()
            existing_username = session.query(User).filter_by(username=username).first()
            existing_mobile = session.query(User).filter_by(mobile=mobile).first()


            print(existing_email, existing_username, existing_mobile)


            # cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
            # existing_email = cursor.fetchone()
            # target the username
            # cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            # existing_username = cursor.fetchone()
            # target the mobile phone number
            # cursor.execute("SELECT * FROM user WHERE mobile = %s", (mobile,))
            # existing_mobile = cursor.fetchone()
    

            # Perform basic validation
            if not email or not username or not password or not confirm_password:
                return jsonify({'status': 'fail', 'message': 'Missing required fields'}), 400

            if email != confirm_email:
                return jsonify({'status': 'fail', 'message': 'Emails do not match'}), 400

            if password != confirm_password:
                return jsonify({'status': 'fail', 'message': 'Passwords do not match'}), 400
            

            upper_case, lower_case, special, digits, is_common= get_password_strength(password)
            if is_common:
                return jsonify({'status': 'fail', 'message': 'Password is too common, please try again.'}), 400
                
            if len(password) < 8:
                return jsonify({'status': 'fail', 'message': 'Password must be atleast 8 characters long'}), 400

            if (validate_email(email) == False):
                return jsonify({'status': 'fail', 'message': 'Email is not valid'}), 400

            if upper_case == 0:
                return jsonify({'status': 'fail', 'message': 'Must include atleast one upper case character'}), 400
            
            if lower_case == 0:
                return jsonify({'status': 'fail', 'message': 'Must include atleast one lower case character'}), 400
            
            if digits == 0:
                return jsonify({'status': 'fail', 'message': 'Must include atleast one digit'}), 400
            
            if special == 0:
                return jsonify({'status': 'fail', 'message': 'Must include atleast one special character eg. #'}), 400
            
            if mobile.isdigit() == False:
                return jsonify({'status': 'fail', 'message': 'Phone number must be all numbers example: (1234567890)'}), 400
            
            if len(mobile) != 10:
                return jsonify({'status': 'fail', 'message': 'mobile must be 10 characters'})
            
            if (existing_email):
                return jsonify({'status': 'fail', 'message': 'User with email already exists'}), 400
            if (existing_username):
                return jsonify({'status': 'fail', 'message': 'Username already exists'}), 400
            if (existing_mobile):
                return jsonify({'status': 'fail', 'message': 'User with mobile number already exists'}), 400



        
            # Assuming the user is successfully created and authenticated
            new_user = User(fullname=fullname, mobile=mobile, username=username, email=email, hash=password)

            # # logic for inserting a new user into database

        
            session.add(new_user)
            session.commit()

            user_id = new_user.id
            auth_token = generate_token(user_id)


            response_data = {
                'status': 'success',
                'message': 'User successfully registered',
                'user': {
                    'id': new_user.id,
                    'email': new_user.email,
                    'username': new_user.username,
                    'fullname': new_user.fullname,
                    'mobile': new_user.mobile,
                },
                'auth_token': auth_token
            }
            status_code = 201
            response = make_response(jsonify(response_data), status_code)
            response.headers['Content-Type'] = 'application/json'

            # login_user(new_user)
            session.close()
            return response

        except Exception as e:
            return jsonify({'status': 'error', 'message': e}), 400
        
        # cursor.close()
        # connection.close()

        

        # check if user is currently in the database using a query search on the email
        # insert block here
        # user = User.query.filter_by(email=email).first()
        # if user is not None:
        #     user = User.query.filter_by(username=user.username).first()
        
        # found_in_common = False
        # # check to see if all secure conditions
        # if (get_password_strength(password) == str):
        #     found_in_common = True
        # else:
        #     upper_case, lower_case, special, digits = get_password_strength(password)


        # # check to see if user is already in the database
        # if user:
        #     print('Email already exists.')

        # # check if emails match
        # elif email != confirm_email:
        #     print('Emails do not match')

        # # check conditions for password
        # elif len(email) < 4:
        #     print('Email must be atleast 4 characters.')
        
        
    

        # else:
        #     #create new user
        #     new_user = User(email=email, username=username, fullname=fullname, password=generate_password_hash(password, 'sha256'))
        #     db.session.add(new_user)
        #     db.session.commit()
        #     login_user(new_user, remember=True)
        #     print('User created successfully.')
        #     return jsonify(create_success_response)


