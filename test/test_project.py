def test_home(client):
    response = client.get('/')
    assert b'<h1>Save Email</h1>' in response.data