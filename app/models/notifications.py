from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from flask_sqlalchemy import SQLAlchemy
import db

class Notification(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    notifiedUserId: Mapped[int] = mapped_column(Integer, index=True)
    message: Mapped[str] = mapped_column(String(255))
    createdAt: Mapped[datetime] = mapped_column(DateTime, datetime=datetime.datetime.utcnow())
    acknowledgedAt: Mapped[datetime] = mapped_column(DateTime, nullable=True)			


    def __init__(self, id: int, notifiedUserId: int, message: str):
        self.id = id
        self.notifiedUserId = notifiedUserId
        self.message = message
        self.createdAt = datetime.datetime.utcnow()
        self.acknowledgedAt = None;

    def __repr__(self):
        return f'<Notification {self.id}>'
    


                                    