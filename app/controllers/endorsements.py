from flask import Blueprint, request
from db import db
from models.endorsements import Endorsement
import bcrypt
from datetime import datetime

# Create a Blueprint for the endorsements routes
endorsements = Blueprint('endorsements', __name__)

# Utility functions

# Gets all endorsements for this follower
def get_followers_endorsement(id):
    return get_endorsements(id)

# Returns the number of endorsements for this user
def get_endorsement_count(id):
    return len(get_endorsement_count(id))


# Routes
@endorsements.get('/<source_id>')
def get_endorsements(source_id):
    endorsements = db.session.query(Endorsement).filter(Endorsement.source_id == source_id)
    return [endorsement._asdict() for endorsement in endorsements]

@endorsements.post('/<source_id>/<target_id>')
def create_endorsement(source_id, target_id):
    body = request.json

    # Add the new endorsement to the database 
    new_endorsement = Endorsement(
        source_id=source_id,
        target_id=target_id,
        endorsement_post=1,
        recipient_name=body['recipient']['name'],
        recipient_username=body['recipient']['username'],
        recipient_profile_pic=body['recipient']['recipient_profile_pic'],
        recipient_profile_url=body['recipient']['recipient_profile_url'],
        endorser_name=body['endorser']['name'],
        endorser_username=body['endorser']['username'],
        endorser_profile_pic=body['endorser']['endorser_profile_pic'],
        endorser_profile_url=body['endorser']['endorser_profile_url'],
        timestamp=datetime.strptime(body['timestamp'], "%Y-%m-%dT%H:%M:%SZ"),
        message=body['message'],
        likes=body.get('likes', 0),
        comments=body.get('comments', 0)
    )
    
    db.session.add(new_endorsement)
    db.session.commit()
    
    return {"message": "Endorsement created", "endorsement": new_endorsement._asdict()}, 201

@endorsements.put('/<id>')
def update_endorsement(id):
    endorsement = db.get_or_404(Endorsement, id)

    # Update user fields
    current_time = datetime.now()
    endorsement.updated_at = current_time
    db.session.commit()
    return f"Updated endorsement with id {id} at {current_time}"

@endorsements.delete('/<id>')
def delete_endorsement(id):
    endorsement = db.get_or_404(Endorsement, id)
    db.session.delete(endorsement)
    db.session.commit()
    return f"Deleted endorsement with id {id}"