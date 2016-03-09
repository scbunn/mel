from flask import Blueprint
from app.RingBuffer import RingBuffer

api = Blueprint('api', __name__)

# Create a ring buffer to hold events for every event type
EVENT_BUFFERS = {
    'marathon_events': RingBuffer(1024),
}

from . import marathon
