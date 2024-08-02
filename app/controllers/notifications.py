from flask import Blueprint
from models.notification import Notification
import datetime
from flask import jsonify

notifications = Blueprint('notifications', __name__)


@notifications.route('', methods=['GET'])
def get_notifications():
    new_notification = Notification(id=1, notifiedUserId=2, message="testing")
    print(jsonify(new_notification))
    return jsonify({'status': 'success', 'message': 'Notification Sent'}), 200
