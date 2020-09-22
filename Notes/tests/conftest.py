import os
import pytest
import tempfile
from flask_sqlalchemy import SQLAlchemy

''' 
configures the application for testing and initializes a new database
https://flask.palletsprojects.com/en/1.1.x/testing/#the-testing-skeleton
'''

from .. import app

# CONFIGURATION
from ..config import TestingConfig
app.config.from_object(TestingConfig)

# FIXTURE
@pytest.fixture
def client():

	db_fd, db_temp_file_uri = tempfile.mkstemp(
		suffix = '.db', 
		dir='/home/miriam/Projects/Python/Flask/Notes/Notes/tests/tmp/')

	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_temp_file_uri

	with app.test_client() as client:

		# DATABASE
		db = SQLAlchemy()
		with app.app_context():
			db.init_app(app)
			db.create_all()	

		yield client

		#CLEAN UP
		db.session.remove()
		db.drop_all()
		
	os.remove(db_temp_file_uri)


		
		
		