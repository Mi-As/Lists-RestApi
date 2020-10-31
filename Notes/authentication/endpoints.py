from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
	jwt_refresh_token_required, get_jwt_identity, jwt_required)

from . import services
from ..apps.users import services as user_services


auth_bp = Blueprint('auth', __name__)

# https://flask-jwt-extended.readthedocs.io/en/stable/
@auth_bp.route('/login', methods=['POST'])
def login():
	"""
	Authenticates user.
	:params email, password:
	:return: access_token, refresh_token
	"""

	# validate if data is json
	if not request.is_json:
		return jsonify({"msg": "Missing JSON in request"}), 400

	# get and validate email and password
	email = request.json.get('email')
	password = request.json.get('password')
	if not email or not password:
		return jsonify({"msg": "Missing email or/and password parameter"}), 400
	
	requested_user = user_services.get_user({'email': email}) # get user object
	if not requested_user:
		return jsonify({"msg": "Bad email or password"}), 401

	if requested_user.check_password(password):
		identity = requested_user.public_id
		ret = {
			'access_token': services.create_access_token(identity=identity, fresh=True),
			'refresh_token': services.create_refresh_token(identity=identity)}
		return jsonify(ret), 200
	else:
		return jsonify({"msg": "Bad email or password"}), 401


@auth_bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
	"""
	Generate a new access token, marks it as non-fresh
	:return: access_token
	"""
	current_user_public_id = get_jwt_identity()
	ret = {
		'access_token': services.create_access_token(identity=current_user_public_id, fresh=False)}
	return jsonify(ret), 200


@auth_bp.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
	"""
	Revokes the current users access and refesh token
	:return: success message
	"""
	user_public_id = get_jwt_identity()
	if services.revoke_user_tokens(user_public_id):
		return jsonify({"msg": "Successfully logged out"}), 200
	else:
		return jsonify({"msg": "Cannot revoke token"}), 404

