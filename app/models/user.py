# from sqlalchemy import String, BINARY
# from sqlalchemy.orm import Mapped, mapped_column
# from flask_login import UserMixin
# from db import db


# # class to handle user model
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(150), unique=True)
#     username = db.Column(db.String(30), unique=True)
#     fullname = db.Column(db.String(70))
#     password = db.Column(db.String(150))

# Defines a User model
# class User(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     username: Mapped[str] = mapped_column(String(30), unique=True)
#     firstname: Mapped[str] = mapped_column(String(30))
#     lastname: Mapped[str] = mapped_column(String(40))
#     hash: Mapped[str] = mapped_column(BINARY(60))

#     # Creates a User entry in the database
#     def __init__(self, firstname: str, lastname: str, username: str, hash: str, salt: str):
#         self.firstname = firstname
#         self.lastname = lastname
#         self.username = username
#         self.hash = hash

#     # Returns a dictionary representation of the User (used for JSON serialization)
#     def _asdict(self):
#         return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


from sqlalchemy import BINARY, DATETIME, VARCHAR, BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from db import db
from datetime import datetime

# Defines a User model
class User(db.Model):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    fullname: Mapped[str] = mapped_column(VARCHAR(50))
    username: Mapped[str] = mapped_column(VARCHAR(35))
    mobile: Mapped[str] = mapped_column(VARCHAR(15))
    email: Mapped[str] = mapped_column(VARCHAR(50))
    hash: Mapped[str] = mapped_column(BINARY(60))
    registeredAt: Mapped[str] = mapped_column(DATETIME)
    lastLogin: Mapped[str] = mapped_column(DATETIME)

    # Creates a User entry in the database
    def __init__(self, fullname: str, mobile: str,  username: str, email: str, hash: str):
        self.fullname = fullname
        self.mobile = mobile
        self.username = username
        self.email = email
        self.hash = hash
        self.registeredAt = datetime.now()

    # Returns a dictionary representation of the User (used for JSON serialization)
    def _asdict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}