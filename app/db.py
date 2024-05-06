from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Set up database instance
class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)