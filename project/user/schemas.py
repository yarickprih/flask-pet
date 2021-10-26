from enum import auto
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow_sqlalchemy.schema import auto_field

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
