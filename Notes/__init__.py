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
from .apps.users.service import get_user_by_public_id
from .authentication.service import get_token_by_jti
jwt = JWTManager(app)

@jwt.user_loader_callback_loader
def user_loader_callback(identity):
	return get_user_by_public_id(identity)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
	requested_user = get_user_by_public_id(identity)
	return {'role':requested_user.role_name}

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


