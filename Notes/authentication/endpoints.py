from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
	jwt_refresh_token_required, get_jwt_identity, jwt_required)
from .services import create_access_token, create_refresh_token, revoke_user_tokens
from ..apps.users.services import get_user_one


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
	try:
		requested_user = get_user_one({'email': email}) # get user object
		if requested_user.check_password(password):
			identity = requested_user.public_id
			ret = {
				'access_token': create_access_token(identity=identity, fresh=True),
				'refresh_token': create_refresh_token(identity=identity)}
			return jsonify(ret), 200

	except Exception as e:
		print(e)
	return jsonify({"msg": "Bad email or password"}), 401

# This will generate a new access token from the refresh token, but
# will mark that access token as non-fresh
@auth_bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
	current_user_public_id = get_jwt_identity()
	ret = {
		'access_token': create_access_token(identity=current_user_public_id, fresh=False)}
	return jsonify(ret), 200

# Endpoint for revoking the current users access and refesh token
@auth_bp.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
	user_public_id = get_jwt_identity()
	if revoke_user_tokens(user_public_id):
		return jsonify({"msg": "Successfully logged out"}), 200
	else:
		return jsonify({"msg": "Cannot revoke token"}), 404

