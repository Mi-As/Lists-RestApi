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

# ROLE
def get_role(name):
	return models.Role.query.filter_by(name=name).first()

def get_roles_by_access(has_access):
	return models.Role.query.filter_by(has_access=has_access).all()

def get_all_roles():
	return models.Role.query.all()	
