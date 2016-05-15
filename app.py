import os
import base64
import pyotp
import sqlite3

from twilio.rest import TwilioRestClient
from flask import request, session, jsonify
from gcm import GCM
import flask

app = flask.Flask(__name__)
app.secret_key = 'super secritzz'
DATABASE = './up4stuff.db'

gcm_api_key = os.environ['GCM_API_KEY']
account = os.environ['TWILIO_ACCOUNT_SID']
token = os.environ['TWILIO_AUTH_TOKEN']
num = "+1" + os.environ['TWILIO_NUMBER']
client = TwilioRestClient(account, token)

totp = pyotp.TOTP(pyotp.random_base32(), interval=120)


def is_valid_session(session):
    if 'phonenumber' in session and 'id' in session:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        try:
            cur.execute("select cookiekey from users where phone = '" +
                        session['phonenumber'] + "'")
            sesh = cur.fetchone()[0]
            if sesh == session['id']:
                return True
        except sqlite3.OperationalError, msg:
            conn.close()
            # return jsonify({'result': "sqlerror {0}".format(msg)})
            print "sqlerror {0}".format(msg)

        # return "{0}\n".format(escape(session['id']))
    else:
        print "Nae phone number or id i guess"
    return False


def generate_session():
    return base64.b64encode(os.urandom(16))


@app.route('/')
def hello_up4stuff():
    return 'We\'re Up 4 Stuff!'


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
        # return "Sent message to {0}!\n".format(phone)
        return jsonify({'result': "Sent message to {0}!".format(phone)})


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
                          "', verified = 1" + " where phone = " + phone)
             conn.commit()
         except sqlite3.OperationalError, msg:
            conn.close()
            return jsonify({'sqlerror': msg})
         return jsonify({'result': "YAS!"})
     else:
         return jsonify({'result': "BOO!"})


@app.route('/user/gcm', methods=['POST'])
def add_gcm():
    if 'phonenumber' in session and 'id' in session:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        try:
            cur.execute("select cookiekey from users where phone = '" +
                        session['phonenumber'] + "'")
            sesh = cur.fetchone()[0]
            if sesh == session['id']:
                gcm_token = request.form['gcm_token']
                conn.execute("update users set gcm_token = '" + gcm_token +
                             "' where phone = " + session['phonenumber'])
                conn.commit()
                return jsonify({'GCM': gcm_token})
            return jsonify({'result': "NAE AUTH MATE!"})
        except sqlite3.OperationalError, msg:
            conn.close()
            return jsonify({'result': "sqlerror {0}".format(msg)})

        # return "{0}\n".format(escape(session['id']))
    return "Dingie, nae auth mate!\n"


@app.route('/user/list')
def user_list():
    if is_valid_session(session):
        return jsonify({'result': "AUTH SESH!"})
    else:
        return jsonify({'result': "NAE AUTH MATE!"})


@app.route('/event/create', methods=['POST'])
def create_event():
    if is_valid_session(session):
        # print "IGOTZ {0}".format(request.get_json())
        # event_details = requests.get_json()
        broadcast_event(request.get_json())
        return jsonify({'result': "AUTH EVENTY!"})
    else:
        return jsonify({'result': "NAE EVENTY FOR YOU MATE!"})


def broadcast_event(details):
    print "BROADCASTING DETAILZ {0}".format(details)
    gcm = GCM(gcm_api_key)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    try:
        cur.execute("select gcm_token from users")
        tokey = cur.fetchone()[0]
    except sqlite3.OperationalError, msg:
        conn.close()
        print "BURNYEBUM {0}".format(msg)
    if tokey:
        print "TOKEY! {0}".format(tokey)
        registration_ids = [tokey]
        response = gcm.json_request(registration_ids=registration_ids,
                                    data=details)
        if response and 'success' in response:
            print "Yarly! successfully send an event!"
    else:
        print "NAE TOKEY!"


if __name__ == '__main__':
    app.run(debug=True)
