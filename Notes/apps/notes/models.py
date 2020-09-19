from ... import db
import uuid

class Note(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	# Date der erstellung
	date = db.Column(db.DateTime)
	# is Active				löschen nach 7 Tagen wenn auf False?

	# Relationship: User (Many to one?)
	# Relationship: Tags zum sotrieren	essen, lernen, ...
	# Relationship: Art zum anzeigen		todo, notiz, ...