from ..apps.users import route, models

class TestEndpoints:
	pass

class TestModels:

	# ROLE
	def test_new_role(self, db_session):
		# create role and add to database
		role_values = {'name':'user','has_access':0}
		db_session.add(models.Role(**role_values))
		# get role and test values
		new_role = models.Role.query.filter_by(id=1).first()
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
			'role_name':'user'}  # reverenced role has to already exit
		db_session.add(models.User(**user_values))
		# get user and test values
		new_user = models.User.query.filter_by(id=1).first()
		assert new_user
		assert new_user.public_id
		assert new_user.name == user_values['name']
		assert new_user.email == user_values['email']
		assert new_user.check_password(user_values['password'])
		assert new_user.role_name == user_values['role_name']
