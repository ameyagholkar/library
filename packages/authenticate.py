#!/usr/bin/python
from flask import render_template, request, flash, redirect, url_for, session
from packages import app
from connectdb import connect_db
from models.User import User


@app.route('/')
def home_page():
	return render_template('register.html')

@app.route('/new/register', methods=['POST'])
def register_new_user():
	db = connect_db().users
	newUser = User()
	newUser.add('name', request.form['name'])
	newUser.add('email', request.form['email'])
	newUser.add('username', request.form['username'])
	newUser.add('password', request.form['password'])
	existingUser = db.find_one({'user.username' : newUser.getProperty('username')})
	if existingUser == None:
		db.insert(newUser.__dict__)
	else:
		flash("User by that username already exists. Please select a different username.", 'error')
		return render_template('register.html')
	return render_template('login.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/login/do', methods=['POST'])
def authenticate():
	db = connect_db().users
	existingUser = db.find_one({'user.username' : request.form['username']})
	if existingUser != None and existingUser['user']['password'] == request.form['password']:
		flash('Logged in successfully!', 'success')
		session['username'] = request.form['username']
		return redirect(url_for('show_all_books'))
	else:
		flash('Oops! Incorrect username or password.', 'error')
		return render_template('login.html')


@app.route('/logout')
def logout():
	session.pop('username')
	flash('Logged out successfully!', 'success')
	return redirect(url_for('show_all_books'))


def check_authentication(session):
	if 'username' not in session:
		flash('You are not signed in. Please sign in to continue', 'error')
		return False
	return True