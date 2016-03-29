# Up 4 Stuff reboot!

## Python/Flask API server, Mac Users, instructions:::::

Grab this code:
`git clone git@github.com:sideb0ard/up4stuff.git`

`cd up4stuff`

Ensure you have virtualenv installed, then create a new Python environment:
`virtualenv venv`

Activate the env:
`source venv/bin/activate`

Install requirements files:
`pip install -r requirements.txt`


Run `./dbstuff.py` to create a local sqlite3 DB.  

Then post to the api with e.g

`curl --data "username=thorBLAH&&phonenumber=4155555500" localhost:5000/user/create`
