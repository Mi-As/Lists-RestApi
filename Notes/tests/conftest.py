import os
import pytest
import tempfile
''' 
configures the application for testing and initializes a new database
https://flask.palletsprojects.com/en/1.1.x/testing/#the-testing-skeleton
'''

# FIXTURES
@pytest.fixture
def app():
	from .. import app
	from ..config import TestingConfig

	app.config.from_object(TestingConfig)
	
	return app

@pytest.fixture
def client(app):
	with app.test_client() as client:
		yield client		

@pytest.fixture
def db(app):
	from flask_sqlalchemy import SQLAlchemy

	# NEW TEST DATABASE
	db = SQLAlchemy()
	with app.app_context():
		db.init_app(app)
		db.create_all()	
		yield db

		#CLEAN UP
		db.session.remove()
		db.drop_all()
		
	os.remove(
		app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///',''))


		
		
		