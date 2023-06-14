# Simple scrpit for creating flask app
# Author: Jakub Sikula

# Import the necessary modules
from flask import Flask

# Import modules from api
from api.commands import register_commands
from api.routes import register_routes


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Load the default configuration
    app.config.from_pyfile('config.py')
    
    # Load cli commands and adress routes
    register_commands(app)
    register_routes(app)

    return app
