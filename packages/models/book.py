#!/usr/bin/python
from flask import url_for

class Book:
	def __init__(self, *args):
		if len(args) == 0:
			self.book = {}
		else:
			self.__new_book(args[0])

	def __new_book(self, book):
		self.book = book

	def __str__(self):
		return str(self.book)

	def add(self, key, value):
		if key == 'thumbnail' and value == '':
			self.book[key] = url_for('static', filename='noimage.jpg')
		else:
			self.book[key] = value

	def getBookProperty(self, key):
		try:
			return self.book[key]
		except Exception, e:
			return None

	def addBookISBN(self, isbn_list):
		for isbn in isbn_list:
			self.add(isbn['type'].lower(), isbn['identifier'])

