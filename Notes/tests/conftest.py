import os
import pytest
import random
import string
import tempfile

from ..apps.users.models import Role
from ..apps.users.services import create_user, get_role

from ..apps.notes.models import NoteType, NoteTag
from ..apps.notes.services import create_note, get_note_type

from ..authentication.services import create_access_token, create_refresh_token
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
	if not get_role('user'):
		db_session.add(Role(name='user', has_access=0))
		db_session.commit()

	rdm_name = random_str('name')
	user_data = {'name': rdm_name, 
				 'email': (rdm_name + '@email.com'),
				 'password': rdm_name}
				
	user = create_user(**user_data)

	ret = {
		'access_token_fresh': create_access_token(identity=user.public_id, fresh=True),
		'access_token': create_access_token(identity=user.public_id, fresh=False),
		'refresh_token': create_refresh_token(identity=user.public_id)}

	return user, {**user_data, **ret}

@pytest.fixture(scope='function')
def test_user_note(test_user, db_session):
	user, user_data = test_user

	if not get_note_type('note'):
		db_session.add(NoteType(name='note'))
		db_session.commit()

	note = create_note(
		user_public_id=user.public_id,
		tag_list=['music'],
		text=random_str('note'))
	return user, user_data, note

@pytest.fixture(scope='function')
def test_user_tag(test_user, db_session):
	user, user_data = test_user

	tag = NoteTag(user_public_id=user.public_id, name=random_str('tag'))
	db_session.add(tag)
	db_session.commit()

	return user, user_data, tag



def random_str(prefix):
	return (
		prefix +'_' + 
		''.join(random.choice(string.ascii_lowercase) for l in range(10))
	)