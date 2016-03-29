import os
import base64
import pyotp
import sqlite3

from twilio.rest import TwilioRestClient
from flask import request, session, escape
import flask

app = flask.Flask(__name__)
app.secret_key = 'super secritzz'

totp = pyotp.TOTP(pyotp.random_base32(), interval=120)


def generate_session():
    return base64.b64encode(os.urandom(16))


DATABASE = './up4stuff.db'
account = os.environ['TWILIO_ACCOUNT_SID']
token = os.environ['TWILIO_AUTH_TOKEN']
num = "+1" + os.environ['TWILIO_NUMBER']
client = TwilioRestClient(account, token)


@app.route('/')
def hello_up4stuff():
    return 'We\'re Up 4 Stuff!'


@app.route('/user/validate', methods=['POST', 'GET'])
def user_validate():
     phone = request.form['phonenumber']
     token = request.form['token']
     if totp.verify(token):
         session['phonenumber'] = request.form['phonenumber']
         sesh_id = generate_session()
         session['id'] = sesh_id
         conn = sqlite3.connect(DATABASE)
         try:
             conn.execute("update users set cookiekey = '" + sesh_id +
                          "' where phone = " + phone)
             conn.commit()
         except sqlite3.OperationalError, msg:
            conn.close()
            return "sqlerrrrzzz: {0}".format(msg)
         return "YAS!\n"
     else:
         return "BOO!\n"


@app.route('/user/create', methods=['POST', 'GET'])
def user_create():
    if request.method == 'GET':
        return "Use a POST with phonenumber please.."
    else:
        phone = request.form['phonenumber']
        conn = sqlite3.connect(DATABASE)
        try:
            conn.execute("insert into users(phone) values(" + phone + ")")
            conn.commit()
        except sqlite3.OperationalError, msg:
            conn.close()
            return msg
        conn.close()
        # TODO - validate phonenumber
        code = totp.now()
        print("Code is {0}\n".format(code))
        client.messages.create(to=phone, from_=num,
                               body="OTP: {0}".format(code))
        return "Sent message to {0}!\n".format(phone)


@app.route('/user/list')
def user_list():
    if 'phonenumber' in session and 'id' in session:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        try:
            cur.execute("select cookiekey from users where phone = '" +
                        session['phonenumber'] + "'")
            sesh = cur.fetchone()[0]
            if sesh == session['id']:
                return "AUTH SESSH!\n"
            return "NAE AUTH MATE."
        except sqlite3.OperationalError, msg:
            conn.close()
            return msg
        return "{0}\n".format(escape(session['id']))
    return "Dingie, nae auth mate!\n"


if __name__ == '__main__':
    app.run(debug=True)
