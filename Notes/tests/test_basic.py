
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


class TestHelloWorld:

	def test_hello_world(self, client):
		response = client.get('/')
		json_data = response.get_json()

		assert response.status_code == 200
		assert json_data[0]['msg'] == "Hello, World!"

	# def test_hello_world_protected(client):
	#	response = client.get('/protected')
