'''
Created on Jul 2, 2013

@author: Pheonix
'''
from packages import app
from flask import render_template

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def ise(e):
    return render_template('500.html'), 500