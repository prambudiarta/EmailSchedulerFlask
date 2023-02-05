from flask import Flask, request, render_template, flash, redirect
import os
import psycopg2   
from dotenv import load_dotenv
from flask_mail import Mail, Message
import redis 
from rq import Queue
from datetime import datetime, timedelta
import time
import threading


### Database Query

# SCHEDULED MAIL TABLE

CREATE_SCHEDULED_MAIL_TABLE = ("CREATE TABLE IF NOT EXISTS scheduledMail (id SERIAL PRIMARY KEY, eventId INTEGER, emailSubject TEXT, emailContent TEXT, schedule TIMESTAMP);")

INSERT_SCHEDULED_MAIL = ("INSERT INTO scheduledMail (eventId, emailSubject, emailContent, schedule) VALUES (%s, %s, %s, TIMESTAMP %s);")

GET_SCHEDULED_EMAIL = "SELECT * FROM scheduledMail WHERE eventId = %s;"

# RECEIVER TABLE

CREATE_RECEIVER_TABLE = ("CREATE TABLE IF NOT EXISTS receiver (id SERIAL PRIMARY KEY, eventId INTEGER, mailAddress TEXT);")

INSERT_RECEIVER_MAIL = ("INSERT INTO receiver (eventId, mailAddress) VALUES (%s, %s);")

GET_USER_ID = "SELECT mailAddress FROM receiver WHERE eventId = %s;"

CHECK_IF_USER_REGISTERED = "SELECT mailAddress FROM receiver WHERE eventId = %s AND mailAddress = %s;"

# EVENT TABLE

CREATE_EVENT_TABLE = ("CREATE TABLE IF NOT EXISTS event (id SERIAL PRIMARY KEY, eventId INTEGER, desc TEXT);")

INSERT_EVENT = ("INSERT INTO event (eventId, desc) VALUES (%s, %s);")

GET_EVENT_ID = "SELECT * FROM event;"

# Loading Enviroment

load_dotenv()
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

# APP Initialize

app = Flask(__name__)
app.secret_key = 'thisissecretkey'
app.permanent_session_lifetime = timedelta(days=1)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
mail = Mail(app)
r = redis.Redis()
scheduler = Queue(connection=r)

# API & Route

@app.post('/save_emails')
def scheduledMail():
    eventId = request.form['eventId']
    emailSubject = request.form['emailSubject']
    emailContent = request.form['emailContent']
    schedule = request.form['schedule']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_SCHEDULED_MAIL_TABLE)
            cursor.execute("SET TIME ZONE 'Asia/Jakarta'")
            cursor.execute(INSERT_SCHEDULED_MAIL, (eventId, emailSubject, emailContent, schedule))
    connection.commit()
    format = "%Y-%m-%dT%H:%M"
    dt_object = datetime.strptime(schedule, format)
    delay = dt_object - datetime.now()
    if delay.total_seconds() > 0:
        scheduler.enqueue(background_task(eventId,emailSubject,emailContent,delay))
        flash("Message Queued!")
        return redirect('/')
    else:
        flash("Time Invalid!")
        return redirect('/')

@app.route('/register_receiver', methods=['GET', 'POST'])
def registerReceiver():
    if request.method == 'POST':
        eventId = request.form['eventId']
        mailAddress = request.form['mailAddress']
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_RECEIVER_TABLE)
                cursor.execute(CHECK_IF_USER_REGISTERED, (eventId, mailAddress))
                exist = cursor.fetchall()
                if (len(exist) == 0):
                    cursor.execute(INSERT_RECEIVER_MAIL, (eventId, mailAddress))
                    connection.commit()
                else:
                    flash('Email Already Registered For This Event!')
                    return render_template('regisEmail.html')
        flash('Success! Email Registered')
        return redirect('/register_receiver')
    else:
        return render_template('regisEmail.html')

@app.post('/register_event')
def registerEvent():
    eventId = request.form['eventId']
    desc = request.form['desc']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_RECEIVER_TABLE)
            cursor.execute(INSERT_RECEIVER_MAIL, (eventId, desc))
    connection.commit()
    return {"id":'OK'}

@app.get('/')
def home():
    return render_template('index.html')

def sendMail(eventId, emailSubject, emailBody, delay):
    with app.app_context():
        time.sleep(delay)
        try:
            receiver = []
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(GET_USER_ID, (eventId,))
                    for row in cursor:
                        (address,) = row
                        receiver.append(address)
            msg = Message(emailSubject, sender='noreply@jublia.com', recipients=receiver)
            msg.body = emailBody
            mail.send(msg)
        except Exception as e:
            print(e)
        return 'OK'

def background_task(eventId, emailSubject, emailBody, delay):
    t = threading.Thread(target=sendMail, args=[eventId, emailSubject, emailBody, delay.total_seconds()], daemon=True)
    t.start()
    return 'OK'