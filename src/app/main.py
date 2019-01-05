"""Application definition"""
from flask import Flask
from flask_mongoengine import MongoEngine
import os

# flask mongoengine
db = MongoEngine()

from app.api_routes import api
from app.app_routes import app_bp

def create_app():
    """ Create and return a Flask app with right config depending on the environment"""
    app = Flask(__name__)
    app.register_blueprint(api)
    app.register_blueprint(app_bp)

    app.config.update(
        MONGO_CONNECT=False,
        DEBUG=False if os.getenv('DEBUG', 'False') == 'False' else True,
        TESTING=False if os.getenv('TESTING', 'False') == 'False' else True,
        MONGODB_HOST=os.getenv('MONGODB_HOST', 'localhost'),
        MONGODB_PORT=int(os.getenv('MONGODB_PORT', 27017)),
        MONGODB_DB=os.getenv('MONGODB_DB', 'spil'),
    )

    db.init_app(app)
    return app

if __name__ == '__main__':
    server = create_app()
    server.run()
