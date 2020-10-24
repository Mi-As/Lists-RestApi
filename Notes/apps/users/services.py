from flask import jsonify, json

from ... import db
from ..services import except_invalid_request_error as except_error
from . import models


# USER 
@except_error
def get_user_one(filter_data):
	return models.User.query.filter_by(**filter_data).first()

@except_error
def get_user_all(filter_data=None):
	if filter_data:
		return models.User.query.filter_by(**filter_data).all()
	return models.User.query.all()

def create_user(name, email, password, role_name='user'):
	new_user = models.User(name, email, password, role_name)
	db.session.add(new_user)
	db.session.commit()

	return new_user

def update_user(user_obj):
	db.session.add(user_obj)
	db.session.commit()

def delete_user(user_obj):
	db.session.delete(user_obj)
	db.session.commit()


def user_to_dict(user_obj):
	return {
		'public_id': user_obj.public_id,
		'name': user_obj.name,
		'email': user_obj.email,
		'role_name': user_obj.role_name
	}


# ROLE
def get_role(name):
	return models.Role.query.filter_by(name=name).first()

def get_roles_by_access(has_access):
	return models.Role.query.filter_by(has_access=has_access).all()

def get_all_roles():
	return models.Role.query.all()	
