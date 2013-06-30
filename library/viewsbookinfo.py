#!/usr/bin/python
from flask import render_template, url_for, flash
from library import app
from bookhelpers import *

@app.route('/testBookApi/<isbn>')
def searchBookByISBN(isbn):
	error = None
	matchedBooks = retrieveBookByISBN(isbn)
	printLists(matchedBooks)
	if len(matchedBooks) == 0:
		error = 'No matching books found. Please try another ISBN number.'
	return render_template('addbook.html', booksFound=matchedBooks, error=error)


