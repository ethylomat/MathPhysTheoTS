from flask_sqlalchemy import SQLAlchemy
from app import db, Ticket
import os

os.system("rm tickets.db")

validcode_file = "test.txt"

db.create_all()

with open(validcode_file) as f:
    content = f.read().splitlines()[1:]

for i in content:
	ticket = Ticket(i)
	db.session.add(ticket)

db.session.commit()
