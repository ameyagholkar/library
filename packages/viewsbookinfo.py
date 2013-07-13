#!/usr/bin/python
import re
from flask import render_template, request, flash, session, redirect, url_for
from packages import app
from bookhelpers import retrieveBookByISBN, retrieveBookByTitle, retrieveBookByAuthor
from connectdb import connect_db
from models.book import Book
from packages.Wrappers import needs_authentication
from packages.authenticate import check_authentication

@app.route('/search/<isbn>')
def searchBookByISBN(isbn):
	error = None
	matchedBooks = retrieveBookByISBN(isbn)
	if len(matchedBooks) == 0:
		error = 'No matching books found. Please try another ISBN number.'
	return render_template('addbook.html', booksFound=matchedBooks, error=error)


@app.route('/search', methods=['GET', 'POST'])
def search_books():
	if check_authentication(session):
		query = request.form['query']
		isbn = text = None
		googleTitle = "Matching Books on our Shelf"
		error = None
		isISBN = False
		resultBookList = []
		try:
			isbn = int(query)
			isISBN =  True
			bookList = connect_db().books.find({ 'book.isbn_13' : str(isbn)})
		except ValueError:
			text = query
			regx = re.compile(".*" + text + ".*", re.IGNORECASE)
			bookList = connect_db().books.find({ "$or" : [
														{"book.title" : { "$regex" : regx} },
														{"book.description" : { "$regex" : regx} },
														{"book.authors" : { "$in" : { "$regex" : regx } } }
											   ] })
		for b in bookList:
			bookPOJO = Book(b['book'])
			if bookPOJO not in resultBookList:
				resultBookList.append(bookPOJO)
	
		if len(resultBookList) == 0:
			flash("No matching books found on our shelf.", 'error')
			googleTitle = "Matching Books found on Earth"
			(resultBookList, error) = search_books_on_google(query, isISBN)
			return render_template('addbook.html', booksFound=resultBookList, googleTitle=googleTitle, error=error)
				
		return render_template('checkoutbook.html', booksFound=resultBookList, googleTitle=googleTitle, error=error)
	else:
		return redirect(url_for('show_all_books'))


def search_books_on_google(query, isISBN):
	print"Calling mybaap Google"
	matchedBooks = []
	error = None
	if isISBN:
		matchedBooks = retrieveBookByISBN(query)
	else:
		matchedBooks = (retrieveBookByTitle(query) + retrieveBookByAuthor(query))
		
	if len(matchedBooks) == 0:
		error = 'No matching books found on Earth! Seems you want a rare book.'
	return matchedBooks, error

