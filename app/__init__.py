import logging
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Enable error logging
    logging.basicConfig(level=logging.DEBUG)

    # Register routes
    from .routes import main
    app.register_blueprint(main)

    return app
