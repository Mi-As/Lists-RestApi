import os
import tempfile

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True

	SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'main.db')

	SECRET_KEY = 'mySecretDevelopmentKey'
	JWT_SECRET_KEY = 'myJwtDevelopmentKey'

	DEVELOPMENT = True
	DEBUG = True

# class ProductionConfig(Config):
#	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
#	SECRET_KEY = os.environ.get('SECRET_KEY')
#	JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') #Todo: b19105c8-9594-43f4-9143-4ac619e855c7

#	DEBUG = False

#class TestingConfig(Config):
#	SECRET_KEY = 'my_testing_key'
#	TESTING = True

