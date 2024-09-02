import os
from dotenv import load_dotenv
from flask import Flask

from board import pages, posts, database, errors

load_dotenv()       # Load Environment Variables

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    
    database.init_app(app)

    app.register_blueprint(pages.bp)
    app.register_blueprint(posts.bp)
    app.register_error_handler(404, errors.page_not_found)

    print(f"Current Environment: {os.getenv('ENVIRONMENT')}")
    print(f"Using Database: {app.config.get('DATABASE')}")
    return app