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

import binascii
from sqlalchemy import BINARY, DATETIME, VARCHAR, BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from db import db
from datetime import datetime
from methods.encdec import hash_password, verify_password

# Defines a User model
class User(db.Model):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    fullname: Mapped[str] = mapped_column(VARCHAR(50))
    username: Mapped[str] = mapped_column(VARCHAR(35))
    mobile: Mapped[str] = mapped_column(VARCHAR(15))
    email: Mapped[str] = mapped_column(VARCHAR(50))
    hash: Mapped[str] = mapped_column(VARCHAR(255))
    # hash: Mapped[bytes] = mapped_column(BINARY(60))
    registeredAt: Mapped[str] = mapped_column(DATETIME)
    lastLogin: Mapped[str] = mapped_column(DATETIME)
    
    # Profile picture fields
    pfp_id: Mapped[int] = mapped_column(BIGINT, nullable=True, autoincrement=True)
    pfp_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    pfp_last_modified: Mapped[int] = mapped_column(BIGINT, nullable=True)
    pfp_size: Mapped[int] = mapped_column(nullable=True)
    pfp_type: Mapped[str] = mapped_column(VARCHAR(50), nullable=True)

    # Background picture fields
    bg_pic_id: Mapped[int] = mapped_column(BIGINT, nullable=True, autoincrement=True)
    bg_pic_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    bg_pic_last_modified: Mapped[int] = mapped_column(BIGINT, nullable=True)
    bg_pic_size: Mapped[int] = mapped_column(nullable=True)
    bg_pic_type: Mapped[str] = mapped_column(VARCHAR(50), nullable=True)

    # Creates a User entry in the database
    def __init__(self, fullname: str, mobile: str,  username: str, email: str, hash: str):
        self.fullname = fullname
        self.mobile = mobile
        self.username = username
        self.email = email
        self.hash = hash_password(hash)
        self.registeredAt = datetime.now()

    # Returns a dictionary representation of the User (used for JSON serialization)
    def _asdict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
    
    
    def verify_user(self, password: str) -> bool:
        return verify_password(password.encode(), self.hash)
    # def verify_password(self, password):
    #     self.hash = self.hash.decode()
    #     try: 
    #         return check_password_hash(self.hash, password)
    #     except ValueError as e:
    #         print(f'Error: {e}')