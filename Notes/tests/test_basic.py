
def test_hello_world(client):
	response = client.get('/')
	json_data = response.get_json()

	assert response.status_code == 200
	assert json_data[0]['msg'] == "Hello, World!"
