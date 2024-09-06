import os
from dotenv import load_dotenv
from flask import Flask
from flask_pymongo import PyMongo
from flask_moment import Moment

from board import database, pages, posts, errors

load_dotenv()       # Load Environment Variables
moment = Moment()

def create_app():
    app = Flask(__name__)
    moment.init_app(app)
    app.config.from_prefixed_env()
    app.config['MONGO_URI'] = os.getenv('MONGO_URL')
    app.config['DATABASE'] = 'messages'
    mongo = PyMongo(app)
    #app.logger.setLevel('INFO')

    database.init_app(app)

    app.register_blueprint(pages.bp)
    app.register_blueprint(posts.bp)
    app.register_error_handler(404, errors.page_not_found)

    app.logger.debug(f"Current Environment: {os.getenv('ENVIRONMENT')}")
    app.logger.debug(f"Using Database: {app.config.get('MONGO_URI')}")
    return app
