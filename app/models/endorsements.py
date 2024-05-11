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
    created_at: Mapped[datetime] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column()

    # Creates a Endorsement entry in the database
    def __init__(self, source_id: int, target_id: int, endorsement_post: int):
        self.source_id = source_id
        self.target_id = target_id
        self.endorsement_post = endorsement_post
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    # TODO: Returns a dictionary representation of the Endorsement (used for JSON serialization)
    def _asdict(self):
        return {'post': self.endorsement_post}
        # return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
