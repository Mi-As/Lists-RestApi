from ... import db
from werkzeug.security import check_password_hash, generate_password_hash
import uuid

class User(db.Model):
	__tabelname__ = 'users'
	user_id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50), nullable=False, unique=True)

	name = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False)

	role = db.relationship('Role', secondary='user_roles')

	def __init__(self,name,email,password):
		self.public_id = str(uuid.uuid4())
		self.name = name
		self.email = email
		self.set_password(password)

	def set_password(self, secret):
		self.password = generate_password_hash(secret)

	def check_password(self, secret):
		return check_password_hash(self.password, secret)
	
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True) # 'Admin', 'User'

class UserRoles(db.Model): # association table
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))	
