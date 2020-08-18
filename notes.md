To access db in Terminal

export FLASK_APP=main.py
flask shell

from model import Villain, db

user = Villain.query.get(1)

user.name = "make change here"

db.session.commit()

