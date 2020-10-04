from flask import json

class TestModels:
	pass

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
		tokens, _ = user_tokens

		headers = {'Content-Type': 'application/json',
				   'Authorization': 'Bearer ' + tokens['access_token']}
