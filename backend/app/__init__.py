from distutils.command.config import config
from flask import Flask
import psycopg2


import peewee as pe
from peewee import *


def create_app():
    a = Flask(__name__)
    a.config.from_object(config)
    a.config['JSON_AS_ASCII'] = False
    # p_db = pe.PostgresqlDatabase('blogstore2', user='lee', password='****', host='*****', port=26000)
    conns = psycopg2.connect(database="blogstore2", user="lee", password="****", host="****", port=26000)
    return a, conns


app, conn = create_app()
cur = conn.cursor()

from app.api import api as api_blueprint

app.register_blueprint(api_blueprint, url_prefix="/api/v1.0")
app.run()



