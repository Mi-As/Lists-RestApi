from ... import db
from datetime import datetime
import uuid
# import like this bc: https://stackoverflow.com/questions/43576422/sqlalchemy-flask-class-is-not-defined
from ..users import models as users

class Note(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50), nullable=False, unique=True)

	text = db.Column(db.String)
	last_change_time = db.Column(db.DateTime, nullable=False)
	is_active = db.Column(db.Boolean, nullable=False) # note löschen nach 7 Tagen wenn auf False?		

	# Relationships
	# One-to-Many
	user_public_id = db.Column(db.String(50), db.ForeignKey('user.public_id', ondelete='CASCADE'))
	type_name =	db.Column(db.String, db.ForeignKey('note_type.name'))
	# Many-to-Many
	tags = db.relationship('NoteTag', secondary='tags_to_note', backref=db.backref('note'))

	def __init__(self, user_public_id, type_name='note', tag_list=[], text='no text'):
		self.public_id = str(uuid.uuid4())
		self.text = text
		self.last_change_time = datetime.now()
		self.is_active=True
		self.set_user_id(user_public_id)
		self.set_type_name(type_name)
		self.set_tags(tag_list)

	def set_user_id(self, user_public_id):
	 	user = users.User.query.filter_by(public_id=user_public_id).first()
	 	assert user, "no such user_public_id!" # 500 internal server error
	 	self.user_public_id = user_public_id
 
	def set_type_name(self, type_name):
		note_type = NoteType.query.filter_by(name=type_name).first()
		assert note_type, "no such type_name!" # 500 internal server error
		self.type_name = note_type.name
	 	
	def set_tags(self, tag_list):
		self.tags = []
		for t in tag_list:
			tag = NoteTag.query.filter_by(name=t).first()
			# if tag does not exits make new one
			if not tag:
				tag = NoteTag(name=t)
				db.session.add(tag)
			if not tag in self.tags:
				self.tags.append(tag)


class NoteType(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)


class NoteTag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)


# association table
tags_to_note = db.Table('tags_to_note',
	db.Column('note_id', db.Integer, db.ForeignKey('note.id'), primary_key=True),
	db.Column('tags_id', db.Integer, db.ForeignKey('note_tag.id'), primary_key=True)
)
