import os
import uuid
import names
import pytest
import tempfile

from ..apps.users.models import User, Role
from ..authentication.service import create_access_token, create_refresh_token
''' 
configures the application for testing and initializes a new database
https://flask.palletsprojects.com/en/1.1.x/testing/	the-testing-skeleton
'''
# init db

# FIXTURES: SESSION
@pytest.fixture(scope='session')
def app():
	from .. import app
	from ..config import TestingConfig
	app.config.from_object(TestingConfig)
	
	return app

@pytest.fixture(scope='session')
def client(app):
	with app.test_client() as client:
		yield client	


@pytest.fixture(scope='session')
def db(app):	
	from .. import db
	with app.app_context():
		db.create_all()
		yield db

		#CLEAN UP
		db.drop_all()
		 
	os.remove(
		app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///',''))	

# FIXTURES: CLASS
@pytest.fixture(scope='class')
def db_session(app, db):
	# Use flush() instead of commit() to
	# communicate with the database while testing

	with app.app_context():
		yield db.session

		#CLEAN UP
		db.session.rollback()
		db.session.close()

# FIXTURES: FUNCTION
@pytest.fixture(scope='function')
def test_user(db_session):
	if not len(Role.query.filter_by(name='user').all()):
		db_session.add(Role(name='user', has_access=0))

	unique_name = names.get_last_name()
	user_data = {'name': unique_name, 
				 'email': (unique_name + '@email.com'),
				 'password': str(uuid.uuid4().hex)}
	user =User(**user_data)
	db_session.add(user)
	db_session.commit()
	return user, user_data

@pytest.fixture(scope='function')
def user_tokens(test_user):
	user, _ = test_user
	ret = {
		'access_token_fresh': create_access_token(identity=user.public_id, fresh=True),
		'access_token': create_access_token(identity=user.public_id, fresh=False),
		'refresh_token': create_refresh_token(identity=user.public_id)}
	return ret, user