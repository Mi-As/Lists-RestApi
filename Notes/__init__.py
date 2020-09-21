from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# CONFIGURATION
from .config import DevelopmentConfig
app.config.from_object(DevelopmentConfig)

# DATABASE
db = SQLAlchemy()
db.init_app(app)
with app.app_context():
    db.create_all()

# MIGRATE
migrate = Migrate(app, db)

# ROUTES
from .apps import notes, users
notes.init_app(app)
users.init_app(app)

from . import authentication as auth
auth.init_app(app)

# JWT
jwt = JWTManager(app)

@jwt.user_loader_callback_loader
def user_loader_callback(identity):
	requested_user = users.models.User.query.filter_by(public_id=identity).first()
	return requested_user

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
	requested_user = users.models.User.query.filter_by(public_id=identity).first()
	return {'role':requested_user.role_name}

# HELLO WORLD
@app.route("/")
def hello():
    return jsonify([{"msg":"Hello, World!"}])

# PROTECTED HELLO WORLD
from flask_jwt_extended import jwt_required
@app.route("/protected")
@jwt_required
def protected_hello():
    return jsonify([{"protected msg":"Hello, World!"}])


