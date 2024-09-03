import click
from flask import current_app, g
from flask_pymongo import PyMongo
from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv() 

mongo = PyMongo()

def init_app(app):
    mongo.init_app(app)
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@click.command('init-db')
def init_db_command():
    db = get_db()
    click.echo('You Sucessfully initialised the database!')

def get_db():
    if 'db' not in g:
        client = MongoClient(current_app.config['MONGO_URI'])
        g.db = client[current_app.config['DATABASE']]
    return g.db
    
def close_db(e=None):
    pass