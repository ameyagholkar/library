#!/usr/bin/python
from flask import render_template, request
from library import app
from connectdb import connect_db


@app.route('/')
def home_page():
	return "Library Management System"


@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/login/do', methods=['POST'])
def authenticate():
	return "Logged " + request.form['username']


@app.route('/logout')
def logout():
	return "Logged out."