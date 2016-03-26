import sqlite3
from flask import Flask
app = Flask(__name__)

DATABASE = './up4stuff.db'


@app.route('/')
def hello_up4stuff():
    return 'We\'re Up 4 Stuff!'


@app.route('/help')
def help():
    return 'Commands:<br>/user/create/<username></br>/usr/validate/<username>'


@app.route('/user/create/<username>')
def create_user(username):
    return "%s created successfully" % username


if __name__ == '__main__':
    app.run()
