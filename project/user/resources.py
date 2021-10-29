import bcrypt
from flask import request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from project import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from .models import User
from .schemas import UserLogin, UserSchema, UserSchemaOutput

user_schema = UserSchema()
user_schema_output = UserSchemaOutput()
users_schema_output = UserSchemaOutput(many=True)
user_login_schema = UserLogin()


class UserResource(Resource):
    def get(self, uuid):
        user = User.query.filter_by(uuid=uuid).first_or_404(
            description=f"User with uuid '{uuid}' wasn't found"
        )
        return user_schema_output.dump(user), 200

    def put(self, uuid):
        user_data = request.json
        user_instance = User.query.filter_by(uuid=uuid).first_or_404(
            description=f"User with uuid '{uuid}' wasn't found"
        )
        try:
            user = user_schema.load(
                user_data,
                session=db.session,
                instance=user_instance,
                partial=True,
            )
            db.session.add(user)
            db.session.commit()
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
        db.session.delete(user)
        db.session.commit()
        return user_schema_output.dump(user), 204


class UsersResource(Resource):
    def get(self):
        users = User.query.all()
        return (
            {"message": "No users found"}
            if not users
            else users_schema_output.dump(users),
            200,
        )

    def post(self):
        user_data = request.json
        try:
            user = User(**user_data)
            db.session.add(user)
            db.session.commit()
        except AssertionError as err:
            return {"error": str(err)}, 400
        except ValidationError as err:
            return {"error": str(err)}, 422
        except IntegrityError as err:
            return {"error": str(err)}, 409
        return user_schema_output.dump(user), 201


class Login(Resource):
    def post(self):
        data = request.json
        user = User.query.filter_by(username=data["username"]).first()
        if not user:
            return {"error": f"Username '{data['username']}' doesn't"}, 422
        if not bcrypt.checkpw(
            data["password"].encode("utf-8"), user.password.encode("utf-8")
        ):
            return {"error": "Invalid credentials"}, 422

        return {"message": "You've been authenticated successfully"}, 200
