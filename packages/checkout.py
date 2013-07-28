'''
Created on Jul 26, 2013

@author: Ameya
'''
from flask import session, redirect, url_for
from packages import app
from errorhandlers import redirectHandlerWithFlashMessage
from userhelpers import getNumberOfBooksCheckedOutForUser, check_if_user_is_authenticated, updateUserCheckedOutBooks
from packages.settings import CHECKOUT_LIMIT
from bookhelpers import queryDBForBookByISBN, updateBookQuantityAfterCheckout

@app.route('/checkout/<isbn>', methods=['GET', 'POST'])
def doCheckout(isbn):
    if check_if_user_is_authenticated(session):
        username = session['username']
        numOfBooksCheckedOut = getNumberOfBooksCheckedOutForUser(username)
        if numOfBooksCheckedOut >= CHECKOUT_LIMIT:
            return redirectHandlerWithFlashMessage('show_all_books', 'You have reached your checkout limit. Please contact the library supervisor for assistance.', 'error')
        else:
            toCheckoutBook = queryDBForBookByISBN(isbn)
            if toCheckoutBook == None:
                return redirectHandlerWithFlashMessage('show_all_books', 'No book by the ISBN ' + str(isbn) + ' found on our shelf.', 'error')

            updateUserCheckedOutBooks(username, toCheckoutBook['book'])
            updateBookQuantityAfterCheckout(isbn)
            return "Checking out book by ISBN: " + str(isbn) + " Currently " + session['username'] + " has checked out " + str(getNumberOfBooksCheckedOutForUser(username)) + " books."
    else:
        return redirect(url_for('show_all_books'))
