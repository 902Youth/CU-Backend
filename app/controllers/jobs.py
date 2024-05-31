from flask import Blueprint, request
from db import db
from models.jobs import Job
import bcrypt
from datetime import datetime

# Create a Blueprint for the jobs routes
jobs = Blueprint('jobs', __name__)

# Validates the request body for update or post requests
def _validate_job(body):
    return (
        'user_id' in body and
        'country' in body and
        'city' in body and
        'state' in body and
        'description' in body and
        'title' in body and
        'upper_salary' in body and
        'lower_salary' in body and
        'deadline_date' in body and
        'employment_type' in body and
        'remote_eligibility' in body and
        'status' in body
    )

# Routes
@jobs.get('/')
def get_jobs():
    jobs = db.session.query(Job).all()
    return [jobs._asdict() for jobs in jobs]

# Create a job
@jobs.post('/')
def create_job():
    body = request.json

    # Validate request body
    if not _validate_job(body):
        return "Missing required fields", 400

    new_job = Job(
        user_id=body['user_id'],
        country=body['country'],
        city=body['city'],
        state=body['state'],
        description=body['description'],
        title=body['title'],
        upper_salary=float(body['upper_salary']),
        lower_salary=float(body['lower_salary']),
        deadline_date=datetime.strptime(body['deadline_date'], '%Y-%m-%d'),
        employment_type=body['employment_type'],
        remote_eligibility=bool(body['remote_eligibility']),
        status=body['status']
    )

    db.session.add(new_job)
    db.session.commit()

    return "Job created"

@jobs.put('/<id>')
def update_job(id):
    job = db.get_or_404(Job, id)
    body = request.json

    # Validate request body
    if not _validate_job(body):
        return "Missing required fields", 400

    job.country=body['country']
    job.city=body['city']
    job.state=body['state']
    job.description=body['description']
    job.title=body['title']
    job.upper_salary=float(body['upper_salary']),
    job.lower_salary=float(body['lower_salary'])
    job.deadline_date=datetime.strptime(body['deadline_date'], '%Y-%m-%d')
    job.employment_type=body['employment_type']
    job.remote_eligibility=bool(body['remote_eligibility'])
    job.status=body['status']
    job.updated_date=datetime.now()

    db.session.commit()
    return f"Updated job with id {id}"

@jobs.delete('/<id>')
def delete_job(id):
    job = db.get_or_404(Job, id)
    db.session.delete(job)
    db.session.commit()
    return f"Deleted job with id {id}"