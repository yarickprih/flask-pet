import re
import uuid

from project import app, bcrypt, db
from sqlalchemy.orm import validates


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(8), unique=True, nullable=False)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email: str, password: str, username: str) -> None:
        self.email = email
        self.username = username
        self.uuid = str(uuid.uuid4())[:8]
        self.password = bcrypt.generate_password_hash(
            password, app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode()

    def __str__(self) -> None:
        return str(
            {
                "id": self.id,
                "uuid": self.uuid,
                "username": self.username,
                "email": self.email,
                "password": self.password,
            }
        )

    def __repr__(self) -> None:
        return str(
            {
                "id": self.id,
                "uuid": self.uuid,
                "username": self.username,
                "email": self.email,
                "password": self.password,
            }
        )

    @validates("username")
    def validate_username(self, _, username: str) -> str:
        username_validator = re.compile(r"^[A-Za-z][A-Za-z0-9_]{6,29}$")
        if not username_validator.match(username):
            raise AssertionError(
                "Username should contain latin letters both registers, or digits and have from 6 to 30 symbols length"
            )
        return username

    @validates("email")
    def validate_email(self, _, email: str) -> str:
        email_validator = re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        )
        if not email_validator.match(email):
            raise AssertionError("Incorrect email format!")
        return email
