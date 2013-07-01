#!/usr/bin/python
from flask import flash, render_template, url_for, redirect
from library import app
from connectdb import connect_db
from bookhelpers import *

@app.route('/add/<isbn>', methods=['GET', 'POST'])
def addToDBIfNotPresent(isbn):
	books = connect_db().books
	b = books.find_one({'book.isbn_13' : isbn})
	print b
	if b == None:
		print "No such book found yet."
		bookList = retrieveBookByISBN(isbn)
		books.insert(bookList[0].__dict__)
		flash(bookList[0].getBookProperty('title') + ' is now available on our shelf!')
		return redirect(url_for('show_all_books'))
	else:
		flash(b['book']['title'] + ' already exists on our shelf!')
		return redirect(url_for('show_all_books'))
