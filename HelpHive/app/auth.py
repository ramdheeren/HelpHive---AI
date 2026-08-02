from flask import Blueprint, render_template, request, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from .db import db


auth = Blueprint('auth', __name__)

@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
    
        email = request.form.get('email').lower()
        phone = request.form.get('phone')
        password = request.form.get('password')
        re_password = request.form.get('confirm-password')
        first_name = request.form.get('first-name').capitalize()
        last_name = request.form.get('last-name').capitalize()
        goal = request.form.get('primary-goal')
        
        if goal == "volunteer":
            goal = 'True'
            skills = request.form.get('skills')
            radius = request.form.get('radius')
            days = request.form.get('days')
            location = ""  # get current location of user from frontend
        else:
            skills = 'None'
            radius = 'None'
            days = 'None'
            location = 'None'
            
        if db['users'].find_one({'email': email}):
            return 'account-alerady-exists'
        
        if password != re_password:
            return 'bad-password-match'
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        db['users'].insert_one(
            {
                'email': email,
                'phone': phone,
                'password': hashed_password,
                'first_name': first_name,
                'last_name': last_name,
                'is_volunteer': goal,
                'skills': skills,
                'radius': radius,
                'days': days,
                'location': location
            }
        )
        
        user = User(
            email=email,
            phone=phone,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            is_volunteer=goal,
            skills=skills,
            radius=radius,
            days=days
        )
        
        login_user(user)
        
        return redirect(url_for('views.home'))
    
    return 'Page under construction'
        


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        lat = data.get('latitude')
        lon = data.get('longitude')
        
        email = request.form.get('email').lower()
        password = request.form.get('password')
        
        user_details = db['users'].find_one({'email': email})

        if not user_details:
            return 'account-does-not-exist'
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        if not check_password_hash(user_details['password'], hashed_password):
            return 'bad-password'
        
        user = User(
            email=email,
            phone=user_details['phone'],
            password=user_details['password'],
            first_name=user_details['first_name'],
            last_name=user_details['last_name'],
            is_volunteer=user_details['is_volunteer'],
            skills=user_details['skills'],
            radius=user_details['radius'],
            days=user_details['days'],
            location=[lat, lon]
        )
        login_user(user)
        
        return redirect(url_for('views.home'))
    
    return 'Page under construction'


@auth.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('views.home'))
        


