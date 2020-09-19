from ... import db
from werkzeug.security import check_password_hash, generate_password_hash
import uuid

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50), nullable=False, unique=True)

	name = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False)

	role = db.relationship('Role', secondary='user_role')

	def __init__(self, name, email, password, role_name='User'):
		self.public_id = str(uuid.uuid4())

		self.name = name
		self.email = email
		self.set_password(password)

		user_role = Role.query.filter_by(name=role_name).first()
		assert user_role, "no such user_role!" # 500 internal server error
		self.role.append(user_role)

	def set_password(self, secret):
		self.password = generate_password_hash(secret)

	def check_password(self, secret):
		return check_password_hash(self.password, secret)
	
class Role(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(50), unique=True)

# Define the user_role association table
user_role = db.Table('user_role',
	db.Column('user_id', db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')),
	db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
)

