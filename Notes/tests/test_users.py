from flask import json
from ..apps.users import endpoints, models

from ..apps.users.services import get_user_one, get_user_all, get_role, get_roles_by_access, get_all_roles

url = '/user'

class TestModels:

	# ROLE
	def test_new_role(self, db_session):
		# create role and add to database
		role_values = {'name':'test','has_access':0}
		db_session.add(models.Role(**role_values))
		db_session.commit()
		# get role and test values
		new_role = get_role(name=role_values['name'])
		assert new_role
		assert new_role.name == role_values['name']
		assert new_role.has_access == role_values['has_access']
	
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
		new_user = get_user_one({'email':user_values['email']})
		assert new_user
		assert new_user.public_id
		assert new_user.name == user_values['name']
		assert new_user.email == user_values['email']
		assert new_user.check_password(user_values['password'])
		assert new_user.role_name == user_values['role_name']

class TestServices:
	
	def test_get_user_one(self, test_user):
		user, _ = test_user

		filter_data1 = {'public_id': user.public_id}
		filter1 = get_user_one(filter_data1)
		assert filter1.public_id == user.public_id

		# no such value
		filter_data2 = {'public_id': 'i dont exist'}
		assert get_user_one(filter_data2) is None

		# key error
		filter_data3 = {'i dont exist': user.public_id}
		assert get_user_one(filter_data3) is None

	def test_get_user_all(self, test_user):
		user, _ = test_user
		assert get_user_all()

		filter_data1 = {'role_name': user.role_name}
		assert get_user_all(filter_data1)

		# no such value
		filter_data2 = {'role_name':'i dont exist'}
		assert not get_user_all(filter_data2)

		# key error
		filter_data3 = {'i dont exist': user.role_name}
		assert not get_user_all(filter_data3)

	def test_get_role(self, db_session):
		db_session.add(models.Role(name='get_test', has_access=0))
		db_session.commit()

		role1 = get_role('get_test')
		assert role1.name == 'get_test'

		# no such value
		assert get_role('i dont exist') == None

	def test_get_roles_by_access(self, db_session):
		start_has_access = len(get_roles_by_access(1))

		db_session.add(models.Role(name='get_all_by_access_test', has_access=1))
		db_session.commit()

		assert len(get_roles_by_access(1)) == start_has_access + 1

		# no such values
		assert not get_roles_by_access('i dont exist')

	def test_get_all_roles(self, db_session):
		start_all = len(get_all_roles())
		
		db_session.add(models.Role(name='get_all_test', has_access=0))
		db_session.commit()

		assert len(get_all_roles()) == start_all + 1


class TestEndpoints:
	
	def test_post_request(self, client):
		pass

	def test_get_request(self, client):
		pass

	def test_put_request(self, client):
		pass

	def test_delete_request(self, client):
		pass
