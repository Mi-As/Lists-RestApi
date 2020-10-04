import os
import tempfile

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True

	JWT_BLACKLIST_ENABLED = True
	JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

	SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'main.db')

	SECRET_KEY = 'mySecretDevelopmentKey'
	JWT_SECRET_KEY = 'myJwtDevelopmentKey'

	DEVELOPMENT = True
	DEBUG = True

class TestingConfig(Config):
	db_fd, db_temp_file_uri = tempfile.mkstemp(
		suffix = '.db', 
		dir= os.path.join(basedir, 'tests/tmp/'))

	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_temp_file_uri

	SECRET_KEY = 'mySecretTestingKey'
	JWT_SECRET_KEY = 'myJwtTestingKey'

	TESTING = True

# class ProductionConfig(Config):
#	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
#	SECRET_KEY = os.environ.get('SECRET_KEY')
#	JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

#	DEBUG = False

