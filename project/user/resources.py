from flask import request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from project import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from .models import User
from .schemas import UserSchema, UserSchemaOutput

user_schema = UserSchema()
user_schema_output = UserSchemaOutput()
users_schema_output = UserSchemaOutput(many=True)


class UserResource(Resource):
    def get(self, uuid):
        if user := User.query.filter_by(uuid=uuid).first():
            return user_schema_output.dump(user), 200
        return {"error": f"User with uuid '{uuid}' wasn't found"}

    def put(self, uuid):
        user_data = request.json
        user_instance = User.query.filter_by(uuid=uuid).first_or_404(
            description=f"User with uuid '{uuid}' wasn't found"
        )
        user = user_schema.load(
            user_data,
            session=db.session,
            instance=user_instance,
            partial=True,
        )
        try:
            user.add()
        except AssertionError as err:
            return {"error": str(err)}, 400
        except ValidationError as err:
            return {"error": str(err)}, 422
        except IntegrityError as err:
            return {"error": str(err)}, 409
        return user_schema_output.dump(user)

    def delete(self, uuid):
        user = User.query.filter_by(uuid=uuid).first_or_404(
            description=f"User with uuid '{uuid}' wasn't found"
        )
        user.delete()
        return user_schema_output.dump(user), 204


class UsersResource(Resource):
    def get(self):
        if users := User.query.all():
            return users_schema_output.dump(users), 200
        return {"message": "No users found"}

    def post(self):
        user_data = request.json
        user = User(**user_data)
        try:
            user.add()
        except AssertionError as err:
            return {"error": str(err)}, 400
        except ValidationError as err:
            return {"error": str(err)}, 422
        except IntegrityError:
            return {"error": "User with such credentials already exists"}, 409
        return user_schema_output.dump(user), 201


class Login(Resource):
    def post(self):
        data = request.json
        user = User.query.filter_by(username=data["username"]).first()
        if not user:
            return {"error": f"Username '{data['username']}' doesn't exist"}, 422
        if not check_password_hash(user.password, data["password"]):
            return {"error": "Invalid credentials"}, 422
        return {"message": "You've been authenticated successfully"}, 200
