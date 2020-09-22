import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True

	SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'main.db')
	print(SQLALCHEMY_DATABASE_URI)

	SECRET_KEY = 'mySecretDevelopmentKey'
	JWT_SECRET_KEY = 'myJwtDevelopmentKey'

	DEVELOPMENT = True
	DEBUG = True

# class ProductionConfig(Config):
#	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
#	SECRET_KEY = os.environ.get('SECRET_KEY')
#	JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') #Todo: b19105c8-9594-43f4-9143-4ac619e855c7

#	DEBUG = False

class TestingConfig(Config):
	SQLALCHEMY_DATABASE_URI = '' # tempfile
	# 'sqlite:///' + os.path.join(basedir, 'test.db')

	SECRET_KEY = 'mySecretTestingKey'
	JWT_SECRET_KEY = 'myJwtTestingKey'

	TESTING = True

