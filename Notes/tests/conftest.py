import os
import pytest
import tempfile

''' 
configures the application for testing and initializes a new database
https://flask.palletsprojects.com/en/1.1.x/testing/	the-testing-skeleton
'''

# FIXTURES
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

@pytest.fixture(scope='class')
def db_session(app, db):

	with app.app_context():
		yield db.session

		#CLEAN UP
		db.session.rollback()
		db.session.close()


		