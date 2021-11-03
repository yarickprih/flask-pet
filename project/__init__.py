import os

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
api = Api()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(
        os.getenv("CONFIG", default="project.config.DevelopmentConfig")
    )
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    add_api_resources(api)
    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)
    migrate.init_app(app, db)
    return app


def register_blueprints(app):
    from .user import user_blueprint

    app.register_blueprint(user_blueprint)


def add_api_resources(api):
    from .user.resources import Login, UserResource, UsersResource

    api.add_resource(UserResource, "/user/<uuid>")
    api.add_resource(UsersResource, "/user")
    api.add_resource(Login, "/login")
