from flask import Blueprint, session
from . import db

SECRET_KEY = 'password'.encode('utf8')

auth = Blueprint('auth', __name__)

# @auth.route('/login')
# def login():
#     return 'Login'

# @auth.route('/signup')
# def signup():
#     return 'Signup'

# @auth.route('/logout')
# def logout():
#     session.pop('uid', None)
    