from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DATETIME
from sqlalchemy.orm import relationship, mapped_column, Mapped
from flask_sqlalchemy import SQLAlchemy
from db import db

class Notification(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    notifiedUserId: Mapped[int] = mapped_column(Integer, index=True)
    message: Mapped[str] = mapped_column(String(255))
    createdAt: Mapped[datetime] = mapped_column(DATETIME)
    acknowledgedAt: Mapped[datetime] = mapped_column(DATETIME, nullable=True)			


    def __init__(self, id: int, notifiedUserId: int, message: str):
        self.id = id
        self.notifiedUserId = notifiedUserId
        self.message = message
        self.createdAt = datetime.utcnow()
        self.acknowledgedAt = None;

    def __repr__(self):
        return f'<Notification {self.id}>'
    


                                    