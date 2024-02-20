from __future__ import annotations

import os
from typing import List
from random import randint

from flask import Flask, request

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

# NOTE(dbp 2024-02-06): bit of a hack; probably better to do this with a .env file
if "DATABASE_URL" not in os.environ:
    os.environ["DATABASE_URL"] = 'postgresql://feedbot_user:111@localhost/feedbot_dev'


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Submission(db.Model):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    sso: Mapped[str]
    code: Mapped[str]
    comments: Mapped[List["Comment"]] = relationship(back_populates="entry")


class Comment(db.Model):
    __tablename__ = "comments"

    line_number: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    subm_id = mapped_column(ForeignKey("submissions.id"))
    entry: Mapped[Submission] = relationship(back_populates="comments")


with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/submission/<int:id>")
def submission(id):
    submission = db.get_or_404(Submission, id)
    return f"""<p>
        id: {submission.id},
        sso: {submission.sso},
        code: <code>{submission.code}</code>
        comments: {submission.comments}
    </p>"""


@app.route("/entry", methods=['POST'])
def receive_entry():
    data = request.args
    print(f"data: {data}")
    id = 0
    if validate(data):
        submission, id = transform(data)
        print(f"id: {id}")
        db.session.add(submission)
        db.session.commit()
    return {'msg': f"id: {id}"}, 200


# this will eventually validate that the sender of an entry is us,
# presumably by using a shared key
def validate(data):
    return True


# this will eventually change the received entry to contain properly
# formatted data (I think just exchanging NUID or email for an SSO token?)
def transform(data):
    gen_id = randint(200, 100000)
    return (
        Submission(
            # TODO: actual ID assignment
            id=gen_id,
            # TODO: SSO assignment
            sso="",
            code=data["code"],
            comments=[],
        ),
        gen_id
    )
