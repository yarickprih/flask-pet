from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from .config import DevelopmentConfig
from .user import user_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(user_bp)
ma = Marshmallow(app)
api = Api(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)


from .user import models
from .user import resources as user_resources

api.add_resource(user_resources.UserResource, "/user/<uuid>")
api.add_resource(user_resources.UsersResource, "/user")


if __name__ == "__main__":
    app.run()
