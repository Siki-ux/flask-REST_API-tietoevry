# Simple scrpit for API of DB about movies
# Author: Jakub Sikula

# Import the necessary modules
from flask import Flask

from api.commands import register_commands
from api.routes import register_routes


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Load the default configuration
    app.config.from_pyfile('config.py')
    
    register_commands(app)
    register_routes(app)

    return app
