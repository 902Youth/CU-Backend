from sqlalchemy import String, BINARY
from sqlalchemy.orm import Mapped, mapped_column
from db import db
from datetime import datetime

# Defines an Endorsement model
class Endorsement(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column()
    target_id: Mapped[int] = mapped_column()
    endorsement_post: Mapped[int] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column()
    message: Mapped[str] = mapped_column(String(3000))
    likes: Mapped[int] = mapped_column()
    recipient_name: Mapped[str] = mapped_column(String(100))
    recipient_username: Mapped[str] = mapped_column(String(100))
    recipient_profile_pic: Mapped[str] = mapped_column(String(100))
    recipient_profile_url: Mapped[str] = mapped_column(String(100))
    endorser_name: Mapped[str] = mapped_column(String(100))
    endorser_username: Mapped[str] = mapped_column(String(100))
    endorser_profile_pic: Mapped[str] = mapped_column(String(100))
    endorser_profile_url: Mapped[str] = mapped_column(String(100))
    comments: Mapped[int] = mapped_column()


    # Creates a Endorsement entry in the database
    def __init__(self, source_id: int, target_id: int, endorsement_post: int, timestamp: datetime ,message: str, likes: int = 0, recipient_name: str = None, recipient_username: str = None, recipient_profile_pic: str = None, recipient_profile_url: str = None, endorser_name: str = None, endorser_username: str = None, endorser_profile_pic: str = None, endorser_profile_url: str = None, comments: int = 0):
        self.source_id = source_id
        self.target_id = target_id
        self.endorsement_post = endorsement_post
        self.timestamp = timestamp
        self.message = message
        self.likes = likes
        self.recipient_name = recipient_name
        self.recipient_username = recipient_username
        self.recipient_profile_pic = recipient_profile_pic
        self.recipient_profile_url = recipient_profile_url  
        self.endorser_name = endorser_name
        self.endorser_username = endorser_username
        self.endorser_profile_pic = endorser_profile_pic
        self.endorser_profile_url = endorser_profile_url
        self.comments = comments
        

    # TODO: Returns a dictionary representation of the Endorsement (used for JSON serialization)
    def _asdict(self):
        # return {'post': self.endorsement_post}
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
