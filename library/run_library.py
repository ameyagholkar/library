#!/usr/bin/python

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.pymongo import PyMongo
from pymongo import Connection
from connectdb import connect_db


app = Flask(__name__)

import viewsbookinfo
if __name__ == '__main__':
	app.run(debug=True)
