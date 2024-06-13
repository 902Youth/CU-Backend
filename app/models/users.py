from sqlalchemy import String, BINARY
from sqlalchemy.orm import Mapped, mapped_column
from db import db

# Defines a User model
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    firstname: Mapped[str] = mapped_column(String(30))
    lastname: Mapped[str] = mapped_column(String(40))
    hash: Mapped[str] = mapped_column(BINARY(60))

    # Creates a User entry in the database
    def __init__(self, firstname: str, lastname: str, username: str, hash: str, salt: str):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.hash = hash

    # Returns a dictionary representation of the User (used for JSON serialization)
    def _asdict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
