from flask_jwt_extended import verify_jwt_in_request

class TestFixtures:

	def test_fixture_app(self, app):
		assert app

	def test_fixture_client(self, client):
		assert client

	def test_fixture_db(self, db):
	 	assert db
	 	assert db.engine.table_names(), "No tables created"

	def test_fixture_db_session(self, db_session):
		assert db_session

	def test_fixture_user(self, test_user):
		user, user_data = test_user
		assert user
		assert user_data

	def test_fixture_note(self, test_user_note):
		user, user_data, note = test_user_note
		assert user
		assert user_data
		assert note

	def test_fixture_tag(self, test_user_tag):
		user, user_data, tag = test_user_tag
		assert user
		assert user_data
		assert tag


class TestHelloWorld:

	def test_hello_world(self, client):
		response = client.get('/')
		json_data = response.get_json()

		assert response.status_code == 200
		assert json_data['msg'] == "Hello, World!"

	def test_hello_world_protected(self, client, test_user):
		_, user_data = test_user
		headers = {'Content-Type': 'application/json',
				   'Authorization': 'Bearer ' + user_data['access_token']}
		response = client.get('/protected', headers=headers)
		json_data = response.get_json()

		assert response.status_code == 200
		assert json_data['msg'] == "protected: Hello, World!"

	def test_hello_world_protected_fresh(self, client, test_user):
		_, user_data = test_user
		headers = {'Content-Type': 'application/json',
				   'Authorization': 'Bearer ' + user_data['access_token_fresh']}
		response = client.get('/protected-fresh', headers=headers)
		json_data = response.get_json()

		assert response.status_code == 200
		assert json_data['msg'] == "protected fresh: Hello, World!"



