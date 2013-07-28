'''
Created on Jul 26, 2013

@author: Ameya
'''
from models.User import User
from connectdb import connect_db
from flask import flash
from settings import CHECKOUT_LIMIT

def check_if_user_is_authenticated(session):
    if 'username' not in session:
        flash('You are not signed in. Please sign in to continue', 'error')
        return False
    return True

def convertToUserPOJO(userFromDB):
    return User(userFromDB['user'])

def getNewUser(request):
    newUser = User()
    newUser.add('name', request.form['name'])
    newUser.add('email', request.form['email'])
    newUser.add('username', request.form['username'])
    newUser.add('password', request.form['password'])
    newUser.add('bookLimit', CHECKOUT_LIMIT)
    newUser.add('booksCheckedOut', [])
    newUser.add('isAdmin', False)
    newUser.add('isRedFlagged', False)
    return newUser

def getNumberOfBooksCheckedOutForUser(username):
    db = connect_db().users
    user = convertToUserPOJO(db.find_one({'user.username': username}))
    booksCheckedOut = user.getProperty('booksCheckedOut')
    if booksCheckedOut == None:
        return 0
    else:
        return len(booksCheckedOut)
    
    
def updateUserCheckedOutBooks(username, book):
    db = connect_db().users
    db.update({'user.username' : username}, { '$push' : {'user.booksCheckedOut' : book} }, True )