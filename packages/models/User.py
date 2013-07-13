'''
Created on Jul 1, 2013

@author: Ameya
'''

class User:
    def __init__(self):
        self.user = {}

    def __str__(self):
        return str(self.user)

    def add(self, key, value):
        self.user[key] = value

    def getProperty(self, key):
        try:
            return self.user[key]
        except Exception, e:
            return None

