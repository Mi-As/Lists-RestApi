from functools import wraps
import sqlalchemy
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, current_user

def except_invalid_request_error(func):
	@wraps(func)
	def wrapped(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except sqlalchemy.exc.InvalidRequestError:
			return None
	return wrapped


def admin_jwt_required(func):
	@wraps(func)
	def wrapped(*args, **kwargs):
		verify_jwt_in_request()
		if current_user.role.has_access:
			return func(*args, **kwargs)
		else:
			return jsonify(
				{"msg":"Insufficient user rights!"}), 403
	return wrapped