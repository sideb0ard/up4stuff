import sqlite3
import os
from twilio.rest import TwilioRestClient
from flask import Flask, request
app = Flask(__name__)

DATABASE = './up4stuff.db'
account = os.environ['TWILIO_ACCOUNT_SID']
token = os.environ['TWILIO_AUTH_TOKEN']
num = "+1" + os.environ['TWILIO_NUMBER']
client = TwilioRestClient(account, token)


@app.route('/')
def hello_up4stuff():
    return 'We\'re Up 4 Stuff!'


@app.route('/help')
def help():
    return 'Commands:<br>POST /user/create/?username=<name>&phonenumber=<numz>'


@app.route('/user/validate', methods=['POST', 'GET'])
def user_validate():
    if request.method == 'GET':
        return "Use a POST with phonenumber please.."
    else:
        # TODO - validate phonenumber
        phone = request.form['phonenumber']
        message = client.messages.create(to=phone, from_=num,
                                         body="Hello Dere!")
        return "Send message to {0}!\n".format(phone)


@app.route('/user/create', methods=['POST', 'GET'])
def user_create():
    # error = None
    if request.method == 'GET':
        return "Use a POST with username and phonenumber please.."
    else:
        username = request.form['username']
        phone = request.form['phonenumber']
        conn = sqlite3.connect(DATABASE)
        # conn.execute("INSERT INTO USERS (NAME) VALUES(" + username + ")")
        try:
            conn.execute("insert into users(name, phone) values('" + username +
                         "', " + phone + ")")
            conn.commit()
        except sqlite3.OperationalError, msg:
            conn.close()
            return msg
        conn.close()
        return "you successfully created {0} with {1}\n".format(username,
                                                                phone)


@app.route('/user/list')
def user_list():
    return "Users:"


if __name__ == '__main__':
    app.run(debug=True)
