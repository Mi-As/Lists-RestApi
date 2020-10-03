from flask import json
from ..apps.users.models import User, Role

auth_user = {'name':'auth user', 'email':'auth.user@email.com', 
			'password':'authuser'}

class TestAuthentication:

	def test_login(self, client, db_session, test_user):
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
		

	def test_refresh(self):
		url = '/refresh'

	def test_logout(self):
		url = '/logout'