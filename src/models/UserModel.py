from dataclasses import dataclass

from werkzeug.security import generate_password_hash, check_password_hash

from .BaseModel import BaseModel
from src.extensions import db


@dataclass
class UserModel(BaseModel):
    __tablename__ = 'users'

    email: str
    email_verified: bool
    password: str

    email = db.Column(db.String, nullable=False, unique=True)
    email_verified = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String, nullable=False)

    """ Database operations """

    @classmethod
    def find_by_email(cls, _email):
        return cls.find_by_first(email=_email)

    """ Utility functions """

    @staticmethod
    def generate_hash(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_hash(password, hashed_password):
        return check_password_hash(password, hashed_password)
