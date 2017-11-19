def test_hello_world(client):
	response = client.get('/')

	assert response.status_code == 200
