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

# app imports need to be before db.create_all()
# otherwise sqlalchemy won't recoginize models
from .apps import notes, users
from . import authentication as auth

with app.app_context():
    db.create_all()


# MIGRATE
migrate = Migrate(app, db)


# ROUTES
notes.init_app(app)
users.init_app(app)
auth.init_app(app)


# JWT
from .apps.users.services import get_user_one
from .authentication.services import get_token_by_jti
jwt = JWTManager(app)

@jwt.user_loader_callback_loader
def user_loader_callback(identity):
	return get_user_one({'public_id':identity})

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
	token = get_token_by_jti(decrypted_token['jti'])
	return None if not token else token.revoked


# HELLO WORLD
@app.route("/")
def hello():
    return jsonify({"msg":"Hello, World!"})

from flask_jwt_extended import jwt_required, fresh_jwt_required
@app.route("/protected")
@jwt_required
def protected_hello():
    return jsonify({"msg":"protected: Hello, World!"})

@app.route("/protected-fresh")
@fresh_jwt_required
def protected_fresh_hello():
	return jsonify({"msg":"protected fresh: Hello, World!"})

