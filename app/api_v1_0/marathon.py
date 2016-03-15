"""Marathon Event API
This implements a simple REST(ish) API to support the marathon event bus.
https://mesosphere.github.io/marathon/docs/event-bus.html

"""

import requests
import sys
from psutil import virtual_memory
from flask import jsonify, request, current_app, url_for, abort
from app.Models import MarathonEvent, MarathonEventBase
from . import api
from . import MARATHON_EVENTS as mbuf


@api.route('events/', methods=['GET'])
def get_events():
    """Return all events currently in the buffer"""
    return jsonify({'events': mbuf.get_summary_events()})


@api.route('events/', methods=['POST'])
def create_event():
    """Accept incoming events and store then in a buffer to be processed"""
    e = MarathonEvent()
    e.import_data(request)
    mbuf.add_event(e)
    return jsonify({}), 201, {'Location': e.get_url()}


@api.route('events/<int:event_id>')
def get_event_by_id(event_id):
    """Return an event based on event id"""
    for event in mbuf.get_events():
        if event.id == event_id:
            return jsonify(event.export_data())
    abort(404)


@api.route('events/testevent', methods=['POST'])
def generate_and_post_test_event():
    """Generate a test event and post it to our self"""
    current_app.logger.debug("posting to {}".format(
        url_for('api.create_event', _external=True)))
    r = requests.post(
        url_for('api.create_event', _external=True),
        json=MarathonEventBase.generate_fake_event()
    )
    rv = {
        'status': r.status_code,
        'message': 'event generated',
        'location': r.headers['location']
    }
    return jsonify(rv), r.status_code


@api.route('health', methods=['GET'])
def health_check():
    """return a health status of the framework"""
    mem = virtual_memory()
    bsize = 0
    for e in mbuf.get_events():
        bsize += sys.getsizeof(e)

    response = {
        'buffers': {
            'buffer size': mbuf.buffer.maxlen,
            'events buffered': mbuf.get_size(),
            'memory size': bsize + sys.getsizeof(mbuf)
        },
        'memory': {
            'total': mem.total / 1048576,
            'available': mem.available / 1048576,
            'percent': mem.percent,
            'used': mem.used / 1048576,
            'free': mem.free / 1048576
        }
    }

    return jsonify(response)
