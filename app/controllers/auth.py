from flask import Flask, session, render_template, jsonify, request, make_response, redirect, url_for, flash, Blueprint
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from methods import pwstrength
import db

from flask_login import login_user, login_required, logout_user, current_user

from App import app

auth = Blueprint('auth', __name__)

# redirect login to home page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        user = None
        login_error = None
        if(email):
            user = User.query.filter_by(email=email).first()
            login_error = 'email'
        else:
            user = User.query.filter_by(username=username).first()
            login_error = 'username'

        if user:
            if check_password_hash(user.password, password):
                flash('Login successful!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('home.html'))
            else:
                flash('Incorrect Password, try again', category='error')
        else:
            flash(f'Invalid {login_error}, please try again.', category='error')  
    
    return redirect(url_for('home.html'), user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout Successful', category='success')
    return redirect(url_for('auth.login'))


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
        

        # check to see if all secure conditions
        upper_case, lower_case, special, digits = pwstrength.get_password_strength(password)


        # check to see if user is already in the database
        if user:
            flash('Email already exists.', category='error')

        # check if emails match
        elif email != confirm_email:
            flash('Emails do not match', category='error')

        # check conditions for password
        elif len(email) < 4:
            flash('Email must be atleast 4 characters.', category='error')
        
        # check the name conditions, 2 letters for first name, one for space,
        elif (fullname < 5):
            flash('Full name must be atleast 5 characters.', category='error')
        
        # check password match
        elif password != confirm_password:
            flash('Password must match.', category='error')

        elif password.isalpha() == True:
            flash('Password must have atleast one number in password', category='error')
        
        elif password.isdigit():
            flash('Password must have atleast one number in the password', category='error')

        elif len(password) < 8:
            flash('Password must be atleast 8 characters.', category='error')

        #all conditions must be met for password validation
        elif upper_case == 0:
            flash('Password must include at least one upper case character.', category='error')
        elif lower_case == 0:
            flash('Password must include at least one lower case character.', category='error')
        elif special == 0:
            flash('Password must contain at least one special character.', category='error')
        elif digits == 0:
            flash('Password must include at least one digit.', category='error')
    

        else:
            #create new user
            new_user = User(email=email, username=username, fullname=fullname, password=generate_password_hash(password, 'sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created successfully.', category='success')
            redirect(url_for('view.home'))

    return render_template('sign_up.html', user=current_user)


