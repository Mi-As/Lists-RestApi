from werkzeug.security import check_password_hash, generate_password_hash
import uuid
from ... import db

# import like this bc: https://stackoverflow.com/questions/43576422/sqlalchemy-flask-class-is-not-defined
from ..notes import models as notes
from ...authentication import models as authenticaton
from . import services




class User(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50), nullable=False, unique=True)

	name = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False)

	# Relationships
	# One-to-Many
	role_name = db.Column(db.String, db.ForeignKey('role.name'))
	# Many-to-One
	notes = db.relationship('Note', passive_deletes='all')
	tokens = db.relationship('Token', passive_deletes='all')

	def __init__(self, name, email, password, role_name='user'):
		self.public_id = str(uuid.uuid4())
		self.name = name
		self.email = email
		self.set_password(password)
		self.set_role_name(role_name)

	def set_role_name(self, role_name):
		role = services.get_role(name=role_name)
		assert role, "no such user_role!" 
		self.role_name = role_name

	def set_password(self, secret):
		self.password = generate_password_hash(secret)

	def check_password(self, secret):
		return check_password_hash(self.password, secret)

class Role(db.Model):  # ['Admin', 'User']
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, unique=True, nullable=False)
	has_access = db.Column(db.Boolean, nullable=False, default=False)
	