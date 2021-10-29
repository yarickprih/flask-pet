from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow_sqlalchemy.schema import auto_field
from marshmallow import Schema, fields
from .models import User


class UserSchema(SQLAlchemySchema):

    username = auto_field()
    email = auto_field()
    password = auto_field()

    class Meta:
        model = User
        load_instance = True


class UserSchemaOutput(SQLAlchemySchema):

    id = auto_field()
    uuid = auto_field()
    username = auto_field()
    email = auto_field()
    password = auto_field()

    class Meta:
        model = User


class UserLogin(Schema):
    username = fields.Str()
    password = fields.Str()
