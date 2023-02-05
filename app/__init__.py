from flask import Flask
import os
import psycopg2   
from dotenv import load_dotenv
from datetime import timedelta


app = Flask(__name__)
app.secret_key = 'thisissecretkey'
app.permanent_session_lifetime = timedelta(days=1)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
load_dotenv()
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

from app import route