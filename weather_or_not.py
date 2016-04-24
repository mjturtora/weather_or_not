# all the imports
# using: http://flask.pocoo.org/docs/0.10/tutorial/setup/#tutorial-setup
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration
#DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'not key secret'
#USERNAME = 'admin'
#PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

if __name__ == '__main__':
    app.run()
