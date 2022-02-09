from dataclasses import dataclass

from werkzeug.security import generate_password_hash, check_password_hash

from .BaseModel import BaseModel, db


@dataclass
class UserModel(BaseModel):
    __tablename__ = 'users'

    username: str
    password: str

    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    """ Database operations """

    @classmethod
    def find_by_username(cls, _username):
        return cls.query.filter_by(username=_username).first()

    """ Utility functions """

    @staticmethod
    def generate_hash(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_hash(password, hashed_password):
        return check_password_hash(password, hashed_password)
