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

	def test_get_token_by_jti(self, test_user):
		token_user, user_data = test_user
		token_obj = get_token_by_jti(decode_token(user_data['access_token'])['jti'])

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

	def test_revoke_token(self, test_user):
		_, user_data = test_user

		jit = decode_token(user_data['access_token'])['jti']
		revoke_token(jit)

		assert get_token_by_jti(jit).revoked == True
		assert not revoke_token('i dont exist')

	def test_revoke_user_tokens(self, test_user):
		token_user, _ = test_user

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
		data1 = {'email': user_data['email'], 'password': user_data['password']} 
		headers1 = {'Content-Type': 'application/json'}
		response1 = client.post(url, headers=headers1, data=json.dumps(data1))
		json_data1 = response1.get_json()

		assert response1.status_code == 200
		assert json_data1['access_token']
		assert json_data1['refresh_token']

		# invalid user password
		data2 = {'email': user_data['email'], 'password': 'invalid'} 
		headers2 = {'Content-Type': 'application/json'}
		response2 = client.post(url, headers=headers2, data=json.dumps(data2))
		json_data2 = response2.get_json()

		assert response2.status_code == 401
		assert json_data2['msg'] == "Bad email or password"

		# invalid user email
		data3 = {'email': 'invalid', 'password': user_data['password']} 
		headers3 = {'Content-Type': 'application/json'}
		response3 = client.post(url, headers=headers3, data=json.dumps(data3))
		json_data3 = response3.get_json()

		assert response3.status_code == 401
		assert json_data3['msg'] == "Bad email or password"

		# invalid json data
		data4 = {'email': 'invalid', 'password':user_data['password']} 
		response4 = client.post(url, data=data3)
		json_data4 = response4.get_json()

		assert response4.status_code == 400
		assert json_data4['msg'] == "Missing JSON in request"

		# invalid post data
		data5 = {'email': user_data['email'], 'invalid':user_data['password']} 
		headers5 = {'Content-Type': 'application/json'}
		response5 = client.post(url, headers=headers5, data=json.dumps(data5))
		json_data5= response5.get_json()

		assert response5.status_code == 400
		assert json_data5['msg'] == "Missing email or/and password parameter"

	def test_refresh(self, client, test_user):
		url = '/refresh'
		_, user_data = test_user

		headers = {'Content-Type': 'application/json',
				   'Authorization': 'Bearer ' + user_data['refresh_token']}
		response = client.post(url, headers=headers)
		json_data = response.get_json()

		assert response.status_code == 200
		assert json_data['access_token']

	def test_logout(self, client, test_user):
		url = '/logout'
		user, user_data = test_user

		headers = {'Content-Type': 'application/json',
				   'Authorization': 'Bearer ' + user_data['access_token']}
		response = client.delete(url, headers=headers)
		json_data = response.get_json()

		assert response.status_code == 200
		assert json_data['msg'] == "Successfully logged out"
		for token_obj in user.tokens:
			assert token_obj.revoked == True


