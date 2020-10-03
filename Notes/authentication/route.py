from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
	create_access_token, create_refresh_token,
	jwt_refresh_token_required, get_jwt_identity)
from ..apps.users.models import User


auth_bp = Blueprint('auth', __name__)

# https://flask-jwt-extended.readthedocs.io/en/stable/
# Standard login endpoint. Will return a fresh access token and
# a refresh token
@auth_bp.route('/login', methods=['POST'])
def login():

	# validate if data is json
	if not request.is_json:
		return jsonify({"msg": "Missing JSON in request"}), 400

	# get and validate email and password
	email = request.json.get('email')
	password = request.json.get('password')
	if not email or not password:
		return jsonify({"msg": "Missing email or/and password parameter"}), 400
	# get user object
	requested_user = User.query.filter_by(email=email).first()
	try:
		if requested_user.check_password(password):
			ret = {
				'access_token': create_access_token(identity=requested_user.public_id, fresh=True),
				'refresh_token': create_refresh_token(identity=requested_user.public_id)}
			return jsonify(ret), 200

	except Exception as e:
		print(e)
	return jsonify({"msg": "Bad email or password"}), 401


# Refresh token endpoint. This will generate a new access token from
# the refresh token, but will mark that access token as non-fresh,
# as we do not actually verify a password in this endpoint.
@auth_bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
	current_user_public_id = get_jwt_identity()
	ret = {
		'access_token': create_access_token(identity=current_user_public_id, fresh=False)
	}
	return jsonify(ret), 200