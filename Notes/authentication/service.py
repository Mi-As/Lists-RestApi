from .. import db
from .models import Token
from ..apps.users.service import get_user_by_public_id

from flask_jwt_extended import create_access_token as jwt_create_access_token
from flask_jwt_extended import create_refresh_token as jwt_create_refresh_token

def create_access_token(identity='', fresh=False):
	access_token = jwt_create_access_token(identity=identity, fresh=fresh)
	obj_token = Token(access_token, identity)
	db.session.add(obj_token)
	db.session.commit()
	return access_token

def create_refresh_token(identity=''):
	refresh_token = jwt_create_refresh_token(identity=identity)
	obj_token = Token(refresh_token, identity)
	db.session.add(obj_token)
	db.session.commit()
	return refresh_token


def revoke_token(jti):
	token = get_token_by_jti(jti)
	if not token:
		return False
	token.revoked = True
	db.session.refresh(token)
	db.session.commit()
	return True

def revoke_user_tokens(user_public_id):
	user = get_user_by_public_id(user_public_id)
	if not user:
		return False
	for token in user.token:
		if not revoke_token(token.jti):
			return False
	return True


def get_token_by_jti(jti):
	try:
		token = Token.query.filter_by(jti=jti).one()
		return token
	except NoResultFound:
		return None

