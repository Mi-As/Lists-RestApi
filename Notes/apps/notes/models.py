from ... import db
from datetime import datetime
from ..users.models import User
import uuid

class Note(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50), nullable=False, unique=True)

	text = db.Column(db.String)
	date = db.Column(db.DateTime, nullable=False)
	is_active = db.Column(db.Boolean, nullable=False) # note löschen nach 7 Tagen wenn auf False?		

	# Relationships
	# One-to-Many
	user_public_id = db.Column(db.Integer, db.ForeignKey('user.public_id', ondelete='CASCADE'))
	type_name =	db.Column(db.String, db.ForeignKey('note_type.name'))
	# Many-to-Many
	tags = db.relationship('note_tags', secondary='tags_to_note', backref=db.backref('note'))

	def __init__(self, user_public_id, type_name='note', tag_list=[], text='no text'):
		self.public_id = str(uuid.uuid4())
		self.text = text
		self.date = datetime.now().date()
		self.is_active=True
		self.set_user_id(user_public_id)
		self.set_type_name(type_name)
		self.set_tags(tag_list)


	def set_user_id(user_public_id):
	 	user = User.query.filter_by(public_id=user_public_id).first()
	 	assert user, "no such user_public_id!" # 500 internal server error
	 	self.user_id.append(user_public_id)
 
	def set_type_name(type_name):
		note_type = note_type.query.filter_by(name=type_name).first()
		assert note_type, "no such type_name!" # 500 internal server error
		self.type_name.append(note_type.name)
	 	
	def set_tags(tag_list):
		for t in tag_list:
			tag = note_tags.query.filter_by(name=t).first()
			# if tag does not exits make new one
			if not tag:
				tag = note_tags(name=t)
				db.session.add(tag)
			self.tags.append(tag)


note_type = db.Table('note_type',
	db.Column('id', db.Integer, primary_key=True),
	db.Column('name', db.String, unique=True)
)

note_tags = db.Table('note_tags',
	db.Column('id', db.Integer, primary_key=True),
	db.Column('name', db.String, unique=True)
)

tags_to_note = db.Table('tags_to_note',
	db.Column('note_id', db.Integer, ForeignKey('note.id'), primary_key=True),
	db.Column('tags_id', db.Integer, ForeignKey('tags.id'), primary_key=True)
)
