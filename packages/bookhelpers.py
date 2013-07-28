import requests
from models.book import Book
from connectdb import connect_db

def printLists(list):
	for item in list:
		print item
		print "\n"

def getDefaultValue(value):
	if type(value) is list:
		return []
	else:
		return ''

def addBookProperty(parentBook, book, keyToAdd, *searchKeys):
	try:
		for key in searchKeys:
			parentBook = parentBook[key]
	except KeyError, e:
		parentBook = getDefaultValue(parentBook)
	if keyToAdd != 'isbn':
		book.add(keyToAdd, parentBook)
	else:
		book.addBookISBN(parentBook)


def convert_json_to_POJO_list(booksJson):
	matchedBooks = []
	if booksJson['totalItems'] != 0:
		for book in booksJson['items']:
			b = Book()
			addBookProperty(book, b, 'isbn', 'volumeInfo', 'industryIdentifiers')
			addBookProperty(book, b, 'authors', 'volumeInfo', 'authors')
			addBookProperty(book, b, 'title', 'volumeInfo', 'title')
			addBookProperty(book, b, 'id', 'id')
			addBookProperty(book, b, 'description', 'volumeInfo', 'description')
			addBookProperty(book, b, 'pageCount', 'volumeInfo', 'pageCount')
			addBookProperty(book, b, 'rating', 'volumeInfo', 'averageRating')
			addBookProperty(book, b, 'thumbnail', 'volumeInfo', 'imageLinks', 'thumbnail')
			addBookProperty(book, b, 'publishedDate', 'volumeInfo', 'publishedDate')
			addBookProperty(book, b, 'publisher', 'volumeInfo', 'publisher')
			addBookProperty(book, b, 'language', 'volumeInfo', 'language')
			addBookProperty(book, b, 'previewLink', 'volumeInfo', 'previewLink')
			addBookProperty(book, b, 'country', 'saleInfo', 'country')
			b.add('availableQuantity', 2)
			matchedBooks.append(b)
	return matchedBooks

def retrieveBookByISBN(isbn):
	url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn + '&country=US'
	booksJson = requests.get(url).json()
	matchedBooks = convert_json_to_POJO_list(booksJson)		
	return matchedBooks


def retrieveBookByTitle(title):
	url = 'https://www.googleapis.com/books/v1/volumes?q=title:' + title + '&country=US'
	booksJson = requests.get(url).json()
	matchedBooks = convert_json_to_POJO_list(booksJson)		
	return matchedBooks

def retrieveBookByAuthor(author):
	url = 'https://www.googleapis.com/books/v1/volumes?q=author:' + author + '&country=US'
	booksJson = requests.get(url).json()
	matchedBooks = convert_json_to_POJO_list(booksJson)		
	return matchedBooks

def queryDBForBookByISBN(isbn):
	return connect_db().books.find_one({ 'book.isbn_13' : str(isbn)})

def updateBookQuantityAfterCheckout(isbn):
	db = connect_db().books
	db.update({'book.isbn_13': isbn}, {'$inc' : {'book.availableQuantity' : -1}})

	