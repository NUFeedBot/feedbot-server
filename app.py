import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

# NOTE(dbp 2024-02-06): bit of a hack; probably better to do this with a .env file
if not "DATABASE_URL" in os.environ:
    os.environ["DATABASE_URL"] = 'postgresql:///feedbot_user:111@feedbot_dev'

app = Flask(__name__)
db = SQLAlchemy()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/submission/<id>")
def submission(id):
    # TODO: SQL sanitization
    submission = db.one("SELECT * FROM submissions WHERE id='%s'", id)
    if submission is None:
        return f"<p>Error: Could not find a submission with the given id: {id}</p>"
    else:
        return f"<code>{submission.code}</code>"


@app.route("/entry")
def receive_entry():
    data = request.args
    if validate(data):
        db.run(f"INSERT INTO submissions VALUES ({data.code}, {data.id})")
    return {'data': data}, 200


# this will eventually validate that the sender of an entry is us,
# presumably by using a shared key
def validate(args):
    return True


# this will eventually change the received entry to contain properly
# formatted data (I think just exchanging NUID or email for an SSO token?)
def transform(args):
    return args
