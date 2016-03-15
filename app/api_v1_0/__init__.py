from flask import Blueprint
from app.ringbuffer import MarathonEventBuffer

api = Blueprint('api', __name__)

MARATHON_EVENTS = MarathonEventBuffer(1024)

from . import marathon, errors
