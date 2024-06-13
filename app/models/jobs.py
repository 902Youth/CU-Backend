from sqlalchemy import String, Boolean, Float, ForeignKey, BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from db import db
from datetime import datetime

# Defines a Job model
class Job(db.Model):
	id: Mapped[int] = mapped_column(primary_key=True)
	user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('user.id'))
	posted_date: Mapped[datetime] = mapped_column()
	updated_date: Mapped[datetime] = mapped_column()
	country: Mapped[str] = mapped_column(String(50))
	city: Mapped[str] = mapped_column(String(50))
	state: Mapped[str] = mapped_column(String(50))
	description: Mapped[str] = mapped_column(String(3000))
	title: Mapped[str] = mapped_column(String(100))
	upper_salary: Mapped[float] = mapped_column(Float)
	lower_salary: Mapped[float] = mapped_column(Float)
	deadline_date: Mapped[datetime] = mapped_column()
	employment_type: Mapped[str] = mapped_column(String(30))
	status: Mapped[str] = mapped_column(String(10), default='open')
	remote_eligibility: Mapped[bool] = mapped_column(Boolean)

	def __init__(self, user_id: int, country: str, city: str, state: str, description: str, title: str, upper_salary: float, lower_salary: float, deadline_date: datetime, employment_type: str, remote_eligibility: bool, status: str):
		self.user_id = user_id
		self.country = country
		self.city = city
		self.state = state
		self.description = description
		self.title = title
		self.upper_salary = upper_salary
		self.lower_salary = lower_salary
		self.deadline_date = deadline_date
		self.employment_type = employment_type
		self.remote_eligibility = remote_eligibility
		self.posted_date = datetime.now()
		self.updated_date = datetime.now()
		self.status = status

	# Returns a dictionary representation of the Job (used for JSON serialization)
	def _asdict(self):
			return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
