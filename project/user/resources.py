from flask import request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from project import db
from sqlalchemy.exc import IntegrityError

from .models import User
from .schemas import UserSchema, UserSchemaOutput

user_schema = UserSchema()
user_schema_output = UserSchemaOutput()
users_schema_output = UserSchemaOutput(many=True)


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
