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
from .apps import lists, users
lists.init_app(app)
users.init_app(app)

from . import authentication as auth
auth.init_app(app)

# JWT
jwt = JWTManager(app)

@app.route("/")
def hello():
    return jsonify([{"message":"Hello, World!"}])


