#!/usr/bin/python

from flask import render_template
from packages import app
from connectdb import connect_db
from models.book import Book

@app.route('/shelf', methods=['GET', 'POST'])
def show_all_books():
	bookList = connect_db().books.find()
	displayBookList = []
	for b in bookList:
		displayBookList.append(Book(b['book']))
	return render_template('checkoutbook.html', booksFound=displayBookList)


