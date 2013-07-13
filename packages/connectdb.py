#!/usr/bin/python
from pymongo import Connection

def connect_db():
	conn = Connection('localhost', 27017)
	db = conn['library']
	return db