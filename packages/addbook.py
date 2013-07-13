#!/usr/bin/python
from flask import flash, url_for, redirect
from packages import app
from connectdb import connect_db
from bookhelpers import retrieveBookByISBN

@app.route('/add/<isbn>', methods=['GET', 'POST'])
def addToDBIfNotPresent(isbn):
	books = connect_db().books
	b = books.find_one({'book.isbn_13' : isbn})
	if b == None:
		bookList = retrieveBookByISBN(isbn)
		books.insert(bookList[0].__dict__)
		flash(bookList[0].getBookProperty('title') + ' is now available on our shelf!', 'info')
		return redirect(url_for('show_all_books'))
	else:
		flash(b['book']['title'] + ' already exists on our shelf!', 'error')
		return redirect(url_for('show_all_books'))
