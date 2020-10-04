from flask import json
from ..authentication import models

from flask_jwt_extended import (create_access_token as jwt_create_access_token)
from flask_jwt_extended import decode_token

class TestModels:
	
	def test_new_token(self, db_session, test_user):
		token_user, _ = test_user
		test_token = jwt_create_access_token(identity=token_user.public_id, fresh=False)
		decoded_test_token = decode_token(test_token)
		# create token and add to database
		token_values = {'encoded_token': test_token, 'user_identity': token_user.public_id}
		db_session.add(models.Token(**token_values))
		db_session.commit()
		# test values
		new_token = models.Token.query.filter_by(jti=decoded_test_token['jti']).one()
		assert new_token.jti
		assert new_token.token_type == 'access'
		assert new_token.revoked is not None
		assert new_token.expires
		assert new_token.user_public_id == token_user.public_id

class TestServices:
	pass

class TestEndpoints:

	def test_login(self, client, test_user):
		url = '/login'
		_, user_data = test_user
		# authentication
		# valid data
		data = {'email': user_data['email'], 'password':user_data['password']} 
		headers = {'Content-Type': 'application/json'}
		response = client.post(url, headers=headers, data=json.dumps(data))
		json_data = response.get_json()

		assert response.status_code == 200
		assert json_data['access_token']
		assert json_data['refresh_token']

		# invalid data
		data = {'email': user_data['email'], 'password': 'asdf'} 
		headers = {'Content-Type': 'application/json'}
		response = client.post(url, headers=headers, data=json.dumps(data))
		json_data = response.get_json()

		assert response.status_code == 401
		assert json_data['msg'] == "Bad email or password"
		

	def test_refresh(self, client, user_tokens):
		url = '/refresh'
		tokens, _ = user_tokens

		headers = {'Content-Type': 'application/json',
				   'Authorization': 'Bearer ' + tokens['refresh_token']}
		response = client.post(url, headers=headers)
		json_data = response.get_json()

		assert response.status_code == 200
		assert json_data['access_token']

	def test_logout(self, client, user_tokens):
		url = '/logout'
		tokens, user = user_tokens

		headers = {'Content-Type': 'application/json',
				   'Authorization': 'Bearer ' + tokens['access_token']}
		response = client.delete(url, headers=headers)
		json_data = response.get_json()

		assert response.status_code == 200
		assert json_data['msg'] == "Successfully logged out"
		for token_obj in user.tokens:
			assert token_obj.revoked == True


