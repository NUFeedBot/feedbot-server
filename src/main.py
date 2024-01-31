from flask import Flask
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('db.json')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/submission/<id>")
def submission(id):
    Entry = Query()
    submission = db.search(Entry.id == id)
    if len(submission) == 0:
        return f"<p>Error: Could not find a submission with the given id: {id}</p>"
    else:
        return f"<code>{submission[0].code}</code>"

@app.route("/entry")
def receive_entry():
    data = request.args
    if validate(data):
        db.insert(transform(data))
    return {'data': data}, 200

# this will eventually validate that the sender of an entry is us,
# presumably by using a shared key
def validate(args):
    return True

# this will eventually change the received entry to contain properly
# formatted data (I think just exchanging NUID or email for an SSO token?)
def transform(args):
    return args
