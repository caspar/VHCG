from flask import Blueprint, Flask, request, render_template, g, redirect, Response, flash, session
from . import db

SECRET_KEY = 'password'.encode('utf8')

auth = Blueprint('auth', __name__)

@admin.route('/admin_panel')
def admin_panel():
    return render_template("admin_panel.html")

# @auth.route('/signup')
# def signup():
#     return 'Signup'

# @auth.route('/logout')
# def logout():
#     session.pop('uid', None)
    