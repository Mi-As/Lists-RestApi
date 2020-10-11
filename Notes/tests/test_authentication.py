from flask import json
from flask_jwt_extended import (create_access_token as jwt_create_access_token)
from flask_jwt_extended import decode_token

from ..authentication.models import Token
from ..authentication.services import (create_access_token, create_refresh_token, 
	get_token_by_jti, revoke_token, revoke_user_tokens)


class TestModels:
	
	def test_new_token(self, db_session, test_user):
		token_user, _ = test_user
		test_token = jwt_create_access_token(identity=token_user.public_id, fresh=False)
		decoded_test_token = decode_token(test_token)
		# create token and add to database
		token_values = {'encoded_token': test_token, 'user_identity': token_user.public_id}
		db_session.add(Token(**token_values))
		db_session.commit()
		# test values
		new_token = get_token_by_jti(jti=decoded_test_token['jti'])
		assert new_token.jti
		assert new_token.type == 'access'
		assert new_token.revoked is not None
		assert new_token.expires
		assert new_token.user_public_id == token_user.public_id


class TestServices:

	def test_get_token_by_jti(self, user_tokens):
		tokens, token_user = user_tokens
		token_obj = get_token_by_jti(decode_token(tokens['access_token'])['jti'])

		assert token_obj.user_public_id == token_user.public_id
		assert not get_token_by_jti('i dont exist')

	def test_create_access_token(self, test_user):
		token_user, _ = test_user
		test_token = create_access_token(identity=token_user.public_id)
		token_obj = get_token_by_jti(decode_token(test_token)['jti'])

		assert test_token
		assert token_obj.user_public_id == token_user.public_id
		assert token_obj.type == 'access'

	def test_create_refresh_token(self, test_user):
		token_user, _ = test_user
		test_token = create_refresh_token(identity=token_user.public_id)
		token_obj = get_token_by_jti(decode_token(test_token)['jti'])

		assert test_token
		assert token_obj.user_public_id == token_user.public_id
		assert token_obj.type == 'refresh'

	def test_revoke_token(self, user_tokens):
		tokens, _ = user_tokens

		jit = decode_token(tokens['access_token'])['jti']
		revoke_token(jit)

		assert get_token_by_jti(jit).revoked == True
		assert not revoke_token('i dont exist')

	def test_revoke_user_tokens(self, user_tokens):
		_, token_user = user_tokens

		assert not revoke_user_tokens('i dont exist')
		
		revoke_user_tokens(token_user.public_id)
		for t in token_user.tokens:
			assert t.revoked


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


