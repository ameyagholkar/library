#!/usr/bin/python
from flask import Flask
app = Flask(__name__)
import viewsbookinfo
import authenticate
import addbook
import showshelf
import errorhandlers


