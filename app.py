import os
import pyotp
import sqlite3

#from flask_inputs import Inputs
#from flask_wtf import Form
#from wtforms import StringField
#from wtforms.validators import DataRequired
#
from twilio.rest import TwilioRestClient
from flask import Flask, request, jsonify
#app = Flask(__name__)
import flask
app = flask.Flask(__name__)
app.secret_key = 'super secritzz'

import flask.ext.login as flask_login

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'thor@thor.com': {'pw': 'secret'}}

totp = pyotp.TOTP(pyotp.random_base32(), interval=120)

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user


DATABASE = './up4stuff.db'
account = os.environ['TWILIO_ACCOUNT_SID']
token = os.environ['TWILIO_AUTH_TOKEN']
num = "+1" + os.environ['TWILIO_NUMBER']
client = TwilioRestClient(account, token)




#class UserInputs(Form):
#    phonenumber = StringField('phonenumber', validators=[DataRequired()])
#

@app.route('/')
def hello_up4stuff():
    return 'We\'re Up 4 Stuff!'


#@app.route('/help')
#def help():
#    return 'Commands:<br>POST /user/create/?username=<name>&phonenumber=<numz>'
#

@app.route('/user/validate', methods=['POST', 'GET'])
def user_validate():
     phone = request.form['phonenumber']
     token = request.form['token']
     if totp.verify(token):
         return "YAS!\n"
     else:
         return "BOO!\n"



@app.route('/user/create', methods=['POST', 'GET'])
def user_create():
    # error = None
    if request.method == 'GET':
        return "Use a POST with phonenumber please.."
    else:
        phone = request.form['phonenumber']
        conn = sqlite3.connect(DATABASE)
        #conn.execute("INSERT INTO USERS (NAME) VALUES(" + username + ")")
        try:
            conn.execute("insert into users(phone) values(" + phone + ")") 
            conn.commit()
        except sqlite3.OperationalError, msg:
            conn.close()
            return msg
        conn.close()
        # TODO - validate phonenumber
        code = totp.now()
        message = client.messages.create(to=phone, from_=num,
                body="OTP: {0}".format(code))
        return "Send message to {0}!\n".format(phone)


@app.route('/user/list')
def user_list():
    return "Users:"


@app.route('/login', methods=['POST'])
def login():
    email = flask.request.form['email']
    if flask.request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return "Logged in!"
    return 'Bad login\n'

if __name__ == '__main__':
    app.run(debug=True)
