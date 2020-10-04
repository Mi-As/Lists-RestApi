from . import models

def get_user_by_email(email):
	try:
		return models.User.query.filter_by(email=email).one()
	except NoResultFound:
		return None

def get_user_by_public_id(public_id):
	try:
		return models.User.query.filter_by(public_id=public_id).one()
	except NoResultFound:
		return None
