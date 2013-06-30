#!/usr/bin/python
from flask import Flask
app = Flask(__name__)
import library.viewsbookinfo
import library.authenticate
import library.addbook
import library.showshelf


