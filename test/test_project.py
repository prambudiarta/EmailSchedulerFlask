from flask import url_for, request

def test_home(client):
    response = client.get('/')
    assert b'<h1>Save Email</h1>' in response.data

def test_register_receiver(client):
    response = client.get('/register_receiver')
    assert b'<h1>Register Receiver</h1>' in response.data

def test_save_email(client):
    response = client.post('/save_emails', data={'eventId':'1', 'emailSubject':'Alpha', 'emailContent':'Beta', 'schedule':'2023-05-06T02:17'}, follow_redirects=True)
    assert b"Message Queued!" in response.data

def test_save_email_invalid_time(client):
    response = client.post('/save_emails', data={'eventId':'1', 'emailSubject':'Alpha', 'emailContent':'Beta', 'schedule':'1997-05-06T02:17'}, follow_redirects=True)
    assert b"Time Invalid!" in response.data

def test_email_exist(client):
    response = client.post('/register_receiver', data={'eventId':'1', 'mailAddress':'prambudiarta@gmail.com'}, follow_redirects=True)
    assert b"Email Already Registered For This Event!" in response.data

def test_email_success(client):
    response = client.post('/register_receiver', data={'eventId':'4', 'mailAddress':'test@mail.com'}, follow_redirects=True)
    assert b"Success! Email Registered" in response.data