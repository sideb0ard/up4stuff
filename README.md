# Up 4 Stuff reboot!

## Python/Flask API server, Mac Users, instructions:::::

### Flask API

Grab this code:  
`git clone git@github.com:sideb0ard/up4stuff.git`

`cd up4stuff`

Ensure you have virtualenv installed, then create a new Python environment:  
`virtualenv venv`

Activate the env:  
`source venv/bin/activate`

Install requirements files:  
`pip install -r requirements.txt`

### Database
Run `./dbstuff.py` to create a local sqlite3 DB.  

### Environment variables
No credentials are stored in the code, so you need to make your creds available via local environment variables:  
export TWILIO_ACCOUNT_SID=XXXXXXXXXXXXXXXXXXX  
export TWILIO_AUTH_TOKEN=XXXXXXXXXXXXXXXXXXXX  
export TWILIO_NUMBER=XXXXXXXXXXXXXXXXXXXXXXXX

### Finally
Start it up!  
`python app.py`

In another window, you can start calling the API with e.g.  

Create user:  
`curl --data "phonenumber=4155555555" localhost:5000/user/create`  

You should recieve an SMS confirmation code. The code is also currently shown on the server console.  

Post that confirmation back with your number, and save the cookie which you get back:  
`curl localhost:5000/user/validate --data "phonenumber=4157455030&token=309058" -c cookies.txt`

The cookie has a session token which is then used for authenticating futher requests:

with session in cookie:
`curl localhost:5000/user/list -b cookies.txt`  
`AUTH SESSH!`

without:
`curl localhost:5000/user/list`  
Dingie, nae auth mate!`








