from flask import json
from ..apps.users import endpoints, models, services

url = '/user'

class TestModels:

	# ROLE
	def test_new_role(self, db_session):
		# create role and add to database
		role_values = {'name':'test','has_full_access':0}
		db_session.add(models.Role(**role_values))
		db_session.commit()
		# get role and test values
		new_role = services.get_role({'name':role_values['name']})
		assert new_role
		assert new_role.name == role_values['name']
		assert new_role.has_full_access == role_values['has_full_access']
	
	# USER
	def test_new_user(self, db_session):
		# create user and add to database
		user_values = {
			'name':'test user', 
			'email':'test@email.com', 
			'password':'testpassword', 
			'role_name':'test'}  # reverenced role has to already exit
		db_session.add(models.User(**user_values))
		db_session.commit()
		# get user and test values
		new_user = services.get_user({'email':user_values['email']})
		assert new_user
		assert new_user.public_id
		assert new_user.name == user_values['name']
		assert new_user.email == user_values['email']
		assert new_user.check_password(user_values['password'])
		assert new_user.role_name == user_values['role_name']


class TestServices:
	
	def test_get_user(self, test_user):
		user, _ = test_user

		filter_data1 = {'public_id': user.public_id}
		filter1 = services.get_user(filter_data1)
		assert filter1.public_id == user.public_id

		# no such value
		filter_data2 = {'public_id': 'i dont exist'}
		assert services.get_user(filter_data2) is None

		# key error
		filter_data3 = {'i dont exist': user.public_id}
		assert services.get_user(filter_data3) is None

	def test_get_users(self, test_user):
		user, _ = test_user
		assert services.get_users()

		filter_data1 = {'role_name': user.role_name}
		assert services.get_users(filter_data1)

		# no such value
		filter_data2 = {'role_name':'i dont exist'}
		assert not services.get_users(filter_data2)

		# key error
		filter_data3 = {'i dont exist': user.role_name}
		assert not services.get_users(filter_data3)

	def test_create_user(self):
		user_email = 'user123@email.com'

		new_user = services.create_user(
			name='user', email=user_email, password='userpassword')

		assert new_user
		assert services.get_user({'email':user_email}) 

	def test_update_user(self, test_user):
		user, user_data = test_user

		new_name = 'a new name'
		user.name = new_name
		services.update_user(user)

		updated_user = services.get_user({'email':user_data['email']})
		assert updated_user
		assert updated_user.name == new_name

	def test_delete_user(self, test_user):
		user, user_data = test_user
		services.delete_user(user)

		assert services.get_user({'email':user_data['email']}) is None

	def test_user_to_dict(self, test_user):
		user, _ = test_user

		dict_data = services.user_to_dict(user)

		assert dict_data['public_id'] == user.public_id
		assert dict_data['name'] == user.name
		assert dict_data['email'] == user.email
		assert dict_data['role_name'] == user.role_name


	def test_get_role(self, db_session):
		db_session.add(models.Role(name='get_test', has_full_access=0))
		db_session.commit()

		role1 = services.get_role({'name':'get_test'})
		assert role1.name == 'get_test'

		# no such value
		assert services.get_role({'name':'i dont exist'}) is None

	def test_get_all_roles(self, db_session):
		start_all = len(services.get_roles())
		
		data = {'name':'get_all_test', 'has_full_access':0}
		db_session.add(models.Role(**data))
		db_session.commit()

		assert len(services.get_roles()) == start_all + 1
		assert services.get_roles(data)


class TestEndpoints:
	
	def test_post_request(self, client):
		headers = {'Content-Type': 'application/json'}

		# valid data
		data1 = {'name':'asdf1','email':'asdf1','password':'asdf1'}
		response1 = client.post(url, headers=headers, data=json.dumps(data1))
		json_data1 = response1.get_json()
		assert response1.status_code == 201
		assert json_data1['msg'].startswith('New user created!')
		assert json_data1['user']['email'] == data1['email']
		assert services.get_user({'email': data1['email']})

		# invalid keys
		data2 = {'name':'asdf2','password':'asdf2'}
		response2 = client.post(url, headers=headers, data=json.dumps(data2))
		json_data2 = response2.get_json()
		assert response2.status_code == 400
		assert json_data2['msg'].startswith('A Key is missing')

		# invalid values
		data3 = {'name':'asdf3','email':'asdf3','password':''}
		response3 = client.post(url, headers=headers, data=json.dumps(data3))
		json_data3 = response3.get_json()
		assert response3.status_code == 400
		assert json_data3['msg'].startswith('Please check your data')

		# invalid values
		data4 = {'name':'asdf4','email':'asdf1','password':'asdf4'}
		response4 = client.post(url, headers=headers, data=json.dumps(data4))
		json_data4 = response4.get_json()
		assert response4.status_code == 409
		assert json_data4['msg'] == 'Email already in use!'

	def test_get_request(self, client, test_user):
		user, user_data = test_user

		headers = {'Content-Type': 'application/json',
				   'Authorization': 'Bearer ' + user_data['access_token']}
		response = client.get(url, headers=headers)
		json_data = response.get_json()

		assert response.status_code == 200
		assert json_data['public_id'] == user.public_id

	def test_put_request(self, client, test_user):
		user, user_data = test_user

		headers = {'Content-Type': 'application/json',
				   'Authorization': 'Bearer ' + user_data['access_token_fresh']}
		data = {'name':'new name 123', 'email':'new email 123', 'password':'new password 123'}
		response = client.put(url, headers=headers, data=json.dumps(data))
		json_data = response.get_json()

		assert response.status_code == 200
		assert json_data['msg'].startswith('User data')
		assert services.get_user({'email':data['email']})

	def test_delete_request(self, client, test_user):
		user, user_data = test_user

		headers = {'Content-Type': 'application/json',
				   'Authorization': 'Bearer ' + user_data['access_token_fresh']}
		response = client.delete(url, headers=headers)
		json_data = response.get_json()

		assert response.status_code == 200
		assert json_data['msg'].startswith('User ')
		assert services.get_user({'public_id':user.public_id}) is None
