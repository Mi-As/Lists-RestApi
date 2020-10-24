from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, fresh_jwt_required, current_user

from .services import (user_to_dict, get_user_all, 
	create_user, update_user, delete_user)


class UserAPI(MethodView):
	""" Endpoint: /user """

	def post(self):
		"""
		creates a new user
		:params name, email, password: 
		:return: success message
		"""
		json_data = request.get_json()

		# check if all keys are existing
		if not set(['name','email','password']) == json_data.keys():
			return jsonify({"msg":'A Key is missing, check: name, email, password!'}), 400

		# check for empty strings
		if not len(json_data) == len(list(filter(None,json_data.values()))):
			return jsonify({"msg":'Please check your data, no empty strings allowed!'}), 400

		# check if email is unique
		for u in get_user_all():
			if u.email == json_data['email']:
				print(u.email, u.name)
				return jsonify({"msg":'Email already in use!'}), 409

		# create user
		new_user = create_user(
			name=json_data['name'],
			email=json_data['email'],
			password=json_data['password'])

		return jsonify(
			{"msg":'New user created! Hello {} :)'.format(new_user.name),
			 "user": user_to_dict(new_user)}
		), 201

	@jwt_required
	def get(self):
		""" 
		:return: userdata from currently logged in user
		"""
		return jsonify(user_to_dict(current_user)), 200

	@fresh_jwt_required
	def put(self):
		"""
		updates current user data
		:params name, email, password:
		:return: success message
		"""

		json_data = request.get_json()

		for key, data in json_data.items():
			if key == 'name':
				current_user.name = data
			elif key == 'email':
				current_user.email = data
			elif key == 'password':
				current_user.set_password(data)

		update_user(current_user)

		return jsonify({"msg":
			'User data {} successfully updated!'.format(list(json_data.keys()))
		}), 200

		
	@fresh_jwt_required
	def delete(self):
		"""
		deletes current user
		:return: success message
		"""
		delete_user(current_user)
		return jsonify({"msg":"User '{}' has been successfully deleted!".format(current_user.name)}), 200

